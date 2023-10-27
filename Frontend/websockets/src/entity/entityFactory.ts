import { ElasticSearchDocument } from "./models/ESInterface";
import { ValidEntityString } from "./models/ESInterface";
import { User } from "./models/user";
import { Product } from "./models/product";
import { Post } from "./models/post";
import { Interaction } from "./models/interaction";

type ESDocWithDataConstructor<T extends ElasticSearchDocument> = new (
  data: any
) => T;

export function createEntity(
  entityStr: ValidEntityString,
  data: any
): ElasticSearchDocument {
  let EntityClass: ESDocWithDataConstructor<ElasticSearchDocument> | null =
    null;

  switch (entityStr) {
    case "user":
      EntityClass = User;
      break;
    case "product":
      EntityClass = Product;
      break;
    case "post":
      EntityClass = Post;
      break;
    case "interaction":
      EntityClass = Interaction;
      break;
    default:
      throw new Error(`Invalid entity type: ${entityStr}`);
  }

  return new EntityClass(data);
}
