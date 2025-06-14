from setuptools import setup, find_packages


with open("requirements.txt") as f:
    requirements = [line.strip() for line in f if line.strip() and not line.startswith("#")]


setup(
    name='beaver',
    version='1.0.0',
    packages=find_packages(),  # Automatically find packages in subdirectories
    install_requires=requirements,
    author='Iasonas Kakandris',
    description='Beaver is a DSL for machine learning in live data',
    package_data={
        "beaver": [
            "grammar/*.tx",
            "templates/*.jinja",
        ],
    },
    install_requires=[
        "textx",
        "jinja2",

    ],
)
