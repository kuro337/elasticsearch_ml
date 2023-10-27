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

// /home/chin/projects/Search/Elasticsearch/Frontend/websockets/src/utils/sort_posts.ts
function sortPostsByScores(posts, scores) {
  return posts.sort((a, b) => {
    const scoreA =
      scores.find((score) => score.post_id === a.post_id)?.score || 0;
    const scoreB =
      scores.find((score) => score.post_id === b.post_id)?.score || 0;
    return scoreB - scoreA;
  });
}

// /home/chin/projects/Search/Elasticsearch/Frontend/websockets/src/socket/handlers/recommendations.ts
function handleRecommendationResponseDirect(data) {
  console.log("Received Message from Backend:");
  if (data && data.data && data.data.action) {
    let sortedPosts = data.data.results.posts || [];
    if (sortedPosts.length === 0) return;
    if (data.data.results.scores) {
      sortedPosts = sortPostsByScores(sortedPosts, data.data.results.scores);
    }
    const postsEvent = new CustomEvent("topPostsReceived", {
      detail: sortedPosts,
    });
    document.dispatchEvent(postsEvent);
    if (data.data.results.scores) {
      const scoresEvent = new CustomEvent("postScoresReceived", {
        detail: data.data.results.scores,
      });
      document.dispatchEvent(scoresEvent);
    }
  } else {
    console.log("Data format is not as expected");
  }
}

// /home/chin/projects/Search/Elasticsearch/Frontend/websockets/src/entity/models/Exceptions.ts
class InvalidElasticsearchIndexError extends Error {
  constructor(indexName) {
    super(`Invalid Elasticsearch index name: ${indexName}`);
    this.name = "InvalidElasticsearchIndexError";
  }
}

// /home/chin/projects/Search/Elasticsearch/Frontend/websockets/src/entity/decorator.ts
function html(type, placeholder) {
  return function (target, propertyKey) {
    if (!target.constructor._fieldMetadata) {
      target.constructor._fieldMetadata = {};
    }
    target.constructor._fieldMetadata[propertyKey] = { type, placeholder };
  };
}

// /home/chin/projects/Search/Elasticsearch/Frontend/websockets/src/entity/models/user.ts
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

// /home/chin/projects/Search/Elasticsearch/Frontend/websockets/src/entity/models/product.ts
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

// /home/chin/projects/Search/Elasticsearch/Frontend/websockets/src/entity/models/post.ts
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

// /home/chin/projects/Search/Elasticsearch/Frontend/websockets/src/entity/models/interaction.ts
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

