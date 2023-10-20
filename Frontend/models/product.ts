import { ElasticSearchDocument } from "./ElasticSearchInterface";

export class Product implements ElasticSearchDocument {
  public id: number;
  public url: string;
  public last_accessed: string;
  public ip_address: string;
  public user_agent: string;
  public dates: string[];
  public manufacturers: string[];
  public timestamp?: string;
  public embedding?: number[];

  private esIndexName: string = "products";

  public getESIndexName(): string {
    return this.esIndexName;
  }
}
