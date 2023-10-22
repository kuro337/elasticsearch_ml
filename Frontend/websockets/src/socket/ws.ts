/// <reference lib="dom" />
/// <reference lib="dom.iterable" />

export class WebSocketClient {
  private webSocket: WebSocket | null = null;

  public isConnected(): boolean {
    return (
      this.webSocket !== null && this.webSocket.readyState === WebSocket.OPEN
    );
  }

  public establishConnection(wsUrl?: string): void {
    if (!this.webSocket || this.webSocket.readyState === WebSocket.CLOSED) {
      this.webSocket = new WebSocket(wsUrl || "ws://localhost:8000/ws");

      this.webSocket.onopen = (event) => {
        console.log("Connection opened", event);
        // Connection was opened.
      };

      this.webSocket.onmessage = (event) => {
        console.log("Received message from server:", event.data);
        // You can process received messages here.
      };

      this.webSocket.onclose = (event) => {
        console.log("Connection closed", event);
        // Connection was closed.
      };

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
      console.log("Connection not opened.");
    } else {
      this.webSocket.send(message); // Your message is sent to the server.
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
