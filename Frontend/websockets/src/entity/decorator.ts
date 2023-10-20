export function html(type: string, placeholder: string) {
  return function (target: any, propertyKey: string) {
    if (!target.constructor._fieldMetadata) {
      target.constructor._fieldMetadata = {};
    }
    target.constructor._fieldMetadata[propertyKey] = { type, placeholder };
  };
}
