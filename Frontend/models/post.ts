import { ElasticSearchDocument } from "./ElasticSearchInterface";

export class Post implements ElasticSearchDocument {
  public lang: string;
  public title: string;
  public short_title: string;
  public description: string;
  public author: string;
  public tags: string;
  public post_id: string;
  public component: string;
  public dynamic_path: string;
  public render_func: string;
  public timestamp?: string;
  public embedding?: number[];

  private esIndexName: string = "posts";

  public getESIndexName(): string {
    return this.esIndexName;
  }
}
