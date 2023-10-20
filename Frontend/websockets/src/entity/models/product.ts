import { ElasticSearchDocument } from "./ElasticSearchInterface";
import { html } from "../decorator";

export class Product implements ElasticSearchDocument {
  @html("text", "Enter product name")
  public product_name: string;

  @html("string", "Enter category")
  public category: string;

  @html("number", "Enter product ID")
  public pid: number;

  @html("text", "Enter product URL")
  public url: string;

  @html("text", "Enter manufacturers")
  public manufacturers: string[];

  @html("date", "Enter last accessed date")
  public last_accessed: string;

  public timestamp?: string;
  public embedding?: number[];

  private esIndexName: string = "products";

  constructor({
    product_name = "default_product",
    category = "default_category",
    pid = 0, // default for numbers could be 0 or another appropriate value
    url = "default_url",
    manufacturers = [],
    last_accessed = "MM/DD/YYYY", // or another appropriate default
    timestamp,
    embedding,
  }: {
    product_name?: string;
    category?: string;
    pid?: number;
    url?: string;
    manufacturers?: string[];
    last_accessed?: string;
    timestamp?: string;
    embedding?: number[];
  } = {}) {
    this.product_name = product_name;
    this.category = category;
    this.pid = pid;
    this.url = url;
    this.manufacturers = manufacturers;
    this.last_accessed = last_accessed;
    if (timestamp) {
      this.timestamp = timestamp;
    }
    if (embedding) {
      this.embedding = embedding;
    }
  }

  public getESIndexName(): string {
    return this.esIndexName;
  }
}
