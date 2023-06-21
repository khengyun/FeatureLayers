from setuptools import setup, find_packages
from featurelayers.__version__ import __version__

def local_scheme(version):
    return ""


setup(
    name='featurelayers',
    version=__version__,
    description='featurelayers Package',
    author='khengyun',
    author_email='khaangnguyeen@email.com',
    packages=find_packages(),
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
    use_scm_version={"local_scheme": local_scheme},
    setup_requires=['setuptools_scm'],
)
