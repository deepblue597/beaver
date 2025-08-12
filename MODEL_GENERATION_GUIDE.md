# 🦫 Beaver Model Generation and Validation Guide

This guide explains how to generate model classes and perform static validation in the Beaver project.

## 🚀 Quick Start

### 1. Generate Code with Validation

```bash
# Basic code generation with validation
python beaver_cli.py generate --input examples/model.bvr

# Generate with comprehensive checking
python beaver_cli.py generate --input examples/model.bvr --check-syntax --verbose

# Preview what will be generated
python beaver_cli.py generate --input examples/model.bvr --dry-run
```

### 2. Validate Models Only

```bash
# Validate without generating code
python beaver_cli.py validate --input examples/model.bvr

# Verbose validation with detailed feedback
python beaver_cli.py validate --input examples/model.bvr --verbose
```

### 3. Analyze Model Files

```bash
# Analyze all examples
python beaver_cli.py analyze --directory examples

# Analyze specific file
python beaver_cli.py analyze --input examples/model.bvr

# Get JSON output for programmatic use
python beaver_cli.py analyze --directory examples --output json
```

## 📋 Available Tools

### 1. Enhanced Code Generator (`beaver/gen_enhanced.py`)

**Features:**

- ✅ Static validation before code generation
- ✅ Syntax checking of generated code
- ✅ Compilation testing
- ✅ Dry-run mode for previewing
- ✅ Verbose logging
- ✅ Comprehensive error reporting

**Usage:**

```bash
python beaver/gen_enhanced.py --metamodel examples/model.bvr --generated_file_name output.py --check-syntax --verbose
```

**Options:**

- `--validate-only`: Only perform validation, skip code generation
- `--skip-validation`: Skip static validation (not recommended)
- `--check-syntax`: Validate Python syntax of generated code
- `--dry-run`: Show preview without creating files
- `--verbose`: Enable detailed output

### 2. Model Validator (`beaver/validator.py`)

**Features:**

- ✅ Validates model classes exist in River library
- ✅ Checks parameter compatibility
- ✅ Validates model combinations in pipelines
- ✅ Provides improvement suggestions
- ✅ Categorizes issues by severity (Error/Warning/Info)

**Validation Categories:**

- **Model Existence**: Checks if River classes are available
- **Parameter Validation**: Verifies parameter names and types
- **Pipeline Compatibility**: Ensures models work together
- **Best Practices**: Suggests improvements

### 3. Model Analyzer (`beaver/analyzer.py`)

**Features:**

- ✅ Analyzes complexity of model configurations
- ✅ Provides improvement suggestions
- ✅ Generates detailed reports
- ✅ Supports batch analysis of multiple files
- ✅ JSON output for integration

**Metrics Tracked:**

- Model count and types
- Data source complexity
- Pipeline structure
- Parameter usage
- Feature engineering complexity

### 4. Unified CLI (`beaver_cli.py`)

**Features:**

- ✅ Single entry point for all operations
- ✅ Consistent command structure
- ✅ Built-in help and examples
- ✅ Error handling and user feedback

## 🔍 Validation Examples

### Model Class Validation

The validator checks that your models are properly defined:

```yaml
# ✅ GOOD: Valid River model
algorithm <ALMAClassifier> alma_model
    params:
        lr = 0.1

# ❌ BAD: Non-existent class
algorithm <NonExistentClassifier> bad_model
    params:
        invalid_param = 1
```

### Parameter Validation

Parameters are validated against River documentation:

```yaml
# ✅ GOOD: Valid parameters
algorithm <KMeans> clustering_model
    params:
        n_clusters = 5
        halflife = 0.5

# ❌ BAD: Invalid parameter
algorithm <KMeans> bad_clustering
    params:
        wrong_parameter = 5
```

### Pipeline Validation

The system checks pipeline compatibility:

```yaml
# ✅ GOOD: Complete pipeline
preprocessor <StandardScaler> scaler
algorithm <LogisticRegression> classifier
metric <Accuracy> accuracy_metric

# ⚠️ WARNING: Missing preprocessor
algorithm <LogisticRegression> classifier_only
```

## 📊 Understanding Validation Reports

### Error Levels

1. **❌ ERROR**: Must be fixed before code generation

   - Non-existent model classes
   - Invalid parameter names
   - Critical syntax issues

