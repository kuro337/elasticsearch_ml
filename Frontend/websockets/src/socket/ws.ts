/// <reference lib="dom" />
/// <reference lib="dom.iterable" />

import { handleRecommendationResponse } from "./handlers/recommendations";

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

      this.webSocket.onmessage = handleRecommendationResponse;

      // this.webSocket.onmessage = (event) => {
      //   console.log("Received message:", event.data.action);

      //   try {
      //     const data = JSON.parse(event.data);
      //     console.log("Data Parsed");

      //     if (
      //       data &&
      //       data.data &&
      //       data.data.action &&
      //       data.data.action === "getTopPosts"
      //     ) {
      //       let sortedPosts = data.data.results.posts || [];

      //       if (data.data.results.scores) {
      //         sortedPosts = sortPostsByScores(
      //           sortedPosts,
      //           data.data.results.scores
      //         );
      //       }

      //       const postsEvent = new CustomEvent("topPostsReceived", {
      //         detail: sortedPosts,
      //       });
      //       document.dispatchEvent(postsEvent);

      //       if (data.data.results.scores) {
      //         const scoresEvent = new CustomEvent("postScoresReceived", {
      //           detail: data.data.results.scores,
      //         });
      //         document.dispatchEvent(scoresEvent);
      //       }
      //     } else {
      //       console.log("Action not found or data not in expected format");
      //     }
      //   } catch (error) {
      //     console.log("Received Message from Backend: ", event.data);
      //   }
      // };

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
