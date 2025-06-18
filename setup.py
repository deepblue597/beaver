from setuptools import setup

setup(
    name='beaver',
    version='1.0.0',
    packages=['beaver'],  # Automatically find packages in subdirectories
    author='Iasonas Kakandris',
    description='Beaver is a DSL for machine learning in live data',
    author_email = 'ikakandris@gmail.com' , 
    install_requires=[
        "textx",        # For DSL parsing
        "jinja2",       # For templating
        "river",        # For online machine learning
        "quixstreams",  # For streaming/Kafka integration
        "plotly",       # For plotting/visualization
        "dash",         # For dashboards
        "numpy",        # For numerical operations
        "pandas",       # For data manipulation (if used)
        "scikit-learn", # For metrics or models (if used)
        "dill",         # For object serialization
        "matplotlib",   # For plotting (pyplot, animation)
        "kagglehub", 
        "sseclient",
        "flatten_dict"


    ],
)
