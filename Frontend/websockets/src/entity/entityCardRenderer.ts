/// <reference lib="dom" />
/// <reference lib="dom.iterable" />

import { generateUserCard } from "../hydrate/gen_user";
import { generatePostCard } from "../hydrate/gen_post";

type EntityType = "users" | "posts";

export function renderEntitiesOnSimilarityEvent(
  divId: string,
  entityType: EntityType
) {
  document.addEventListener(
    `${entityType}Received` as any,
    (event: CustomEvent) => {
      const entities = event.detail;

      // Generate the HTML representation for each entity
      const cardsHtml = entities
        .map((entity: any) => generateEntityCard(entity, entityType))
        .join("");

      // Insert into the designated div
      const container = document.getElementById(divId);
      if (container) {
        container.innerHTML = cardsHtml;
      } else {
        console.error(`Element with ID "${divId}" not found.`);
      }
    }
  );
}

function generateEntityCard(entity: any, entityType: EntityType): string {
  switch (entityType) {
    case "users":
      return generateUserCard(entity);
    case "posts":
      return generatePostCard(entity);
    // Add other entity types as necessary.
    default:
      console.error("Unknown entity type:", entityType);
      return "";
  }
}
// main.ts
// import { renderEntitiesOnSimilarityEvent } from "./entityCardRenderer";

// renderEntitiesOnSimilarityEvent("your_user_div_id", "user");
// renderEntitiesOnSimilarityEvent("your_post_div_id", "post");
// ... more setups as needed.
