"""
Model analysis and improvement suggestions for Beaver DSL files.
This script analyzes existing .bvr files and provides recommendations.
"""

import argparse
from pathlib import Path
from textx import metamodel_from_file
from beaver.calc import *
from beaver.validator import ModelValidator, ValidationLevel
import json
import sys


class ModelAnalyzer:
    """Analyzes Beaver model files and provides improvement suggestions."""
    
    def __init__(self):
        self.validator = ModelValidator()
        self.analysis_results = {}
    
    def analyze_file(self, file_path: str) -> dict:
        """
        Analyze a single .bvr file.
        
        Args:
            file_path: Path to the .bvr file
            
        Returns:
            dict: Analysis results
        """
        try:
            # Load grammar and parse file
            processors = {
                'Data': data_action,
                'Assignment': assignment_action,
                'Expression': expression_action,
                'Term': term_action,
                'Factor': factor_action,
                'Operand': operand_action,
            }
            
            ml_mm = metamodel_from_file('beaver/grammar/pipeline.tx')
            ml_mm.register_obj_processors(processors)
            config = ml_mm.model_from_file(file_path)
            
            analysis = {
                'file_path': file_path,
                'status': 'success',
                'models': [],
                'data_sources': [],
                'pipelines': [],
                'validation_issues': [],
                'suggestions': [],
                'metrics': {
                    'total_models': 0,
                    'total_data_sources': 0,
                    'total_pipelines': 0,
                    'complexity_score': 0
                }
            }
            
            # Analyze models
            if hasattr(config, 'models') and config.models:
                analysis['metrics']['total_models'] = len(config.models)
                
                for model in config.models:
                    model_info = self._analyze_model(model)
                    analysis['models'].append(model_info)
                    
                    # Validate model
                    self.validator.clear_issues()
                    self.validator.validate_model(model)
                    
                    for issue in self.validator.issues:
                        analysis['validation_issues'].append({
                            'model': model.name,
                            'level': issue.level.value,
                            'message': issue.message,
                            'suggestion': issue.suggestion
                        })
            
            # Analyze data sources
            if hasattr(config, 'data') and config.data:
                analysis['metrics']['total_data_sources'] = len(config.data)
                
                for data in config.data:
                    data_info = self._analyze_data_source(data)
                    analysis['data_sources'].append(data_info)
            
            # Analyze pipelines
            if hasattr(config, 'pipelines') and config.pipelines:
                analysis['metrics']['total_pipelines'] = len(config.pipelines)
                
                for pipeline in config.pipelines:
                    pipeline_info = self._analyze_pipeline(pipeline)
                    analysis['pipelines'].append(pipeline_info)
            
            # Calculate complexity score
            analysis['metrics']['complexity_score'] = self._calculate_complexity(analysis)
            
            # Generate suggestions
            analysis['suggestions'] = self._generate_suggestions(analysis)
            
            return analysis
            
        except Exception as e:
            return {
                'file_path': file_path,
                'status': 'error',
                'error': str(e),
                'suggestions': [f"Fix parsing error: {str(e)}"]
            }
    
    def _analyze_model(self, model) -> dict:
        """Analyze a single model definition."""
        model_info = {
            'name': getattr(model, 'name', 'unknown'),
            'type': getattr(model.type, '__class__', type(None)).__name__ if hasattr(model, 'type') else 'unknown',
            'model_class': getattr(model.type, 'name', 'unknown') if hasattr(model, 'type') and hasattr(model.type, 'name') else 'unknown',
            'parameter_count': 0,
            'has_parameters': False,
            'parameters': []
        }
        
        if hasattr(model, 'params') and model.params:
            model_info['has_parameters'] = True
            model_info['parameter_count'] = len(model.params)
            
            for param in model.params:
                param_info = {
                    'name': getattr(param, 'name', 'unnamed') if hasattr(param, 'name') else 'unnamed',
                    'type': getattr(param.value, '__class__', type(None)).__name__ if hasattr(param, 'value') else 'unknown'
                }
                model_info['parameters'].append(param_info)
        
        return model_info
    
    def _analyze_data_source(self, data) -> dict:
        """Analyze a data source definition."""
        data_info = {
            'name': getattr(data, 'name', 'unknown'),
            'input_topic': getattr(data, 'input_topic', None),
            'has_features': False,
            'has_preprocessors': False,
            'feature_engineering': False
        }
        
        if hasattr(data, 'features') and data.features:
            data_info['has_features'] = True
            
            if hasattr(data.features, 'assignments') and data.features.assignments:
                data_info['feature_engineering'] = True
        
        if hasattr(data, 'preprocessors') and data.preprocessors:
            data_info['has_preprocessors'] = True
        
        return data_info
    
    def _analyze_pipeline(self, pipeline) -> dict:
        """Analyze a pipeline definition."""
        pipeline_info = {
            'name': getattr(pipeline, 'name', 'unknown'),
            'has_output_topic': hasattr(pipeline, 'output_topic') and getattr(pipeline, 'output_topic', None) is not None,
            'has_data': hasattr(pipeline, 'data') and getattr(pipeline, 'data', None) is not None,
            'has_algorithm': hasattr(pipeline, 'algorithm') and getattr(pipeline, 'algorithm', None) is not None,
            'has_metrics': hasattr(pipeline, 'metrics') and getattr(pipeline, 'metrics', None) is not None
        }
        
        # Add more detailed info if available
        if hasattr(pipeline, 'data') and pipeline.data:
            pipeline_info['data_name'] = getattr(pipeline.data, 'name', 'unknown') if hasattr(pipeline.data, 'name') else str(pipeline.data)
        
        if hasattr(pipeline, 'algorithm') and pipeline.algorithm:
            pipeline_info['algorithm_name'] = getattr(pipeline.algorithm, 'name', 'unknown') if hasattr(pipeline.algorithm, 'name') else str(pipeline.algorithm)
        
        return pipeline_info
    
    def _calculate_complexity(self, analysis: dict) -> int:
        """Calculate a complexity score for the configuration."""
        score = 0
        score += analysis['metrics']['total_models'] * 2
        score += analysis['metrics']['total_data_sources'] * 3
        score += analysis['metrics']['total_pipelines'] * 5
        
        # Add complexity for parameters
        for model in analysis['models']:
            score += model['parameter_count']
        
        # Add complexity for feature engineering
        for data in analysis['data_sources']:
            if data['feature_engineering']:
                score += 3
        
        return score
    
    def _generate_suggestions(self, analysis: dict) -> list:
        """Generate improvement suggestions based on analysis."""
        suggestions = []
        
        # Check for missing components
        if analysis['metrics']['total_models'] == 0:
            suggestions.append("No models defined. Add at least one algorithm model.")
        
        if analysis['metrics']['total_data_sources'] == 0:
            suggestions.append("No data sources defined. Add data sources for your pipelines.")
        
        if analysis['metrics']['total_pipelines'] == 0:
            suggestions.append("No pipelines defined. Add pipeline definitions to connect your components.")
        
        # Check for best practices
        algorithm_models = [m for m in analysis['models'] 
                          if any(x in m['type'].lower() for x in ['classifier', 'regressor', 'clustering'])]
        preprocessing_models = [m for m in analysis['models'] 
                             if 'preprocessing' in m['type'].lower()]
        
        if algorithm_models and not preprocessing_models:
            suggestions.append("Consider adding preprocessing steps for better model performance.")
        
        # Check for parameter usage
        models_without_params = [m for m in analysis['models'] if not m['has_parameters']]
        if len(models_without_params) > len(analysis['models']) / 2:
            suggestions.append("Many models use default parameters. Consider tuning parameters for better performance.")
        
        # Performance suggestions
        if analysis['metrics']['complexity_score'] > 50:
            suggestions.append("High complexity detected. Consider simplifying your configuration for better maintainability.")
        
        if analysis['metrics']['complexity_score'] < 10:
            suggestions.append("Low complexity. You might benefit from adding more sophisticated preprocessing or ensemble methods.")
        
        return suggestions


