import { get } from "http";
import { ElasticSearchDocument } from "./models/ElasticSearchInterface";

/*
 * @Interface for Model Decorator
 *
 * @Constraints -> Must have a type and placeholder
 *
 */
interface DecoratorMetadata {
  type: string;
  placeholder: string;
}

export function generateEntityHtml(entity: ElasticSearchDocument): string {
  let htmlString = `<div class="entity-label">Entity</div>
      <div id="entity-input">`;

  // Get the Object Containing all Fields with @html Decorators
  const fieldMetadataObject: { [key: string]: DecoratorMetadata } =
    (entity as any).constructor._fieldMetadata || {};

  // Loop over all properties of the entity (user.name , user.email , etc.)

  for (const property of Object.keys(entity)) {
    //
    // Check if property exists in the Metadata
    // If not - do not create HTML for it

    if (!(property in fieldMetadataObject)) {
      continue;
    }

    // Extract Metadata - it exists
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
