"""
@Utilility

@SerializeJSON 
@ClientFacing

- Root Handler uses this Utility to Extract:
  - @Action  
  - @Payload 
"""
import json


def serialize_client_message(message: str):
    """
    Serialize Data sent by Client
    """
    print(f"Message received:\n {message}")

    try:
        data_dict = json.loads(message)
    except json.JSONDecodeError:
        return "ws_help", message

    action = data_dict.get("action")
    payload = data_dict.get("payload")

    print(f"Action Received by Root Handler:\n {action}")

    return action, payload
