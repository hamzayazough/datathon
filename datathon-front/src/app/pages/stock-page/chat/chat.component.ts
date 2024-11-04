import { Component } from '@angular/core';
import { Message } from '../../../interfaces/message.interface';

@Component({
  selector: 'app-chat',
  templateUrl: './chat.component.html',
  styleUrl: './chat.component.scss',
})
export class ChatComponent {
  messages: Message[] = [];
  text: string = '';
  disabled = false;

  sendMessageToClaude(message: Message) {
    //do smthng
    this.messages.push(message);
    //this.disabled = false
  }

  submitMsg() {
    if (this.text) {
      this.sendMessageToClaude({ text: this.text });
      this.text = '';
      //this.disabled = true;
    }
  }
}
