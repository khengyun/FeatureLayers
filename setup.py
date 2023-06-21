import setuptools
from setuptools import setup, find_packages

setup(
    name='featurelayers',
    version='1.0.0',
    description='FeatureLayers Package',
    author='khengyun',
    author_email='khaangnguyeen@email.com',
    packages=find_packages(),
    install_requires=[
        'numpy',
        'scipy',
        'tensorflow',
        'keras',
        'scipy',
    ])
