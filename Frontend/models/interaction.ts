import { ElasticSearchDocument } from "./ElasticSearchInterface";

export class Interaction implements ElasticSearchDocument {
  public interaction_type: string;
  public post_id: string;
  public username: string;
  public timestamp?: string;
  public embedding?: number[];

  private esIndexName: string = "interactions";

  public getESIndexName(): string {
    return this.esIndexName;
  }
}
