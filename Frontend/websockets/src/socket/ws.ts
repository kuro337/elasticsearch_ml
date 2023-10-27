/// <reference lib="dom" />
/// <reference lib="dom.iterable" />

import { handleRecommendationResponseDirect } from "./handlers/recommendations";
import { handleSimilarEntitiesResponse } from "./handlers/similarity";

const actionHandlers: { [key: string]: Function } = {
  getTopPosts: handleRecommendationResponseDirect,
  similar_entities: handleSimilarEntitiesResponse,
};

export interface WSResponse {
  data: {
    action: string;
    results: any;
  };
}

export class WebSocketClient {
  private webSocket: WebSocket | null = null;
  private wsUrl: string = "ws://localhost:8000/ws";

  constructor(wsUrl?: string) {
    this.wsUrl = wsUrl || "ws://localhost:8000/ws";
  }

  public isConnected(): boolean {
    return (
      this.webSocket !== null && this.webSocket.readyState === WebSocket.OPEN
    );
  }

  public establishConnection(wsUrl?: string): void {
    if (!this.webSocket || this.webSocket.readyState === WebSocket.CLOSED) {
      this.webSocket = new WebSocket(wsUrl || this.wsUrl);

      this.webSocket.onopen = (event) => {
        console.log("Connection opened", event);
      };

      this.webSocket.onclose = (event) => {
        console.log("Connection closed", event);
      };

      this.webSocket.onmessage = (event: MessageEvent<any>) => {
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

      // this.webSocket.onmessage = handleRecommendationResponse;

      this.webSocket.onerror = (error) => {
        console.log("WebSocket Error: ", error);
        // An error occurred during the connection.
      };
    } else {
      console.log("WebSocket is already opened.");
    }
  }

  public sendMessage(message: string): void {
    if (!this.webSocket || this.webSocket.readyState !== WebSocket.OPEN) {
      console.log("Connection not opened. Establishing connection...");
      this.establishConnection();

      this.webSocket!.addEventListener("open", () => {
        this.webSocket!.send(message);
      });
    } else {
      this.webSocket!.send(message);
    }
  }

  public setOnMessageHandler(handler: (event: MessageEvent) => void): void {
    if (this.webSocket) {
      this.webSocket.onmessage = handler;
    }
  }

  public closeConnection(): void {
    if (!this.webSocket || this.webSocket.readyState !== WebSocket.OPEN) {
      console.log("Connection not opened.");
    } else {
      this.webSocket.close(); // This will close the connection.
    }
  }
}
