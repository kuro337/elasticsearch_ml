export class InvalidElasticsearchIndexError extends Error {
  constructor(indexName: string) {
    super(`Invalid Elasticsearch index name: ${indexName}`);
    this.name = "InvalidElasticsearchIndexError";
  }
}
