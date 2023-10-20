"""
Exceptions for Elasticsearch
"""


class ElasticsearchInsertionError(Exception):
    """Exception raised for errors in Elasticsearch document insertion."""


class ElasticsearchConnectionError(Exception):
    """Exception raised for errors in Elasticsearch document insertion."""


class SSLCertificateNotProvided(Exception):
    """SSL Certicate Is Required To Connect To Elasticsearch"""


class ElasticsearchIndexAlreadyExists(Exception):
    """Index Already Exists"""
