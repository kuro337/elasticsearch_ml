import { ElasticSearchDocument } from "./models/ElasticSearchInterface";

type InputValue = string | number | string[] | number[]; // JSON serializable types

interface InputData {
  [key: string]: InputValue;
}

// Function to create an entity from the form inputs
export function createEntityFromInputs<T extends ElasticSearchDocument>(
  EntityClass: new () => T, // class constructor
  inputContainerSelector: string // selector for the form or container of inputs
): { entity: string; data: T } {
  const inputs = document.querySelectorAll(
    `${inputContainerSelector} sl-input`
  );

  // Create a new entity with default values using the class constructor
  const entity = new EntityClass();

  inputs.forEach((inputElement) => {
    const input = inputElement as HTMLInputElement;
    const fieldName = input.name;
    const value = parseInputValue(input.value, fieldName, entity);

    // If the field exists in the entity class (including inherited properties)
    if (fieldName in entity) {
      // Assign the input value to the corresponding field in the entity
      (entity[fieldName as keyof T] as any) = value; // We use 'any' here because TypeScript doesn't allow index access on type variables
    }
  });

  const entityName = EntityClass.name;
  return {
    entity: entityName,
    data: entity,
  };
  // return entity;
}

export function parseInputValue(
  value: string,
  fieldName: string,
  entity: any
): InputValue {
  if (typeof entity[fieldName] === "number") {
    return Number(value);
  }

  if (Array.isArray(entity[fieldName])) {
    if (typeof entity[fieldName][0] === "number") {
      return value.split(",").map(Number);
    }

    return value.split(",");
  }

  return value; // serialize to string by default
}

// Example usage:
// Assuming `Product` and `Interaction` are classes that implement `ElasticSearchDocument` and have a no-argument constructor
// const product = createEntityFromInputs(Product, "#product-inputs");
// const interaction = createEntityFromInputs(Interaction, "#interaction-inputs");
