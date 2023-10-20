import { ElasticSearchDocument } from "./ElasticSearchInterface";
import { html } from "../decorator";

export class Interaction implements ElasticSearchDocument {
  @html("text", "Enter interaction type")
  public interaction_type: string;

  @html("text", "Enter post id")
  public post_id: string;

  @html("text", "Enter username")
  public username: string;

  public timestamp?: string;
  public embedding?: number[];

  private esIndexName: string = "interactions";

  constructor({
    interaction_type = "default_interaction_type",
    post_id = "default_post_id",
    username = "default_username",
    timestamp,
    embedding,
  }: {
    interaction_type?: string;
    post_id?: string;
    username?: string;
    timestamp?: string;
    embedding?: number[];
  } = {}) {
    this.interaction_type = interaction_type;
    this.post_id = post_id;
    this.username = username;
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
