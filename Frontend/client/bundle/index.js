var __legacyDecorateClassTS = function (decorators, target, key, desc) {
  var c = arguments.length,
    r =
      c < 3
        ? target
        : desc === null
        ? (desc = Object.getOwnPropertyDescriptor(target, key))
        : desc,
    d;
  if (typeof Reflect === "object" && typeof Reflect.decorate === "function")
    r = Reflect.decorate(decorators, target, key, desc);
  else
    for (var i = decorators.length - 1; i >= 0; i--)
      if ((d = decorators[i]))
        r = (c < 3 ? d(r) : c > 3 ? d(target, key, r) : d(target, key)) || r;
  return c > 3 && r && Object.defineProperty(target, key, r), r;
};

class WebSocketClient {
  webSocket = null;
  establishConnection(wsUrl) {
    if (!this.webSocket || this.webSocket.readyState === WebSocket.CLOSED) {
      this.webSocket = new WebSocket(wsUrl || "ws://localhost:8000/ws");
      this.webSocket.onopen = (event) => {
        console.log("Connection opened", event);
      };
      this.webSocket.onmessage = (event) => {
        console.log("Received message from server:", event.data);
      };
      this.webSocket.onclose = (event) => {
        console.log("Connection closed", event);
      };
      this.webSocket.onerror = (error) => {
        console.log("WebSocket Error: ", error);
      };
    } else {
      console.log("WebSocket is already opened.");
    }
  }
  sendMessage(message) {
    if (!this.webSocket || this.webSocket.readyState !== WebSocket.OPEN) {
      console.log("Connection not opened.");
    } else {
      this.webSocket.send(message);
    }
  }
  closeConnection() {
    if (!this.webSocket || this.webSocket.readyState !== WebSocket.OPEN) {
      console.log("Connection not opened.");
    } else {
      this.webSocket.close();
    }
  }
}
function generateEntityHtml(entity) {
  let htmlString = `<div class="entity-label">Entity</div>
      <div id="entity-input">`;
  const fieldMetadataObject = entity.constructor._fieldMetadata || {};
  for (const property of Object.keys(entity)) {
    if (!(property in fieldMetadataObject)) {
      continue;
    }
    let { type, placeholder } = fieldMetadataObject[property];
    if (!type || !placeholder) {
      continue;
    }
    htmlString += `
      <div class="entity-field-selection">
        <label for="${property}">${property}</label>
        <sl-input type="${type}" name="${property}" placeholder="${placeholder}" id="${property}" />
      </div>`;
  }
  htmlString += `</div>`;
  return htmlString;
}
function html(type, placeholder) {
  return function (target, propertyKey) {
    if (!target.constructor._fieldMetadata) {
      target.constructor._fieldMetadata = {};
    }
    target.constructor._fieldMetadata[propertyKey] = { type, placeholder };
  };
}

class Post {
  timestamp;
  embedding;
  esIndexName = "posts";
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
  getESIndexName() {
    return this.esIndexName;
  }
}
__legacyDecorateClassTS(
  [html("text", "Enter language")],
  Post.prototype,
  "lang",
  undefined
);
__legacyDecorateClassTS(
  [html("text", "Enter Post Title")],
  Post.prototype,
  "title",
  undefined
);
__legacyDecorateClassTS(
  [html("text", "Enter short title")],
  Post.prototype,
  "short_title",
  undefined
);
__legacyDecorateClassTS(
  [html("text", "Enter description")],
  Post.prototype,
  "description",
  undefined
);
__legacyDecorateClassTS(
  [html("text", "Enter author")],
  Post.prototype,
  "author",
  undefined
);
__legacyDecorateClassTS(
  [html("text", "Enter tags")],
  Post.prototype,
  "tags",
  undefined
);
__legacyDecorateClassTS(
  [html("text", "Enter post id")],
  Post.prototype,
  "post_id",
  undefined
);
__legacyDecorateClassTS(
  [html("text", "Enter component")],
  Post.prototype,
  "component",
  undefined
);
__legacyDecorateClassTS(
  [html("text", "Enter dynamic path")],
  Post.prototype,
  "dynamic_path",
  undefined
);
__legacyDecorateClassTS(
  [html("text", "Enter render function")],
  Post.prototype,
  "render_func",
  undefined
);
class Product {
  timestamp;
  embedding;
  esIndexName = "products";
  constructor({
    product_name = "default_product",
    category = "default_category",
    pid = 0,
    url = "default_url",
    manufacturers = [],
    last_accessed = "MM/DD/YYYY",
    timestamp,
    embedding,
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
  getESIndexName() {
    return this.esIndexName;
  }
}
__legacyDecorateClassTS(
  [html("text", "Enter product name")],
  Product.prototype,
  "product_name",
  undefined
);
__legacyDecorateClassTS(
  [html("string", "Enter category")],
  Product.prototype,
  "category",
  undefined
);
__legacyDecorateClassTS(
  [html("number", "Enter product ID")],
  Product.prototype,
  "pid",
  undefined
);
__legacyDecorateClassTS(
  [html("text", "Enter product URL")],
  Product.prototype,
  "url",
  undefined
);
__legacyDecorateClassTS(
  [html("text", "Enter manufacturers")],
  Product.prototype,
  "manufacturers",
  undefined
);
__legacyDecorateClassTS(
  [html("date", "Enter last accessed date")],
  Product.prototype,
  "last_accessed",
  undefined
);
class User {
  timestamp;
  embedding;
  esIndexName = "users";
  constructor({
    username = "john_doe",
    first_name = "default_first_name",
    last_name = "default_last_name",
    email = "default_email",
    gender = "NA",
    country = "default_country",
    age = 0,
    timestamp,
    embedding,
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
  getESIndexName() {
    return this.esIndexName;
  }
}
__legacyDecorateClassTS(
  [html("text", "Enter User Name")],
  User.prototype,
  "username",
  undefined
);
__legacyDecorateClassTS(
  [html("text", "Enter first name")],
  User.prototype,
  "first_name",
  undefined
);
__legacyDecorateClassTS(
  [html("text", "Enter last name")],
  User.prototype,
  "last_name",
  undefined
);
__legacyDecorateClassTS(
  [html("text", "Enter email")],
  User.prototype,
  "email",
  undefined
);
__legacyDecorateClassTS(
  [html("text", "M, F, NA")],
  User.prototype,
  "gender",
  undefined
);
__legacyDecorateClassTS(
  [html("text", "Enter country")],
  User.prototype,
  "country",
  undefined
);
__legacyDecorateClassTS(
  [html("number", "Enter age")],
  User.prototype,
  "age",
  undefined
);
class Interaction {
  timestamp;
  embedding;
  esIndexName = "interactions";
  constructor({
    interaction_type = "default_interaction_type",
    post_id = "default_post_id",
    username = "default_username",
    timestamp,
    embedding,
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
  getESIndexName() {
    return this.esIndexName;
  }
}
__legacyDecorateClassTS(
  [html("text", "Enter interaction type")],
  Interaction.prototype,
  "interaction_type",
  undefined
);
__legacyDecorateClassTS(
  [html("text", "Enter post id")],
  Interaction.prototype,
  "post_id",
  undefined
);
__legacyDecorateClassTS(
  [html("text", "Enter username")],
  Interaction.prototype,
  "username",
  undefined
);

console.log("Hello via Bun!");
export {
  generateEntityHtml,
  WebSocketClient,
  User,
  Product,
  Post,
  Interaction,
};
