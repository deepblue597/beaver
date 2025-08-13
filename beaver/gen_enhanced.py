"""
Enhanced code generation with static validation for Beaver DSL.
This script generates Python code from Beaver DSL files and performs comprehensive validation.
"""

import argparse
import ast
import sys
import os
from pathlib import Path
from textx import metamodel_from_file
from jinja2 import Environment, FileSystemLoader
import subprocess
import tempfile

# Add parent directory to path for imports
from calc import *
from validator import validate_beaver_model, ModelValidator


def parse_command_line_arguments():
    parser = argparse.ArgumentParser(description='Enhanced Pipeline generator with validation')
    
    parser.add_argument('--metamodel', default='examples/model.bvr',
                       help='The file in which your pipeline is configured', type=str)
    parser.add_argument('--generated_file_name', default='generated_pipeline.py',
                       help='Destination file name', type=str)
    parser.add_argument('--validate-only', action='store_true',
                       help='Only perform validation without code generation')
    parser.add_argument('--skip-validation', action='store_true',
                       help='Skip static validation and generate code directly')
    parser.add_argument('--check-syntax', action='store_true',
                       help='Check Python syntax of generated code')
    parser.add_argument('--strict-analysis', action='store_true',
                       help='Use strict mode for static analysis (errors fail generation)')
    parser.add_argument('--skip-static-analysis', action='store_true',
                       help='Skip static analysis (only syntax and compilation)')
    parser.add_argument('--dry-run', action='store_true',
                       help='Show what would be generated without writing files')
    parser.add_argument('--verbose', '-v', action='store_true',
                       help='Enable verbose output')
    
    return parser.parse_args()


def validate_generated_syntax(code: str) -> tuple[bool, str]:
    """
    What it does:

    ast.parse(code): Converts Python code string into an Abstract Syntax Tree
    If successful: Code has valid Python syntax
    If SyntaxError: Code has syntax problems (missing parentheses, indentation errors, etc.)
    Returns: Success boolean + descriptive message
    
    Args:
        code: Generated Python code as string
        
    Returns:
        Tuple[bool, str]: (is_valid, error_message)
    """
    try:
        ast.parse(code)
        return True, "Syntax validation passed"
    except SyntaxError as e:
        return False, f"Syntax error at line {e.lineno}: {e.msg}"
    except Exception as e:
        return False, f"Validation error: {str(e)}"


def test_generated_code(code: str, file_path: str, enable_static_analysis: bool = True, strict_mode: bool = False) -> tuple[bool, str]:
    """
    Enhanced test of generated code with comprehensive validation.
    
    Performs multiple validation layers:
    1. Syntax validation (AST parsing)
    2. Compilation validation (py_compile)  
    3. Static analysis validation (forward references, unused variables)
    
    Args:
        code: Generated Python code
        file_path: Path where the code would be saved
        enable_static_analysis: Whether to perform static analysis (default: True)
        strict_mode: If True, static analysis errors will fail the test (default: False)
        
    Returns:
        Tuple[bool, str]: (success, detailed_message)
    """
    try:
        messages = []
        
        # 1. Syntax validation using AST
        try:
            ast.parse(code)
            messages.append("✅ Syntax validation passed")
        except SyntaxError as e:
            return False, f"❌ Syntax error at line {e.lineno}: {e.msg}"
        
        # 2. Compilation validation using py_compile
        with tempfile.NamedTemporaryFile(mode='w', suffix='.py', delete=False) as temp_file:
            temp_file.write(code)
            temp_file_path = temp_file.name
        
        try:
            result = subprocess.run(
                [sys.executable, '-m', 'py_compile', temp_file_path],
                capture_output=True,
                text=True
            )
            
            if result.returncode == 0:
                messages.append("✅ Compilation validation passed")
            else:
                return False, f"❌ Compilation failed: {result.stderr}"
        finally:
            # Clean up temp file
            Path(temp_file_path).unlink()
        
        # 3. Static analysis validation (if enabled)
        if enable_static_analysis:
            try:
                # Import the static analyzer (adjust path for current location)
                import os
                current_dir = Path(__file__).parent
                parent_dir = current_dir.parent
                sys.path.insert(0, str(parent_dir))
                
                # Try multiple possible locations for the analyzer
                analyzer_imported = False
                try:
                    from beaver_static_analyzer import analyze_code_string
                    analyzer_imported = True
                except ImportError:
                    # Try from parent directory
                    analyzer_path = parent_dir / "beaver_static_analyzer.py"
                    if analyzer_path.exists():
                        import importlib.util
                        spec = importlib.util.spec_from_file_location("beaver_static_analyzer", analyzer_path)
                        analyzer_module = importlib.util.module_from_spec(spec)
                        spec.loader.exec_module(analyzer_module)
                        analyze_code_string = analyzer_module.analyze_code_string
                        analyzer_imported = True
                
                if not analyzer_imported:
                    raise ImportError("Could not import static analyzer")
                
                static_results = analyze_code_string(code)
                
                # Process static analysis results
                error_count = len(static_results.get('errors', []))
                warning_count = len(static_results.get('warnings', []))
                
                if error_count > 0:
                    error_msg = f"❌ Static analysis found {error_count} error(s):\n"
                    for error in static_results['errors'][:3]:  # Show first 3 errors
                        error_msg += f"   • {error}\n"
                    if error_count > 3:
                        error_msg += f"   • ... and {error_count - 3} more errors\n"
                    
                    if strict_mode:
                        return False, error_msg
                    else:
                        messages.append(f"⚠️ Static analysis: {error_count} errors (lenient mode)")
                else:
                    messages.append("✅ Static analysis passed")
                
                if warning_count > 0:
                    messages.append(f"💡 Static analysis: {warning_count} warning(s) found")
                    
            except ImportError:
                messages.append("⚠️ Static analyzer not available - skipping advanced validation")
            except Exception as e:
                messages.append(f"⚠️ Static analysis failed: {str(e)}")
        
        # All validations passed
        summary = "; ".join(messages)
        return True, summary
        
    except Exception as e:
        return False, f"❌ Testing failed: {str(e)}"


