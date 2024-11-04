import { Component, OnInit, Output, EventEmitter } from '@angular/core';
import { StockInfo } from '../../../interfaces/stock-info.interface';
import { dummy } from './dummy';
import { Observable } from 'rxjs';
@Component({
  selector: 'app-page-content',
  templateUrl: './page-content.component.html',
  styleUrl: './page-content.component.scss',
})
export class PageContentComponent implements OnInit {
  stockInfo?: StockInfo;
  @Output() chatEmit: EventEmitter<string> = new EventEmitter<string>();

  ngOnInit() {
    //just dummy, fetch here
    this.stockInfo = {} as StockInfo;
    for (let [index, element] of Object.keys(dummy).entries()) {
      (this.stockInfo as any)[element] = new Observable((subscriber) => {
        setTimeout(() => {
          subscriber.next((dummy as any)[element]);
          subscriber.complete();
        }, index * 1000);
      });
    }
  }

  camelToSnakeCase(str: string) {
    return str.replace(/[A-Z]/g, (letter) => ` ${letter.toLowerCase()}`);
  }

  clickEntry(str: string, source?: string) {
    this.chatEmit.emit(`${str} (${source || 'no source'})`);
  }

  getEntries(obj: Object): any {
    return Object.entries(obj).map(([key, val]) => [
      this.camelToSnakeCase(key),
      val,
    ]);
  }
}
