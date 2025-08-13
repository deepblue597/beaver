#!/usr/bin/env python3
"""
Beaver Static Code Analyzer
Enhanced static analysis for generated Python code.
"""

import ast
from typing import Dict, Any, List

def analyze_code_string(code: str) -> Dict[str, Any]:
    """
    Analyze Python code string for static issues.
    
    Args:
        code: Python code as string
        
    Returns:
        Analysis results dictionary
    """
    try:
        # Parse the code into AST
        tree = ast.parse(code)
        
        # Track variables
        defined_vars = set()
        used_vars = {}  # var_name: [line_numbers]
        errors = []
        warnings = []
        
        # Built-in names that don't need definition
        builtins = {
            'len', 'str', 'int', 'float', 'list', 'dict', 'set', 'tuple',
            'range', 'enumerate', 'zip', 'map', 'filter', 'sum', 'max', 'min',
            'abs', 'round', 'print', 'input', 'open', 'type', 'isinstance',
            'hasattr', 'getattr', 'setattr', 'delattr', '__name__', '__main__'
        }
        
        class VariableTracker(ast.NodeVisitor):
            def visit_Import(self, node):
                for alias in node.names:
                    name = alias.asname if alias.asname else alias.name.split('.')[0]
                    defined_vars.add(name)
            
            def visit_ImportFrom(self, node):
                for alias in node.names:
                    name = alias.asname if alias.asname else alias.name
                    defined_vars.add(name)
            
            def visit_FunctionDef(self, node):
                defined_vars.add(node.name)
                # Don't visit function body for now (to avoid complexity)
            
            def visit_Assign(self, node):
                for target in node.targets:
                    if isinstance(target, ast.Name):
                        defined_vars.add(target.id)
                
                # Visit the right-hand side to track usage
                self.visit(node.value)
            
            def visit_Name(self, node):
                if isinstance(node.ctx, ast.Load):
                    if node.id not in used_vars:
                        used_vars[node.id] = []
                    used_vars[node.id].append(node.lineno)
        
        # Analyze the code
        tracker = VariableTracker()
        tracker.visit(tree)
        
        # Check for forward references
        assigned_vars = {}
        for node in ast.walk(tree):
            if isinstance(node, ast.Assign):
                for target in node.targets:
                    if isinstance(target, ast.Name):
                        assigned_vars[target.id] = node.lineno
        
        # Find forward reference errors
        for var_name, usage_lines in used_vars.items():
            if var_name in assigned_vars:
                definition_line = assigned_vars[var_name]
                for usage_line in usage_lines:
                    if usage_line < definition_line:
                        errors.append(
                            f"Line {usage_line}: Variable '{var_name}' used before definition at line {definition_line}"
                        )
            elif (var_name not in defined_vars and 
                  var_name not in builtins and 
                  not var_name.startswith('_')):
                for usage_line in usage_lines:
                    errors.append(
                        f"Line {usage_line}: Variable '{var_name}' used before definition"
                    )
        
        # Check for unused variables (simple version)
        framework_imports = {
            'Dash', 'Input', 'Output', 'dcc', 'html', 'go', 'make_subplots',
            'threading', 'ConnectionConfig', 'Application', 'Pipeline'
        }
        
        for var_name, definition_line in assigned_vars.items():
            if (var_name not in used_vars and 
                not var_name.startswith('_') and
                var_name not in framework_imports):
                warnings.append(
                    f"Line {definition_line}: Variable '{var_name}' is assigned but never used"
                )
        
        return {
            'valid': len(errors) == 0,
            'errors': errors,
            'warnings': warnings,
            'info': [],
            'statistics': {
                'total_variables': len(assigned_vars),
                'lines_of_code': len(code.split('\n'))
            }
        }
        
    except SyntaxError as e:
        return {
            'valid': False,
            'errors': [f"Syntax error at line {e.lineno}: {e.msg}"],
            'warnings': [],
            'info': [],
            'statistics': {}
        }
    except Exception as e:
        return {
            'valid': False,
            'errors': [f"Analysis error: {str(e)}"],
            'warnings': [],
            'info': [],
            'statistics': {}
        }


if __name__ == "__main__":
    # Test the analyzer
    test_code = """
result = svm.predict(data)
svm = OneClassSVM()
data = [1, 2, 3]
"""
    results = analyze_code_string(test_code)
    print(f"Valid: {results['valid']}")
    for error in results['errors']:
        print(f"Error: {error}")
    for warning in results['warnings']:
        print(f"Warning: {warning}")