def analyze_directory(directory: str, output_format: str = 'text'):
    """Analyze all .bvr files in a directory."""
    analyzer = ModelAnalyzer()
    directory_path = Path(directory)
    
    if not directory_path.exists():
        print(f"❌ Directory not found: {directory}")
        return
    
    bvr_files = list(directory_path.glob('*.bvr'))
    
    if not bvr_files:
        print(f"❌ No .bvr files found in {directory}")
        return
    
    print(f"🔍 Analyzing {len(bvr_files)} .bvr files in {directory}...")
    
    all_results = {}
    
    for file_path in bvr_files:
        print(f"📄 Analyzing {file_path.name}...")
        result = analyzer.analyze_file(str(file_path))
        all_results[file_path.name] = result
    
    # Output results
    if output_format == 'json':
        print(json.dumps(all_results, indent=2))
    else:
        print_analysis_report(all_results)


def print_analysis_report(results: dict):
    """Print a formatted analysis report."""
    print("\n" + "="*60)
    print("📊 BEAVER MODEL ANALYSIS REPORT")
    print("="*60)
    
    total_files = len(results)
    successful_analyses = len([r for r in results.values() if r['status'] == 'success'])
    failed_analyses = total_files - successful_analyses
    
    print(f"\n📈 Summary:")
    print(f"   Total files analyzed: {total_files}")
    print(f"   Successful analyses: {successful_analyses}")
    print(f"   Failed analyses: {failed_analyses}")
    
    # Aggregate statistics
    total_models = sum(r.get('metrics', {}).get('total_models', 0) for r in results.values() if r['status'] == 'success')
    total_data_sources = sum(r.get('metrics', {}).get('total_data_sources', 0) for r in results.values() if r['status'] == 'success')
    total_pipelines = sum(r.get('metrics', {}).get('total_pipelines', 0) for r in results.values() if r['status'] == 'success')
    
    print(f"\n🔢 Aggregate Statistics:")
    print(f"   Total models: {total_models}")
    print(f"   Total data sources: {total_data_sources}")
    print(f"   Total pipelines: {total_pipelines}")
    
    # Detailed file analysis
    for filename, result in results.items():
        print(f"\n📄 {filename}")
        print("-" * 40)
        
        if result['status'] == 'error':
            print(f"❌ Error: {result['error']}")
            continue
        
        metrics = result['metrics']
        print(f"   Models: {metrics['total_models']}")
        print(f"   Data sources: {metrics['total_data_sources']}")
        print(f"   Pipelines: {metrics['total_pipelines']}")
        print(f"   Complexity score: {metrics['complexity_score']}")
        
        # Validation issues
        if result['validation_issues']:
            print(f"\n   🔍 Validation Issues:")
            for issue in result['validation_issues']:
                emoji = "❌" if issue['level'] == 'error' else "⚠️" if issue['level'] == 'warning' else "ℹ️"
                print(f"      {emoji} [{issue['model']}] {issue['message']}")
                if issue['suggestion']:
                    print(f"         💡 {issue['suggestion']}")
        
        # Suggestions
        if result['suggestions']:
            print(f"\n   💡 Suggestions:")
            for suggestion in result['suggestions']:
                print(f"      • {suggestion}")


def main():
    """Main entry point for model analysis."""
    parser = argparse.ArgumentParser(description='Analyze Beaver model files')
    parser.add_argument('--directory', '-d', default='examples',
                       help='Directory containing .bvr files to analyze')
    parser.add_argument('--file', '-f', 
                       help='Analyze a specific .bvr file')
    parser.add_argument('--output', '-o', choices=['text', 'json'], default='text',
                       help='Output format')
    parser.add_argument('--verbose', '-v', action='store_true',
                       help='Enable verbose output')
    
    args = parser.parse_args()
    
    if args.file:
        # Analyze single file
        analyzer = ModelAnalyzer()
        result = analyzer.analyze_file(args.file)
        
        if args.output == 'json':
            print(json.dumps({args.file: result}, indent=2))
        else:
            print_analysis_report({args.file: result})
    else:
        # Analyze directory
        analyze_directory(args.directory, args.output)


if __name__ == "__main__":
    main()
