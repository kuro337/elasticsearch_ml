import { ElasticSearchDocument } from "./models/ElasticSearchInterface";
import { User } from "./models/user";
import { Product } from "./models/product";
import { Post } from "./models/post";
import { Interaction } from "./models/interaction";

type ESDocConstructor<T extends ElasticSearchDocument> = new () => T;

interface EntityMapping {
  classConstructor: ESDocConstructor<ElasticSearchDocument>;
  inputSelector: string;
}

export function mapEntityStrToClass(entityStr: string): EntityMapping | null {
  let classConstructor: ESDocConstructor<ElasticSearchDocument> | null = null;
  let inputSelector: string = "";

  switch (entityStr.toLowerCase()) {
    case "user":
      classConstructor = User;
      inputSelector = "#user-input";
      break;
    case "product":
      classConstructor = Product;
      inputSelector = "#product-input";
      break;
    case "post":
      classConstructor = Post;
      inputSelector = "#post-input";
      break;
    case "interaction":
      classConstructor = Interaction;
      inputSelector = "#interaction-input";
      break;
    default:
      console.error("Invalid entity type:", entityStr);
      return null;
  }

  return {
    classConstructor,
    inputSelector,
  };
}