// /home/chin/projects/Search/Elasticsearch/Frontend/websockets/src/entity/entityMapper.ts
function mapEntityStrToClass(entityStr) {
  let classConstructor = null;
  let inputSelector = "";
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
function mapElasticsearchIndexToEntityStr(indexName) {
  switch (indexName.toLowerCase()) {
    case "users":
      return "user";
    case "products":
      return "product";
    case "posts":
      return "post";
    case "interactions":
      return "interaction";
    default:
      throw new InvalidElasticsearchIndexError(indexName);
  }
}

// /home/chin/projects/Search/Elasticsearch/Frontend/websockets/src/entity/entityFactory.ts
function createEntity(entityStr, data) {
  let EntityClass = null;
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

// /home/chin/projects/Search/Elasticsearch/Frontend/websockets/src/socket/handlers/similarity.ts
function handleSimilarEntitiesResponse(data) {
  console.log("Received Similar Entities from Backend:\n", data);
  const entityIndexName = Object.keys(data.data.results).find(
    (key) => key !== "scores"
  );
  if (!entityIndexName) {
    console.log("Entity index name not found in the results.");
    return;
  }
  let entityStr;
  try {
    entityStr = mapElasticsearchIndexToEntityStr(entityIndexName);
  } catch (error) {
    if (error instanceof InvalidElasticsearchIndexError) {
      console.error(error.message);
    } else {
      console.error("Unexpected error:", error);
    }
    return;
  }
  const rawEntities = data.data.results[entityIndexName];
  const entities = rawEntities.map((rawEntity) =>
    createEntity(entityStr, rawEntity)
  );
  const entitiesEvent = new CustomEvent(`${entityIndexName}Received`, {
    detail: entities,
  });
  document.dispatchEvent(entitiesEvent);
  const scores = data.data.results.scores;
  const scoresEvent = new CustomEvent(`similar_entities_scores_received`, {
    detail: scores,
  });
  document.dispatchEvent(scoresEvent);
  console.log(
    `Similar Entities Event Dispatched :\n eventName : ${entityIndexName}Received`
  );
}

// /home/chin/projects/Search/Elasticsearch/Frontend/websockets/src/socket/ws.ts
var actionHandlers = {
  getTopPosts: handleRecommendationResponseDirect,
  similar_entities: handleSimilarEntitiesResponse,
};

class WebSocketClient {
  webSocket = null;
  wsUrl = "ws://localhost:8000/ws";
  constructor(wsUrl) {
    this.wsUrl = wsUrl || "ws://localhost:8000/ws";
  }
  isConnected() {
    return (
      this.webSocket !== null && this.webSocket.readyState === WebSocket.OPEN
    );
  }
  establishConnection(wsUrl) {
    if (!this.webSocket || this.webSocket.readyState === WebSocket.CLOSED) {
      this.webSocket = new WebSocket(wsUrl || this.wsUrl);
      this.webSocket.onopen = (event) => {
        console.log("Connection opened", event);
      };
      this.webSocket.onclose = (event) => {
        console.log("Connection closed", event);
      };
      this.webSocket.onmessage = (event) => {
        console.log("initial handler for message", event);
        if (
          typeof event.data === "string" &&
          !event.data.trim().startsWith("{")
        ) {
          console.log("Received Plain String from Backend:", event.data);
          return;
        }
        try {
          const data = JSON.parse(event.data);
          const handler = actionHandlers[data.data.action];
          if (handler) {
            handler(data);
          } else {
            console.log("Unknown action or data not in expected format");
          }
        } catch (error) {
          console.error("Error parsing message as JSON:", error);
        }
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
      console.log("Connection not opened. Establishing connection...");
      this.establishConnection();
      this.webSocket.addEventListener("open", () => {
        this.webSocket.send(message);
      });
    } else {
      this.webSocket.send(message);
    }
  }
  setOnMessageHandler(handler) {
    if (this.webSocket) {
      this.webSocket.onmessage = handler;
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
// /home/chin/projects/Search/Elasticsearch/Frontend/websockets/src/entity/dynInputGen.ts
function generateEntityHtml(entity) {
  const entityName = entity.constructor.name.toLowerCase();
  let htmlString = `<div class="entity-label" id=${entityName}>Entity</div>
      <div class="entity-input" >`;
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
// /home/chin/projects/Search/Elasticsearch/Frontend/websockets/src/entity/serializeEntity.ts
function createEntityFromInputs(EntityClass, inputContainerSelector) {
  const inputs = document.querySelectorAll(
    `${inputContainerSelector} sl-input`
  );
  const entity = new EntityClass();
  inputs.forEach((inputElement) => {
    const input = inputElement;
    const fieldName = input.name;
    const value = parseInputValue(input.value, fieldName, entity);
    if (fieldName in entity) {
      entity[fieldName] = value;
    }
  });
  const entityName = EntityClass.name;
  return {
    entity: entityName,
    data: entity,
  };
}
function parseInputValue(value, fieldName, entity) {
  if (typeof entity[fieldName] === "number") {
    return Number(value);
  }
  if (Array.isArray(entity[fieldName])) {
    if (typeof entity[fieldName][0] === "number") {
      return value.split(",").map(Number);
    }
    return value.split(",");
  }
  return value;
}
// /home/chin/projects/Search/Elasticsearch/Frontend/websockets/src/hydrate/gen_user.ts
function generateUserCard(user3) {
  console.log("Received User: ", user3);
  const cardStyles = `
  border: 1px solid #555;
  padding: 15px;
  margin: 10px;
  background-color: #222;
  font-family: "Lato", sans-serif;
  color: #fff;
  display: flex;
  flex-direction: column;
`;
  const fieldStyles = `
  margin-bottom: 10px;
  display: flex;
`;
  const keyStyles = `
  width: 100px;
`;
  const cardHtml = `
<div style="${cardStyles}">
  <div style="${fieldStyles}"><span style="${keyStyles}">Username:</span> ${user3.username}</div>
  <div style="${fieldStyles}"><span style="${keyStyles}">Name:</span> ${user3.first_name} ${user3.last_name}</div>
  <div style="${fieldStyles}"><span style="${keyStyles}">Email:</span> ${user3.email}</div>
  <div style="${fieldStyles}"><span style="${keyStyles}">Gender:</span> ${user3.gender}</div>
  <div style="${fieldStyles}"><span style="${keyStyles}">Country:</span> ${user3.country}</div>
  <div style="${fieldStyles}"><span style="${keyStyles}">Age:</span> ${user3.age}</div>
</div>
`;
  return cardHtml;
}

// /home/chin/projects/Search/Elasticsearch/Frontend/websockets/src/hydrate/gen_post.ts
function generatePostCard(post3) {
  const cardStyles = `
    border: 1px solid #555;
    padding: 15px;
    margin: 10px;
    background-color: #111;
    font-family: "Lato", sans-serif;
    font-size: 0.75rem;
    color: #ddd;
    display: flex;
    flex-direction: column;
  `;
  const fieldStyles = `
    margin-bottom: 10px;
    display: flex;
  `;
  const keyStyles = `
    width: 120px;
  `;
  const cardHtml = `
    <div style="${cardStyles}">
      <div style="${fieldStyles}"><span style="${keyStyles}">Post:</span> ${post3.post_id}</div>
      <div style="${fieldStyles}"><span style="${keyStyles}">Lang:</span> ${post3.lang}</div>
      <div style="${fieldStyles}"><span style="${keyStyles}">Title:</span> ${post3.title}</div>
      <div style="${fieldStyles}"><span style="${keyStyles}">Short Title:</span> ${post3.short_title}</div>
      <div style="${fieldStyles}"><span style="${keyStyles}">Description:</span> ${post3.description}</div>
      <div style="${fieldStyles}"><span style="${keyStyles}">Author:</span> ${post3.author}</div>
      <div style="${fieldStyles}"><span style="${keyStyles}">Tags:</span> ${post3.tags}</div>
    </div>
  `;
  return cardHtml;
}

// /home/chin/projects/Search/Elasticsearch/Frontend/websockets/src/entity/entityCardRenderer.ts
function renderEntitiesOnSimilarityEvent(divId, entityType) {
  document.addEventListener(`${entityType}Received`, (event) => {
    const entities = event.detail;
    const cardsHtml = entities
      .map((entity) => generateEntityCard(entity, entityType))
      .join("");
    const container = document.getElementById(divId);
    if (container) {
      container.innerHTML = cardsHtml;
    } else {
      console.error(`Element with ID "${divId}" not found.`);
    }
  });
}
var generateEntityCard = function (entity, entityType) {
  switch (entityType) {
    case "users":
      return generateUserCard(entity);
    case "posts":
      return generatePostCard(entity);
    default:
      console.error("Unknown entity type:", entityType);
      return "";
  }
};
// /home/chin/projects/Search/Elasticsearch/Frontend/websockets/src/hydrate/gen_scores.ts
function generateScoresCard(scores) {
  let scoresList = "";
  scores.forEach((score) => {
    scoresList += `
      <div class="score-field">
        <span class="score-id">${score.post_id}</span>
        <span class="score-value">${score.score}</span>
      </div>`;
  });
  const cardHtml = `
    <div class="card score-card">
      ${scoresList}
    </div>
  `;
  return cardHtml;
}
// /home/chin/projects/Search/Elasticsearch/Frontend/websockets/index.ts
console.log("Hello via Bun!");
export {
  renderEntitiesOnSimilarityEvent,
  mapEntityStrToClass,
  generateUserCard,
  generateScoresCard,
  generatePostCard,
  generateEntityHtml,
  createEntityFromInputs,
  WebSocketClient,
  User,
  Product,
  Post,
  Interaction,
};
