"""
Enhanced code generation with static validation for Beaver DSL.
This script generates Python code from Beaver DSL files and performs comprehensive validation.
"""

import argparse
import ast
import sys
from pathlib import Path
from textx import metamodel_from_file
from jinja2 import Environment, FileSystemLoader
from beaver.calc import *
from beaver.validator import validate_beaver_model, ModelValidator
import subprocess
import tempfile


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
    parser.add_argument('--dry-run', action='store_true',
                       help='Show what would be generated without writing files')
    parser.add_argument('--verbose', '-v', action='store_true',
                       help='Enable verbose output')
    
    return parser.parse_args()


def validate_generated_syntax(code: str) -> tuple[bool, str]:
    """
    Validate the syntax of generated Python code.
    
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


def test_generated_code(code: str, file_path: str) -> tuple[bool, str]:
    """
    Test if the generated code can be imported and basic functionality works.
    
    Args:
        code: Generated Python code
        file_path: Path where the code would be saved
        
    Returns:
        Tuple[bool, str]: (success, message)
    """
    try:
        # Create a temporary file to test imports
        with tempfile.NamedTemporaryFile(mode='w', suffix='.py', delete=False) as temp_file:
            temp_file.write(code)
            temp_file_path = temp_file.name
        
        # Try to compile the file
        result = subprocess.run(
            [sys.executable, '-m', 'py_compile', temp_file_path],
            capture_output=True,
            text=True
        )
        
        # Clean up
        Path(temp_file_path).unlink()
        
        if result.returncode == 0:
            return True, "Code compilation successful"
        else:
            return False, f"Compilation failed: {result.stderr}"
            
    except Exception as e:
        return False, f"Testing failed: {str(e)}"


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
        
        env = Environment(loader=FileSystemLoader('.'))
        template = env.get_template('beaver/templates/models.jinja')
        
        # Prepare template data
        flattened_dict = dict_flatten(outpout) if 'outpout' in globals() else {}
        
        # Generate code
        if args.verbose:
            print("⚙️ Generating Python code...")
        
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
        
        # Test code compilation
        if args.check_syntax:
            if args.verbose:
                print("🧪 Testing code compilation...")
            
            compile_success, compile_message = test_generated_code(generated_code, args.generated_file_name)
            
            if not compile_success:
                print(f"❌ {compile_message}")
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
