import { Component } from '@angular/core';
import { Message } from '../../../interfaces/message.interface';
import { HttpClient } from '@angular/common/http';
import { StringDecoder } from 'string_decoder';

@Component({
  selector: 'app-chat',
  templateUrl: './chat.component.html',
  styleUrl: './chat.component.scss',
})
export class ChatComponent {
  messages: Message[] = [];
  text: string = '';
  serverUrl: string = 'http://127.0.0.1:8000';
  disabled = false;
  constructor(public http: HttpClient) {}

  sendMessageToClaude(message: Message) {
    this.messages.push(message);
    this.disabled = true;
    this.http
      .post<{ response: string }>(`${this.serverUrl}/converse/AAPL`, {
        message: message.query ?? message.text,
      })
      .subscribe((res) => {
        this.disabled = false;
        this.messages.push({ text: res.response });
      });
  }

  submitMsg() {
    if (this.text) {
      this.sendMessageToClaude({ text: this.text });
      this.text = '';
    }
  }
}
