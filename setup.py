# Always prefer setuptools over distutils
from setuptools import setup  # type: ignore

# To use a consistent encoding
from codecs import open
from os import path

# The directory containing this file
HERE: str = path.abspath(path.dirname(__file__))

# Get the long description from the README file
with open(path.join(HERE, "README.md"), encoding="utf-8") as f:
    long_description: str = f.read()

# This call to setup() does all the work
setup(
    name="svst",
    version="0.1.14",
    description="Standalone Variables Static Typing",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://svst.readthedocs.io/",
    author="Spiked Engineering",
    author_email="spikedengineering@tutanota.com",
    project_urls={
        "Code Repository": "https://github.com/spikedengineering/svst",
        "Documentation": "https://svst.readthedocs.io/",
    },
    license="MPL2",
    classifiers=[
        "Intended Audience :: Developers",
        "License :: OSI Approved :: Mozilla Public License 2.0 (MPL 2.0)",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Operating System :: OS Independent",
    ],
    packages=["svst"],
    include_package_data=True,
    install_requires=["mypy"],
    entry_points={
        "console_scripts": [
            "svst = svst.cli:main",
        ],
    },
)
