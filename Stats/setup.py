"""
Creating a Module for SBERT

Run in current directory to Init Module
pip install -e .

From other projects, you can now import SBERT like this:

pip install -e /path/to/SBERT 

/home/chin/projects/Search/Elasticsearch/Stats
"""

from setuptools import setup, find_packages

setup(
    name="Stats",
    version="0.1.0",
    packages=find_packages(),
)