2. **⚠️ WARNING**: Should be reviewed but won't block generation

   - Parameter type mismatches
   - Missing preprocessing steps
   - Suboptimal configurations

3. **ℹ️ INFO**: Suggestions for improvement
   - Performance optimizations
   - Best practice recommendations
   - Code quality improvements

### Sample Validation Report

```
🔍 Model Validation Report
==================================================

❌ ERRORS (1):
  • [model2] Parameter 'wrong_param' not valid for ALMAClassifier
    💡 Valid parameters: lr, alpha, B, C

⚠️ WARNINGS (2):
  • [model3] Parameter 'lr' expects float, got str
  • [pipeline] No preprocessing steps found
    💡 Consider adding StandardScaler or other preprocessors

ℹ️ INFO (1):
  • [model4] Using default parameters
    💡 Consider tuning parameters for better performance
```

## 🛠️ Advanced Usage

### Custom Validation Rules

You can extend the validator with custom rules:

```python
from beaver.validator import ModelValidator, ValidationIssue, ValidationLevel

class CustomValidator(ModelValidator):
    def validate_custom_rule(self, model):
        # Add your custom validation logic
        if model.name.startswith('test_'):
            self.issues.append(ValidationIssue(
                level=ValidationLevel.WARNING,
                message="Model name suggests this is a test model",
                model_name=model.name,
                suggestion="Use descriptive model names in production"
            ))
```

### Batch Processing

Process multiple files programmatically:

```python
from beaver.analyzer import ModelAnalyzer
from pathlib import Path

analyzer = ModelAnalyzer()
results = {}

for file_path in Path('examples').glob('*.bvr'):
    results[file_path.name] = analyzer.analyze_file(str(file_path))

# Generate summary report
for filename, result in results.items():
    if result['status'] == 'success':
        print(f"{filename}: {result['metrics']['complexity_score']} complexity")
```

### Integration with CI/CD

Add validation to your CI pipeline:

```yaml
# .github/workflows/validate-models.yml
name: Validate Beaver Models
on: [push, pull_request]

jobs:
  validate:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - name: Setup Python
        uses: actions/setup-python@v2
        with:
          python-version: "3.9"
      - name: Install dependencies
        run: pip install -r requirements.txt
      - name: Validate models
        run: |
          for file in examples/*.bvr; do
            python beaver_cli.py validate --input "$file" --verbose
          done
```

## 🐛 Troubleshooting

### Common Issues

1. **"Module not found" errors**

   - Ensure River is installed: `pip install river`
   - Check for typos in model class names

2. **"Parameter not valid" errors**

   - Check River documentation for correct parameter names
   - Verify parameter types match expected values

3. **Generation fails after validation passes**
   - Check template syntax in Jinja files
   - Verify all referenced models are defined

### Getting Help

1. **Verbose Mode**: Add `--verbose` to any command for detailed output
2. **Dry Run**: Use `--dry-run` to preview without making changes
3. **Check Examples**: Run `python beaver_cli.py examples` to see available examples
4. **Extended Help**: Run `python beaver_cli.py help` for comprehensive guidance

## 📈 Best Practices

### Model Definition

1. **Use Descriptive Names**: `fraud_detector` instead of `model1`
2. **Include Parameters**: Don't rely only on defaults
3. **Add Preprocessing**: Most models benefit from data preprocessing
4. **Define Metrics**: Always include appropriate evaluation metrics

### Validation Workflow

1. **Validate Early**: Run validation before complex configurations
2. **Fix Errors First**: Address all errors before warnings
3. **Test Generated Code**: Use `--check-syntax` to catch issues early
4. **Review Suggestions**: Consider warnings and info messages

### Development Cycle

1. **Start Simple**: Begin with basic models and add complexity gradually
2. **Validate Frequently**: Run validation after each change
3. **Use Analysis**: Regularly analyze your configurations for improvements
4. **Document Changes**: Keep track of model parameter tuning

## 🔗 Related Files

- `beaver/validator.py`: Core validation logic
- `beaver/gen_enhanced.py`: Enhanced code generator
- `beaver/analyzer.py`: Model analysis and suggestions
- `beaver_cli.py`: Unified command-line interface
- `beaver/templates/models_macros.jinja`: Updated Jinja templates
- `examples/`: Sample .bvr files for testing
