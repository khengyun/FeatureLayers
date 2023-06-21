from setuptools import setup, find_packages

setup(
    name='featurelayers',
    description='featurelayers Package',
    author='khengyun',
    author_email='khaangnguyeen@email.com',
    packages=find_packages(include=['featurelayers', 'featurelayers.layers']),
    install_requires=[
        'numpy',
        'scipy',
        'tensorflow',
        'keras',
        'scipy',
    ],
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Education",
        "Programming Language :: Python :: 3",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
    ],
    use_scm_version={
        'version_scheme': 'guess-next-dev',
        'local_scheme': 'no-local-version',
    },
    setup_requires=['setuptools_scm'],
)