"""
Static validation system for Beaver DSL model classes.
This module provides functionality to validate model definitions before code generation.
"""

import inspect
from typing import Dict, List, Set, Any, Optional, Tuple
import importlib
from dataclasses import dataclass
from enum import Enum


class ValidationLevel(Enum):
    ERROR = "error"
    WARNING = "warning"
    INFO = "info"


@dataclass
class ValidationIssue:
    level: ValidationLevel
    message: str
    model_name: str
    line_number: Optional[int] = None
    suggestion: Optional[str] = None


class ModelValidator:
    """Validates model definitions against River library specifications."""
    
    def __init__(self):
        self.issues: List[ValidationIssue] = []
        self.river_modules = self._load_river_modules()
        
    def _load_river_modules(self) -> Dict[str, Any]:
        """Load available River modules and their classes."""
        modules = {}
        # Complete list of actual River modules (verified)
        river_submodules = [
            'linear_model', 'tree', 'ensemble', 'forest', 'cluster', 
            'preprocessing', 'metrics', 'anomaly', 'drift', 'optim',
            'neural_net', 'proba', 'reco', 'bandit', 'model_selection',
            'compose', 'neighbors', 'naive_bayes', 'time_series', 'rules',
            'multiclass', 'multioutput', 'imblearn', 'facto', 'stats',
            'feature_extraction', 'feature_selection', 'misc'
        ]
        
        for module_name in river_submodules:
            try:
                module = importlib.import_module(f'river.{module_name}')
                modules[module_name] = module
            except ImportError as e:
                # Some modules might not be available in all River versions
                print(f"Warning: Could not import river.{module_name}: {e}")
                
        return modules
    
    def validate_model(self, model_def) -> bool:
        """
        Validate a single model definition.
        
        Args:
            model_def: Model definition from parsed DSL
            
        Returns:
            bool: True if validation passes, False otherwise
        """
        model_name = model_def.name
        class_name = model_def.type.__class__.__name__
        type_name = model_def.type.name
        
        # Check if the model class exists in River
        if not self._validate_model_exists(class_name, type_name, model_name):
            return False
            
        # Validate model parameters
        if hasattr(model_def, 'params') and model_def.params:
            self._validate_parameters(model_def.params, class_name, type_name, model_name)
            
        return len([issue for issue in self.issues if issue.level == ValidationLevel.ERROR]) == 0
    
    def _validate_model_exists(self, class_name: str, type_name: str, model_name: str) -> bool:
        """Check if the specified model class exists in River."""
        # Handle special mappings from grammar/models.tx
        custom_import_map = {
            'neuralNetworksActivations': 'neural_net.activations',
            'multioutputMetrics': 'metrics.multioutput',
            'optimizersBase': 'optim.base',
            'optimInitializers': 'optim.initializers',
            'optimLosses': 'optim.losses',
            'optimSchedulers': 'optim.schedulers',
            'probaBase': 'proba.base',
            'recoBase': 'reco.base',
            'treeBase': 'tree.base',
            'treeSplitter': 'tree.splitter',
            'driftBinary': 'drift.binary',
            # Additional mappings for complete coverage
            'naive_bayes': 'naive_bayes',
            'neighbors': 'neighbors', 
            'time_series': 'time_series',
            'multiclass': 'multiclass',
            'multioutput': 'multioutput',
            'feature_extraction': 'feature_extraction',
            'feature_selection': 'feature_selection',
            'FeatureGroup': 'feature_extraction',  # Default for feature groups
        }
        
        mapped_class = custom_import_map.get(class_name, class_name.lower())
        
        # Handle submodule paths (e.g., 'neural_net.activations')
        if '.' in mapped_class:
            module_parts = mapped_class.split('.')
            try:
                # Import the submodule
                import importlib
                full_module_path = f"river.{mapped_class}"
                submodule = importlib.import_module(full_module_path)
                
                # Check if the specific class exists in the submodule
                if not hasattr(submodule, type_name):
                    available_classes = [name for name in dir(submodule) 
                                       if not name.startswith('_') and inspect.isclass(getattr(submodule, name))]
                    self.issues.append(ValidationIssue(
                        level=ValidationLevel.ERROR,
                        message=f"Class '{type_name}' not found in module 'river.{mapped_class}'",
                        model_name=model_name,
                        suggestion=f"Available classes in {mapped_class}: {', '.join(available_classes[:10])}"
                    ))
                    return False
                return True
                
            except ImportError:
                self.issues.append(ValidationIssue(
                    level=ValidationLevel.ERROR,
                    message=f"Module 'river.{mapped_class}' not found",
                    model_name=model_name,
                    suggestion=f"Check if the module path is correct"
                ))
                return False
        
        # Handle regular modules
        if mapped_class not in self.river_modules:
            self.issues.append(ValidationIssue(
                level=ValidationLevel.ERROR,
                message=f"Module '{mapped_class}' not found in River library",
                model_name=model_name,
                suggestion=f"Available modules: {', '.join(sorted(self.river_modules.keys()))}"
            ))
            return False
            
        module = self.river_modules[mapped_class]
        
        # Check if the specific class exists in the module
        if not hasattr(module, type_name):
            available_classes = [name for name in dir(module) 
                               if not name.startswith('_') and inspect.isclass(getattr(module, name))]
            self.issues.append(ValidationIssue(
                level=ValidationLevel.ERROR,
                message=f"Class '{type_name}' not found in module 'river.{mapped_class}'",
                model_name=model_name,
                suggestion=f"Available classes in {mapped_class}: {', '.join(available_classes[:10])}"
            ))
            return False
            
        return True
    
    def _validate_parameters(self, params: List, class_name: str, type_name: str, model_name: str):
        """Validate model parameters against the class signature."""
        try:
            # Get the mapped module name
            custom_import_map = {
                'neuralNetworksActivations': 'neural_net',
                'multioutputMetrics': 'metrics',
                'optimizersBase': 'optim',
                'optimInitializers': 'optim',
                'optimLosses': 'optim',
                'optimSchedulers': 'optim',
                'probaBase': 'proba',
                'recoBase': 'reco',
                'treeBase': 'tree',
                'treeSplitter': 'tree',
                'driftBinary': 'drift'
            }
            
            mapped_class = custom_import_map.get(class_name, class_name.lower())
            module = self.river_modules[mapped_class]
            model_class = getattr(module, type_name)
            
            # Get the __init__ signature
            sig = inspect.signature(model_class.__init__)
            valid_params = set(sig.parameters.keys()) - {'self'}
            
            # Check each parameter
            for param in params:
                param_name = param.name if hasattr(param, 'name') and param.name else None
                
                if param_name and param_name not in valid_params:
                    self.issues.append(ValidationIssue(
                        level=ValidationLevel.ERROR,
                        message=f"Parameter '{param_name}' not valid for {type_name}",
                        model_name=model_name,
                        suggestion=f"Valid parameters: {', '.join(sorted(valid_params))}"
                    ))
                    
                # Validate parameter types
                if param_name and param_name in sig.parameters:
                    self._validate_parameter_type(param, sig.parameters[param_name], model_name)
                    
        except Exception as e:
            self.issues.append(ValidationIssue(
                level=ValidationLevel.WARNING,
                message=f"Could not validate parameters for {type_name}: {str(e)}",
                model_name=model_name
            ))
    
    def _validate_parameter_type(self, param, param_spec, model_name: str):
        """Validate individual parameter types."""
        # This is a simplified type validation
        # In a full implementation, you'd check against the annotation
        param_name = param.name if hasattr(param, 'name') else "unknown"
        
        if hasattr(param, 'value'):
            value = param.value
            
            # Check for common type mismatches
            if hasattr(param_spec, 'annotation'):
                annotation = param_spec.annotation
                
                # Basic type checking
                if annotation == int and hasattr(value, '__class__') and value.__class__.__name__ not in ['int', 'TypeRef']:
                    self.issues.append(ValidationIssue(
                        level=ValidationLevel.WARNING,
                        message=f"Parameter '{param_name}' expects int, got {value.__class__.__name__}",
                        model_name=model_name
                    ))
                elif annotation == float and hasattr(value, '__class__') and value.__class__.__name__ not in ['float', 'int', 'TypeRef']:
                    self.issues.append(ValidationIssue(
                        level=ValidationLevel.WARNING,
                        message=f"Parameter '{param_name}' expects float, got {value.__class__.__name__}",
                        model_name=model_name
                    ))
    
    def validate_model_compatibility(self, models: List) -> bool:
        """Check if models are compatible when used together in pipelines."""
        pipeline_models = []
        
        for model in models:
            class_name = model.type.__class__.__name__
            type_name = model.type.name
            
            # Categorize models based on both class_name and type_name
            class_lower = class_name.lower()
            type_lower = type_name.lower()
            
            # Preprocessing models
            if self._is_preprocessing_model(class_lower, type_lower):
                pipeline_models.append(('preprocessor', model.name, class_name, type_name))
            # Algorithm models (comprehensive list from grammar/models.tx)
            elif self._is_algorithm_model(class_lower, type_lower):
                pipeline_models.append(('algorithm', model.name, class_name, type_name))
            # Metric models
            elif self._is_metric_model(class_lower, type_lower):
                pipeline_models.append(('metric', model.name, class_name, type_name))
            # Optimizer models
            elif self._is_optimizer_model(class_lower, type_lower):
                pipeline_models.append(('optimizer', model.name, class_name, type_name))
        
        # Check for common pipeline issues
        self._check_pipeline_order(pipeline_models)
        
        return len([issue for issue in self.issues if issue.level == ValidationLevel.ERROR]) == 0
    
    def _is_preprocessing_model(self, class_lower: str, type_lower: str) -> bool:
        """Check if model is a preprocessing model."""
        preprocessing_keywords = [
            'preprocessing', 'scaler', 'normalizer', 'imputer', 'encoder', 'binarizer',
            'clipper', 'standardscaler', 'minmaxscaler', 'robustscaler', 'onehotencoder',
            'ordinalencoder', 'featurehasher', 'gaussianrandomprojector', 'lda'
        ]
        
        return any(x in class_lower for x in ['preprocessing']) or \
               any(x in type_lower for x in preprocessing_keywords)
    
    def _is_algorithm_model(self, class_lower: str, type_lower: str) -> bool:
        """Check if model is an algorithm model based on grammar/models.tx."""
        # Algorithm categories from grammar/models.tx
        algorithm_categories = {
            'anomaly': [
                'gaussianscorer', 'halfspacetrees', 'localoutlierfactor', 'oneclasssvm',
                'predictiveanomalydetection', 'quantilefilter', 'standardabsolutedeviation',
                'thresholdfilter'
            ],
            'linear_model': [
                'almaclassifier', 'bayesianlinearregression', 'linearregression',
                'logisticregression', 'paclassifier', 'paregressor', 'perceptron',
                'softmaxregression'
            ],
            'forest': [
                'amfclassifier', 'amfregressor', 'arfclassifier', 'arfregressor', 'oxtregressor'
            ],
            'cluster': [
                'clustream', 'dbstream', 'denstream', 'kmeans', 'odac', 'streamkmeans', 'textclust'
            ],
            'drift': [
                'adwin', 'driftretrainingclassifier', 'dummydriftdetector', 'kswin',
                'nodrift', 'pagehinkley'
            ],
            'drift_binary': [
                'ddm', 'eddm', 'fhddm', 'hddm_a', 'hddm_w'
            ],
            'ensemble': [
                'adwinbaggingclassifier', 'adwinboostingclassifier', 'adaboostclassifier',
                'boleclassifier', 'baggingclassifier', 'baggingregressor', 'ewaregressor',
                'leveragingbaggingclassifier', 'srpclassifier', 'srpregressor',
                'stackingclassifier', 'votingclassifier'
            ],
            'facto': [
                'ffmclassifier', 'ffmregressor', 'fmclassifier', 'fmregressor',
                'fwfmclassifier', 'fwfmregressor', 'hofmclassifier', 'hofmregressor'
            ],
            'imblearn': [
                'chebyshevoversampler', 'chebyshevundersampler', 'hardsamplingclassifier',
                'hardsamplingregressor', 'randomoversampler', 'randomsampler', 'randomundersampler'
            ],
            'multiclass': [
                'onevseoneclassifier', 'onevsrestclassifier', 'outputcodeclassifier'
            ],
            'multioutput': [
                'classifierchain', 'montecarloclassifierchain', 'multiclassencoder',
                'probabilisticclassifierchain', 'regressorchain'
            ],
            'model_selection': [
                'banditclassifier', 'banditregressor', 'greedyregressor',
                'successiveharvingclassifier', 'successiveharvingregressor'
            ],
            'bandit': [
                'bayesucb', 'epsilongreedy', 'exp3', 'linucbdisjoint', 'randompolicy',
                'thompsonsampling', 'ucb'
            ],
            'naive_bayes': [
                'bernoullinb', 'complementnb', 'gaussiannb', 'multinomialnb'
            ],
            'neighbors': [
                'knnclassifier', 'knnregressor', 'lazysearch', 'swinn'
            ],
            'neural_net': [
                'mlpregressor'
            ],
            'rules': [
                'amrules'
            ],
            'time_series': [
                'holtwinters', 'snarimax'
            ],
            'tree': [
                'extremelyfastdecisiontreeclassifier', 'hoeffdingadaptivetreeclassifier',
                'hoeffdingadaptivetreeregressor', 'hoeffdingtreeclassifier',
                'hoeffdingtreeregressor', 'lastclassifier', 'sgtclassifier',
                'sgtregressor', 'isouptreeregressor'
            ]
        }
        
        # Check if it's in any algorithm category
        all_algorithms = []
        for category_algorithms in algorithm_categories.values():
            all_algorithms.extend(category_algorithms)
        
        # Check class name patterns
        algorithm_class_patterns = [
            'linear_model', 'forest', 'cluster', 'drift', 'ensemble', 'facto',
            'imblearn', 'multiclass', 'multioutput', 'model_selection', 'bandit',
            'naive_bayes', 'neighbors', 'neural_net', 'rules', 'time_series', 'tree',
            'anomaly'
        ]
        
        return any(x in class_lower for x in algorithm_class_patterns) or \
               any(x in type_lower for x in all_algorithms)
    
    def _is_metric_model(self, class_lower: str, type_lower: str) -> bool:
        """Check if model is a metric model."""
        metric_keywords = [
            'accuracy', 'adjustedmutualinfo', 'adjustedrand', 'balancedaccuracy',
            'classificationreport', 'cohenkappa', 'completeness', 'confusionmatrix',
            'crossentropy', 'f1', 'fbeta', 'fowlkesmallows', 'geometricmean',
            'homogeneity', 'jaccard', 'logloss', 'mae', 'mape', 'mcc', 'mse',
            'macrof1', 'macrofbeta', 'macrojaccard', 'macroprecision', 'macrorecall',
            'microf1', 'microfbeta', 'microjaccard', 'microprecision', 'microrecall',
            'multifbeta', 'mutualinfo', 'normalizedmutualinfo', 'precision', 'r2',
            'rmse', 'rmsle', 'rocauc', 'rand', 'recall', 'rollingrocauc', 'smape',
            'silhouette', 'vbeta', 'weightedf1', 'weightedfbeta', 'weightedjaccard',
            'weightedprecision', 'weightedrecall'
        ]
        
        return 'metrics' in class_lower or any(x in type_lower for x in metric_keywords)
    
    def _is_optimizer_model(self, class_lower: str, type_lower: str) -> bool:
        """Check if model is an optimizer model."""
        optimizer_keywords = [
            'amsgrad', 'adabound', 'adadelta', 'adagrad', 'adamax', 'adam',
            'averager', 'ftrlproximal', 'momentum', 'nadam', 'nesterovmomentum',
            'rmsprop', 'sgd', 'constant', 'normal', 'zeros'
        ]
        
        return 'optim' in class_lower or any(x in type_lower for x in optimizer_keywords)
    
    def _check_pipeline_order(self, pipeline_models: List[Tuple[str, str, str, str]]):
        """Check if pipeline model order makes sense."""
        has_preprocessor = any(model_type == 'preprocessor' for model_type, _, _, _ in pipeline_models)
        has_algorithm = any(model_type == 'algorithm' for model_type, _, _, _ in pipeline_models)
        
        if not has_algorithm:
            self.issues.append(ValidationIssue(
                level=ValidationLevel.WARNING,
                message="No algorithm model found in pipeline",
                model_name="pipeline",
                suggestion="Add at least one classifier, regressor, or clustering algorithm"
            ))
    
    def get_validation_report(self) -> str:
        """Generate a formatted validation report."""
        if not self.issues:
            return "✅ All models validated successfully!"
        
        report = []
        report.append("🔍 Model Validation Report")
        report.append("=" * 50)
        
        errors = [issue for issue in self.issues if issue.level == ValidationLevel.ERROR]
        warnings = [issue for issue in self.issues if issue.level == ValidationLevel.WARNING]
        infos = [issue for issue in self.issues if issue.level == ValidationLevel.INFO]
        
        if errors:
            report.append(f"\n❌ ERRORS ({len(errors)}):")
            for issue in errors:
                report.append(f"  • [{issue.model_name}] {issue.message}")
                if issue.suggestion:
                    report.append(f"    💡 {issue.suggestion}")
        
        if warnings:
            report.append(f"\n⚠️  WARNINGS ({len(warnings)}):")
            for issue in warnings:
                report.append(f"  • [{issue.model_name}] {issue.message}")
                if issue.suggestion:
                    report.append(f"    💡 {issue.suggestion}")
        
        if infos:
            report.append(f"\nℹ️  INFO ({len(infos)}):")
            for issue in infos:
                report.append(f"  • [{issue.model_name}] {issue.message}")
        
        return "\n".join(report)
    
    def clear_issues(self):
        """Clear all validation issues."""
        self.issues.clear()


def validate_beaver_model(config) -> Tuple[bool, str]:
    """
    Main validation function for Beaver model configurations.
    
    Args:
        config: Parsed DSL configuration
        
    Returns:
        Tuple[bool, str]: (is_valid, validation_report)
    """
    validator = ModelValidator()
    
    if not hasattr(config, 'models') or not config.models:
        return True, "No models to validate."
    
    all_valid = True
    
    # Validate individual models
    for model in config.models:
        if not validator.validate_model(model):
            all_valid = False
    
    # Validate model compatibility
    if not validator.validate_model_compatibility(config.models):
        all_valid = False
    
    report = validator.get_validation_report()
    return all_valid, report
