import { ElasticSearchDocument } from "./ElasticSearchInterface";
import { html } from "../decorator";

export class User implements ElasticSearchDocument {
  @html("text", "Enter User Name") // Changed to "number" assuming "username" is a numeric ID. Change back to "text" if it's supposed to be a string.
  public username: string;

  @html("text", "Enter first name")
  public first_name: string;

  @html("text", "Enter last name")
  public last_name: string;

  @html("text", "Enter email")
  public email: string;

  @html("text", "M, F, NA")
  public gender: string;

  @html("text", "Enter country")
  public country: string;

  @html("number", "Enter age")
  public age: number;

  public timestamp?: string;
  public embedding?: number[];

  private esIndexName: string = "users";

  constructor({
    username = "john_doe",
    first_name = "default_first_name",
    last_name = "default_last_name",
    email = "default_email",
    gender = "NA",
    country = "default_country",
    age = 0, // or another appropriate default.
    timestamp,
    embedding,
  }: {
    username?: string;
    first_name?: string;
    last_name?: string;
    email?: string;
    gender?: string;
    country?: string;
    age?: number;
    timestamp?: string;
    embedding?: number[];
  } = {}) {
    this.username = username;
    this.first_name = first_name;
    this.last_name = last_name;
    this.email = email;
    this.gender = gender;
    this.country = country;
    this.age = age;
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
