import { Component, ViewChild } from '@angular/core';
import { MatSidenav } from '@angular/material/sidenav';
import { ChatComponent } from '../chat/chat.component';
import { Message } from '../../../interfaces/message.interface';

@Component({
  selector: 'app-stock-page',
  templateUrl: './stock-page.component.html',
  styleUrl: './stock-page.component.scss',
})
export class StockPageComponent {
  @ViewChild('sidenav') sidenav!: MatSidenav;
  @ViewChild('chat') chat!: ChatComponent;
  toggleMatSidenav() {
    this.sidenav.toggle();
  }

  handleChatEmit(query: string) {
    this.sidenav.open();
    const message: Message = {
      query: `please tell me more about this and explain it thoroughly: ${query}`,
      special: true,
      text: `Referenced an element (${query})`,
    };

    this.chat.sendMessageToClaude(message);
  }
}
