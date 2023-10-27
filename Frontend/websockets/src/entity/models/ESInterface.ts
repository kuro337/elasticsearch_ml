export interface ElasticSearchDocument {
  getESIndexName(): string;
}

export type ValidEntityString = "user" | "product" | "post" | "interaction";