def generate_code_with_validation(args):
    """Main function to generate code with comprehensive validation."""
    
    if args.verbose:
        print(f"🚀 Starting Beaver code generation...")
        print(f"📄 Input file: {args.metamodel}")
        print(f"📄 Output file: {args.generated_file_name}")
    
    try:
        # Define processors for DSL parsing
        processors = {
            'Data': data_action,
            'Assignment': assignment_action,
            'Expression': expression_action,
            'Term': term_action,
            'Factor': factor_action,
            'Operand': operand_action,
        }
        
        # Load the DSL grammar
        if args.verbose:
            print("📚 Loading DSL grammar...")
        
        ml_mm = metamodel_from_file('beaver/grammar/pipeline.tx')
        ml_mm.register_obj_processors(processors)
        
        # Parse the DSL configuration file
        if args.verbose:
            print(f"🔍 Parsing configuration file: {args.metamodel}")
        
        config = ml_mm.model_from_file(args.metamodel)
        
        # Perform static validation
        if not args.skip_validation:
            if args.verbose:
                print("🔍 Performing static validation...")
            
            # Use the ModelValidator for validating the Model 
            is_valid, validation_report = validate_beaver_model(config)
            
            print("\n" + validation_report)
            
            if not is_valid:
                print("\n❌ Validation failed! Code generation stopped.")
                if not args.validate_only:
                    print("💡 Use --skip-validation to generate code anyway (not recommended)")
                return False
            else:
                print("\n✅ Static validation passed!")
        
        if args.validate_only:
            print("✅ Validation complete. Exiting as requested.")
            return True
        
        # Load Jinja2 template
        if args.verbose:
            print("🔧 Loading Jinja2 template...")
        
        # Set template loader to look in both current directory and parent
        template_paths = ['.', str(Path(__file__).parent)]
        env = Environment(loader=FileSystemLoader(template_paths))
        template = env.get_template('templates/models.jinja')
        
        # Prepare template data
        # If DSL has feature engineering like:
        # outpout gets populated during parsing:
        flattened_dict = dict_flatten(outpout) if 'outpout' in globals() else {}
        
        # Generate code
        if args.verbose:
            print("⚙️ Generating Python code...")
        
        #  creates Python code using Jinja syntax:  
        generated_code = template.render(
            file=config,
            assignments=flattened_dict
        )
        
        # Validate generated code syntax
        if args.check_syntax:
            if args.verbose:
                print("🔍 Checking generated code syntax...")
            
            syntax_valid, syntax_message = validate_generated_syntax(generated_code)
            
            if not syntax_valid:
                print(f"❌ {syntax_message}")
                return False
            else:
                print(f"✅ {syntax_message}")
        
        # Test code compilation and static analysis
        if args.check_syntax:
            if args.verbose:
                if not args.skip_static_analysis:
                    print("🧪 Testing code with enhanced validation (syntax + compilation + static analysis)...")
                else:
                    print("🧪 Testing code compilation...")
            
            # Use enhanced validation
            compile_success, compile_message = test_generated_code(
                generated_code, 
                args.generated_file_name,
                enable_static_analysis=not args.skip_static_analysis,
                strict_mode=args.strict_analysis
            )
            
            if not compile_success:
                print(f"❌ {compile_message}")
                if args.strict_analysis:
                    print("💡 Use --skip-static-analysis to ignore static analysis errors")
                return False
            else:
                print(f"✅ {compile_message}")
        
        # Output or save the generated code
        if args.dry_run:
            print("\n🔍 DRY RUN - Generated code preview:")
            print("=" * 50)
            print(generated_code[:1000] + "..." if len(generated_code) > 1000 else generated_code)
            print("=" * 50)
            print(f"📊 Total code length: {len(generated_code)} characters")
        else:
            # Save the generated code to a file
            with open(args.generated_file_name, 'w') as f:
                f.write(generated_code)
            
            print(f"✅ Generated code saved to: {args.generated_file_name}")
        
        # Additional statistics
        if args.verbose:
            model_count = len(config.models) if hasattr(config, 'models') and config.models else 0
            data_count = len(config.data) if hasattr(config, 'data') and config.data else 0
            pipeline_count = len(config.pipelines) if hasattr(config, 'pipelines') and config.pipelines else 0
            
            print(f"\n📊 Generation Statistics:")
            print(f"   Models: {model_count}")
            print(f"   Data sources: {data_count}")
            print(f"   Pipelines: {pipeline_count}")
            print(f"   Code lines: {len(generated_code.splitlines())}")
        
        return True
        
    except Exception as e:
        print(f"❌ Error during code generation: {str(e)}")
        if args.verbose:
            import traceback
            traceback.print_exc()
        return False


def main():
    """Main entry point for the enhanced code generator."""
    args = parse_command_line_arguments()
    
    success = generate_code_with_validation(args)
    
    if success:
        print("\n🎉 Process completed successfully!")
        exit_code = 0
    else:
        print("\n💥 Process failed!")
        exit_code = 1
    
    sys.exit(exit_code)


if __name__ == "__main__":
    main()


"""
❓ Why isn't the Analyzer used here?
Different purposes:

gen_enhanced.py: Code generation with validation

Validates input → Generates Python code → Validates output
Focus: "Can I generate working Python code?"
analyzer.py: Analysis and suggestions

Analyzes complexity, best practices, provides improvement suggestions
Focus: "How can I improve my Beaver configuration?"
"""