"""
pip install -e /home/projects/Search/Elasticsearch/SBERT

"""


from elastic_search.es_service import ElasticSearchService


es_service = ElasticSearchService.create_service(cert_location="ssl/ca.crt")
