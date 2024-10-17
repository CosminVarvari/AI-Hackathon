import { Injectable } from '@angular/core';
import { WebSocketSubject } from 'rxjs/webSocket';

@Injectable({
  providedIn: 'root'
})
export class ChatService {
  private socket$!: WebSocketSubject<any>;

  connect(roomName: string) {
    this.socket$ = new WebSocketSubject('ws://localhost:8000/ws/chat/global/');

    return this.socket$;
  }

  sendMessage(message: string, username: string, roomName: string) {
    this.socket$.next({ message, username, roomName });
  }

  disconnect() {
    this.socket$.complete();
  }
}