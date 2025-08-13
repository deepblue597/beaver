import ast
from typing import Set, List, Tuple

def check_forward_references(code: str) -> Tuple[bool, List[str]]:
    """
    Check for forward references and undefined variables using AST analysis.
    
    Args:
        code: Python code as string
        
    Returns:
        Tuple[bool, List[str]]: (is_valid, list_of_errors)
    """
    try:
        tree = ast.parse(code)
        
        defined_vars = set()
        imported_modules = set()
        errors = []
        
        class VariableChecker(ast.NodeVisitor):
            def __init__(self):
                self.current_line = 0
            
            def visit_Import(self, node):
                # Track imported modules
                for alias in node.names:
                    imported_modules.add(alias.name.split('.')[0])
                    if alias.asname:
                        defined_vars.add(alias.asname)
                    else:
                        defined_vars.add(alias.name.split('.')[0])
            
            def visit_ImportFrom(self, node):
                # Track from imports
                if node.module:
                    imported_modules.add(node.module.split('.')[0])
                for alias in node.names:
                    if alias.asname:
                        defined_vars.add(alias.asname)
                    else:
                        defined_vars.add(alias.name)
            
            def visit_Assign(self, node):
                # Track variable definitions
                self.current_line = node.lineno
                for target in node.targets:
                    if isinstance(target, ast.Name):
                        defined_vars.add(target.id)
                
                # Check right-hand side for usage
                self.visit(node.value)
            
            def visit_Name(self, node):
                if isinstance(node.ctx, ast.Load):  # Variable is being used
                    self.current_line = node.lineno
                    if (node.id not in defined_vars and 
                        node.id not in imported_modules and 
                        not node.id.startswith('__')):  # Ignore built-ins like __name__
                        errors.append(f"Line {node.lineno}: Variable '{node.id}' used before definition")
        
        checker = VariableChecker()
        checker.visit(tree)
        
        return len(errors) == 0, errors
        
    except SyntaxError as e:
        return False, [f"Syntax error: {e.msg}"]
    except Exception as e:
        return False, [f"Analysis error: {str(e)}"]

# Test it
if __name__ == "__main__":
    # Test code with forward reference
    test_code = """
quantile = anomaly.QuantileFilter(
    anomaly_detector=svm,
    q=0.995
)
svm = anomaly.OneClassSVM(
    nu=0.2
)
"""
    
    is_valid, errors = check_forward_references(test_code)
    print(f"Valid: {is_valid}")
    for error in errors:
        print(f"Error: {error}")
