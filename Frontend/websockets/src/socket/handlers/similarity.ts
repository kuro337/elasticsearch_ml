import { ElasticSearchDocument } from "../../entity/models/ESInterface";
import { ValidEntityString } from "../../entity/models/ESInterface";
import { InvalidElasticsearchIndexError } from "../../entity/models/Exceptions";
import { mapElasticsearchIndexToEntityStr } from "../../entity/entityMapper";

import { createEntity } from "../../entity/entityFactory";
import { WSResponse } from "../ws";
import { ScoreResult } from "../../entity/models/score";

export function handleSimilarEntitiesResponse(data: WSResponse) {
  console.log("Received Similar Entities from Backend:\n", data);

  const entityIndexName = Object.keys(data.data.results).find(
    (key) => key !== "scores"
  );
  if (!entityIndexName) {
    console.log("Entity index name not found in the results.");
    return;
  }

  let entityStr: ValidEntityString;
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

  const rawEntities: ElasticSearchDocument[] =
    data.data.results[entityIndexName];

  const entities = rawEntities.map((rawEntity: ElasticSearchDocument) =>
    createEntity(entityStr, rawEntity)
  );

  // Emit Event with Mapped Entity Objects
  const entitiesEvent = new CustomEvent(`${entityIndexName}Received`, {
    detail: entities,
  });
  document.dispatchEvent(entitiesEvent);

  const scores: ScoreResult[] = data.data.results.scores;

  const scoresEvent = new CustomEvent(`similar_entities_scores_received`, {
    detail: scores,
  });
  document.dispatchEvent(scoresEvent);

  console.log(
    `Similar Entities Event Dispatched :\n eventName : ${entityIndexName}Received`
  );
}
