import { ElasticSearchDocument } from "./ESInterface";
import { html } from "../decorator";

export class Post implements ElasticSearchDocument {
  @html("text", "Enter language")
  public lang: string;

  @html("text", "Enter Post Title")
  public title: string;

  @html("text", "Enter short title")
  public short_title: string;

  @html("text", "Enter description")
  public description: string;

  @html("text", "Enter author")
  public author: string;

  @html("text", "Enter tags")
  public tags: string;

  @html("text", "Enter post id")
  public post_id: string;

  @html("text", "Enter component")
  public component: string;

  @html("text", "Enter dynamic path")
  public dynamic_path: string;

  @html("text", "Enter render function")
  public render_func: string;

  public timestamp?: string;
  public embedding?: number[];

  private esIndexName: string = "posts";

  constructor({
    lang = "default_language",
    title = "default_title",
    short_title = "default_short_title",
    description = "default_description",
    author = "default_author",
    tags = "default_tags",
    post_id = "default_post_id",
    component = "default_component",
    dynamic_path = "default_dynamic_path",
    render_func = "default_render_function",
    timestamp,
    embedding,
  }: {
    lang?: string;
    title?: string;
    short_title?: string;
    description?: string;
    author?: string;
    tags?: string;
    post_id?: string;
    component?: string;
    dynamic_path?: string;
    render_func?: string;
    timestamp?: string;
    embedding?: number[];
  } = {}) {
    this.lang = lang;
    this.title = title;
    this.short_title = short_title;
    this.description = description;
    this.author = author;
    this.tags = tags;
    this.post_id = post_id;
    this.component = component;
    this.dynamic_path = dynamic_path;
    this.render_func = render_func;
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
