import { Component, OnInit, Output, EventEmitter } from '@angular/core';
import {
  FundamentalData,
  NewsItem,
  StockInfo,
} from '../../../interfaces/stock-info.interface';
import { dummy } from './dummy';
import { Observable, map, take } from 'rxjs';
import { HttpClient } from '@angular/common/http';
import { StockService } from '../../../services/stock.service';
import { Insight } from '../../../interfaces/insight.interface';
import { Stock } from '../../../interfaces/stock-base.interface';
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

  constructor(public http: HttpClient, private stockService: StockService) {}

  ngOnInit() {
    //just dummy, fetch here
    this.stockInfo = {} as StockInfo;
    /* for (let [index, element] of Object.keys(dummy).entries()) {
      (this.stockInfo as any)[element] = new Observable((subscriber) => {
        setTimeout(() => {
          subscriber.next((dummy as any)[element]);
          subscriber.complete();
        }, index * 1000);
      });
    } */

    this.stockInfo = {} as StockInfo;
    this.stockInfo.stockNews = this.http.get<NewsItem[]>(
      `${this.serverUrl}/stocks/${this.symbol}/stock-news`
    );
    this.stockInfo.technicalInsight = this.stockService.getTAnalysis(
      this.symbol
    );
    this.stockInfo.priceHistory = this.stockService.getHistoricData(
      this.symbol
    );
  }

  camelToSnakeCase(str: string) {
    return str.replace(/[A-Z]/g, (letter) => ` ${letter.toLowerCase()}`);
  }

  clickEntry(str: String, source?: string) {
    this.chatEmit.emit(`${str} (${source || 'no source'})`);
  }

  getEntries(obj: Object): any {
    return Object.entries(obj).map(([key, val]) => [
      this.camelToSnakeCase(key),
      val,
    ]);
  }
}
