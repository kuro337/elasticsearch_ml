"""
Creating a Module for Websockets

pip install -e .

From other projects, you can now import SBERT like this:

pip install -e /path/to/SBERT 

/home/chin/projects/Search/Elasticsearch/SBERT

"""

from setuptools import setup, find_packages

setup(
    name="Websockets",
    version="0.1.0",
    packages=find_packages(where="websockets"),
    package_dir={"": "websockets"},
)
