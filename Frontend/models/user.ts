import { ElasticSearchDocument } from "./ElasticSearchInterface";

export class User implements ElasticSearchDocument {
  public username: number;
  public first_name: string;
  public last_name: string;
  public email: string;
  public gender: string;
  public country: string;
  public age: number;
  public timestamp?: string;
  public embedding?: number[];

  private esIndexName: string = "users";

  public getESIndexName(): string {
    return this.esIndexName;
  }
}
