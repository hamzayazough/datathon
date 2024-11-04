import { Component, OnInit, Output, EventEmitter } from '@angular/core';
import { NewsItem, StockInfo } from '../../../interfaces/stock-info.interface';
import { dummy } from './dummy';
import { Observable } from 'rxjs';
import { HttpClient, HttpRequest } from '@angular/common/http';
@Component({
  selector: 'app-page-content',
  templateUrl: './page-content.component.html',
  styleUrl: './page-content.component.scss',
})
export class PageContentComponent implements OnInit {
  stockInfo?: StockInfo;
  @Output() chatEmit: EventEmitter<string> = new EventEmitter<string>();
  symbol: string = 'AAPL';
  serverUrl: string = 'http://127.0.0.1:8000';

  constructor(public http: HttpClient) {}

  ngOnInit() {
    //just dummy, fetch here

    for (let [index, element] of Object.keys(dummy).entries()) {
      (this.stockInfo as any)[element] = new Observable((subscriber) => {
        setTimeout(() => {
          subscriber.next((dummy as any)[element]);
          subscriber.complete();
        }, index * 1000);
      });
    }

    this.stockInfo = {} as StockInfo;
    this.stockInfo.stockNews = this.http.get<NewsItem[]>(
      `${this.serverUrl}/stocks/${this.symbol}/stock-news`
    );
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
