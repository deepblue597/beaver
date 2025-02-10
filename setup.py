from setuptools import setup, find_packages

with open('requirements.txt') as f:
    requirements = f.read().splitlines()

setup(
    name='thesis',
    version='0.1',
    packages=find_packages(),  # Automatically find packages in subdirectories
    install_requires=requirements,
    author='Iasonas Kakandris',
    description='A project integrating Kafka, Quix Streams, River, and TextX',
)
