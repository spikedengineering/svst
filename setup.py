# Always prefer setuptools over distutils
from setuptools import setup  # type: ignore

# To use a consistent encoding
from codecs import open
from os import path

# The directory containing this file
HERE = path.abspath(path.dirname(__file__))

# Get the long description from the README file
with open(path.join(HERE, "README.md"), encoding="utf-8") as f:
    long_description = f.read()

# This call to setup() does all the work
setup(
    name="svst",
    version="0.1.0",
    description="Standalone Variable Static Typing",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://svst.readthedocs.io/",
    author="Spiked Engineering",
    author_email="spikedengineering@tutanota.com",
    license="MPL2",
    classifiers=[
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.12",
        "Operating System :: OS Independent",
    ],
    packages=["svst"],
    include_package_data=True,
    install_requires=["mypy"],
)
