"""
Encrypting an Object to store as the ID
Returns a Hash of the Object Passed
"""
import hashlib
import json
from typing import Dict


def generate_hash(document: Dict):
    """
    Encrypts a Document to be stored in Elasticsearch
    """
    return hashlib.md5(json.dumps(document, sort_keys=True).encode()).hexdigest()
