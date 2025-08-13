#!/usr/bin/env python3
"""
Enhanced test_generated_code function that includes static analysis.
This could replace or enhance the existing function in gen_enhanced.py
"""

import ast
import py_compile
import tempfile
import os
import subprocess
from typing import Dict, Any, List, Tuple

# Import our static analyzer
from beaver_static_analyzer import analyze_code_string

def enhanced_test_generated_code(code: str, strict: bool = True) -> Dict[str, Any]:
    """
    Enhanced version of test_generated_code with comprehensive validation.
    
    Args:
        code: Generated Python code to test
        strict: If True, static analysis errors will fail the test
        
    Returns:
        Dict with comprehensive test results
    """
    results = {
        'valid': True,
        'syntax_valid': False,
        'compilation_valid': False,
        'static_analysis': {},
        'errors': [],
        'warnings': [],
        'info': []
    }
    
    # 1. Syntax validation using AST
    try:
        ast.parse(code)
        results['syntax_valid'] = True
        results['info'].append("✅ Syntax validation passed")
    except SyntaxError as e:
        results['valid'] = False
        results['syntax_valid'] = False
        results['errors'].append(f"Syntax error at line {e.lineno}: {e.msg}")
        # If syntax is invalid, no point in further testing
        return results
    
    # 2. Compilation validation using py_compile
    try:
        with tempfile.NamedTemporaryFile(mode='w', suffix='.py', delete=False) as f:
            f.write(code)
            temp_file = f.name
        
        try:
            py_compile.compile(temp_file, doraise=True)
            results['compilation_valid'] = True
            results['info'].append("✅ Compilation validation passed")
        finally:
            if os.path.exists(temp_file):
                os.unlink(temp_file)
                
    except py_compile.PyCompileError as e:
        results['valid'] = False
        results['compilation_valid'] = False
        results['errors'].append(f"Compilation error: {e.msg}")
        return results
    
    # 3. Static analysis validation
    static_results = analyze_code_string(code)
    results['static_analysis'] = static_results
    
    # Process static analysis results
    if static_results['errors']:
        if strict:
            results['valid'] = False
            results['errors'].extend([f"Static analysis: {error}" for error in static_results['errors']])
        else:
            results['warnings'].extend([f"Static analysis: {error}" for error in static_results['errors']])
    
    if static_results['warnings']:
        results['warnings'].extend([f"Static analysis: {warning}" for warning in static_results['warnings']])
    
    if static_results['info']:
        results['info'].extend([f"Static analysis: {info}" for info in static_results['info']])
    
    # Summary info
    if results['valid']:
        results['info'].append("✅ All validations passed!")
    else:
        results['info'].append("❌ Validation failed - see errors above")
    
    return results

def print_test_results(results: Dict[str, Any]):
    """Print formatted test results."""
    print(f"\n=== Enhanced Code Validation Results ===")
    print(f"Overall Valid: {results['valid']}")
    print(f"Syntax Valid: {results['syntax_valid']}")
    print(f"Compilation Valid: {results['compilation_valid']}")
    
    if results['errors']:
        print(f"\n❌ ERRORS ({len(results['errors'])}):")
        for error in results['errors']:
            print(f"  {error}")
    
    if results['warnings']:
        print(f"\n⚠️  WARNINGS ({len(results['warnings'])}):")
        for warning in results['warnings']:
            print(f"  {warning}")
    
    if results['info']:
        print(f"\n💡 INFO ({len(results['info'])}):")
        for info in results['info']:
            print(f"  {info}")
    
    if 'statistics' in results['static_analysis']:
        stats = results['static_analysis']['statistics']
        if stats:
            print(f"\n📊 CODE STATISTICS:")
            for key, value in stats.items():
                print(f"  {key.replace('_', ' ').title()}: {value}")

def test_on_file(file_path: str, strict: bool = True):
    """Test validation on an existing Python file."""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            code = f.read()
        
        results = enhanced_test_generated_code(code, strict)
        print(f"\n=== Testing file: {file_path} ===")
        print_test_results(results)
        return results
        
    except FileNotFoundError:
        print(f"Error: File '{file_path}' not found")
        return None
    except Exception as e:
        print(f"Error reading file: {str(e)}")
        return None

if __name__ == "__main__":
    # Test with problematic code
    test_code = """
import numpy as np
from sklearn.svm import OneClassSVM

result = anomaly.predict(data)
svm_model = OneClassSVM()
data = np.array([[1, 2], [3, 4]])
anomaly = svm_model.fit(data)
"""
    
    print("=== Testing problematic code (strict mode) ===")
    results = enhanced_test_generated_code(test_code, strict=True)
    print_test_results(results)
    
    print("\n" + "="*60)
    print("=== Testing problematic code (lenient mode) ===")
    results = enhanced_test_generated_code(test_code, strict=False)
    print_test_results(results)
