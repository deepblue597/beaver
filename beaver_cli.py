"""
Beaver CLI - Command-line interface for Beaver DSL operations.
This provides a unified interface for generating, validating, and analyzing Beaver models.
"""

import argparse
import sys
from pathlib import Path
import subprocess


def run_generator(args):
    """Run the enhanced code generator."""
    cmd = [
        sys.executable, 
        'beaver/gen_enhanced.py',
        '--metamodel', args.input,
        '--generated_file_name', args.output
    ]
    
    # Add optional arguments based on user input
    if args.validate_only:
        cmd.append('--validate-only')
    if args.skip_validation:
        cmd.append('--skip-validation')
    if args.check_syntax:
        cmd.append('--check-syntax')
    if args.dry_run:
        cmd.append('--dry-run')
    if args.verbose:
        cmd.append('--verbose')
    
    # Run the command and return the result
    return subprocess.run(cmd)


def run_analyzer(args):
    """Run the model analyzer."""
    cmd = [sys.executable, 'beaver/analyzer.py']
    
    if args.input:
        cmd.extend(['--file', args.input])
    elif args.directory:
        cmd.extend(['--directory', args.directory])
    else:
        cmd.extend(['--directory', 'examples'])
    
    if args.output_format:
        cmd.extend(['--output', args.output_format])
    if args.verbose:
        cmd.append('--verbose')
    
    return subprocess.run(cmd)


def run_validator(args):
    """Run standalone validation."""
    cmd = [
        sys.executable,
        'beaver/gen_enhanced.py',
        '--metamodel', args.input,
        '--validate-only'
    ]
    
    if args.verbose:
        cmd.append('--verbose')
    
    return subprocess.run(cmd)


def list_examples():
    """List available example files."""
    examples_dir = Path('examples')
    
    if not examples_dir.exists():
        print("❌ Examples directory not found")
        return
    
    bvr_files = list(examples_dir.glob('*.bvr'))
    
    if not bvr_files:
        print("❌ No .bvr example files found")
        return
    
    print("📚 Available example files:")
    for file_path in sorted(bvr_files):
        print(f"   • {file_path.name}")
    
    print(f"\n💡 Use: beaver generate --input examples/<filename>")


def show_help():
    """Show extended help information."""
    help_text = """
🦫 Beaver CLI - Machine Learning Pipeline Generator

QUICK START:
   python beaver_cli.py generate --input examples/model.bvr          # Generate code from example
   python beaver_cli.py validate --input examples/model.bvr          # Validate model definitions
   python beaver_cli.py analyze --directory examples                 # Analyze all examples

WORKFLOWS:
   1. Validation-first workflow:
      python beaver_cli.py validate --input mymodel.bvr
      python beaver_cli.py generate --input mymodel.bvr --check-syntax
   
   2. Analysis and improvement:
      python beaver_cli.py analyze --input mymodel.bvr
      # Make improvements based on suggestions
      python beaver_cli.py generate --input mymodel.bvr
   
   3. Safe generation:
      python beaver_cli.py generate --input mymodel.bvr --dry-run --verbose
      python beaver_cli.py generate --input mymodel.bvr --output model.py --check-syntax

EXAMPLES:
   # Generate with full validation and syntax checking
   python beaver_cli.py generate --input examples/model.bvr --output model.py --check-syntax --verbose
   
   # Validate only (no code generation)
   python beaver_cli.py validate --input examples/linear.bvr --verbose
   
   # Analyze all examples and get JSON output
   python beaver_cli.py analyze --directory examples --output json
   
   # Quick test run without writing files
   python beaver_cli.py generate --input examples/model.bvr --dry-run

MORE INFO:
   Each command supports --help for detailed options
   Example: python beaver_cli.py generate --help
    """
    print(help_text)


def main():
    """Main CLI entry point."""
    parser = argparse.ArgumentParser(
        description='Beaver CLI - Machine Learning Pipeline Generator',
        formatter_class=argparse.RawDescriptionHelpFormatter
    )
    
    subparsers = parser.add_subparsers(dest='command', help='Available commands')
    
    # Generate command
    gen_parser = subparsers.add_parser('generate', help='Generate Python code from Beaver DSL')
    gen_parser.add_argument('--input', '-i', required=True, help='Input .bvr file')
    gen_parser.add_argument('--output', '-o', default='generated_pipeline.py', help='Output Python file')
    gen_parser.add_argument('--validate-only', action='store_true', help='Only validate, don\'t generate')
    gen_parser.add_argument('--skip-validation', action='store_true', help='Skip validation')
    gen_parser.add_argument('--check-syntax', action='store_true', help='Check generated code syntax')
    gen_parser.add_argument('--dry-run', action='store_true', help='Show preview without writing files')
    gen_parser.add_argument('--verbose', '-v', action='store_true', help='Verbose output')
    
    # Validate command
    val_parser = subparsers.add_parser('validate', help='Validate Beaver DSL file')
    val_parser.add_argument('--input', '-i', required=True, help='Input .bvr file to validate')
    val_parser.add_argument('--verbose', '-v', action='store_true', help='Verbose output')
    
    # Analyze command
    ana_parser = subparsers.add_parser('analyze', help='Analyze Beaver DSL files')
    ana_parser.add_argument('--input', '-i', help='Analyze specific .bvr file')
    ana_parser.add_argument('--directory', '-d', help='Analyze all .bvr files in directory')
    ana_parser.add_argument('--output-format', choices=['text', 'json'], default='text', help='Output format')
    ana_parser.add_argument('--verbose', '-v', action='store_true', help='Verbose output')
    
    # Examples command
    subparsers.add_parser('examples', help='List available example files')
    
    # Help command
    subparsers.add_parser('help', help='Show extended help and examples')
    
    args = parser.parse_args()
    
    if not args.command:
        parser.print_help()
        return
    
    try:
        if args.command == 'generate':
            result = run_generator(args)
        elif args.command == 'validate':
            result = run_validator(args)
        elif args.command == 'analyze':
            result = run_analyzer(args)
        elif args.command == 'examples':
            list_examples()
            return
        elif args.command == 'help':
            show_help()
            return
        else:
            parser.print_help()
            return
        
        # Exit with the same code as the subprocess
        if hasattr(result, 'returncode'):
            sys.exit(result.returncode)
            
    except KeyboardInterrupt:
        print("\n🛑 Operation cancelled by user")
        sys.exit(1)
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        sys.exit(1)


if __name__ == "__main__":
    main()
