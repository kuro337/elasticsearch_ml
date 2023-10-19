"""
Creating a Module for SBERT

pip install -e .

From other projects, you can now import SBERT like this:

pip install -e /path/to/SBERT 

/home/chin/projects/Search/Elasticsearch/SBERT

"""

from setuptools import setup, find_packages


setup(
    name="Stats",
    version="0.1.0",
    packages=find_packages(),
    install_requires=["pandas", "scikit-learn"],
)

# pip install .
