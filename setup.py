from setuptools import setup, find_packages
import setuptools_scm


setup(
    name='featurelayers',
    description='featurelayers Package',
    author='khengyun',
    author_email='khaangnguyeen@gmail.com',
    packages=find_packages(include=['featurelayers', 'featurelayers.layers']),
    install_requires=[
        'numpy',
        'scipy',
        'tensorflow',
        'keras',
        'scipy',
        'setuptools_scm',
    ],
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Education",
        "Programming Language :: Python :: 3",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
    ],
    use_scm_version={
        'version_scheme': 'post-release',
        'local_scheme': 'node-and-date',
        'write_to': 'featurelayers/_version.py',
        'fallback_version': '0.1.0',
        'git_describe_command': 'git describe --tags --dirty --always',
        'tag_regex': r'^(?P<prefix>v)?(?P<version>[^\+]+)(?P<suffix>.*)?$',
        'parse': setuptools_scm.parse.parse_version,
        'write_to_template': '''\
__version__ = "{version}"
'''
    },
    setup_requires=['setuptools_scm'],
)
