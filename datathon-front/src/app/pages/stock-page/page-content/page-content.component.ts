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
import { ActivatedRoute } from '@angular/router';
import { FundamentalsService } from '../../../services/fundamentals.service';
@Component({
  selector: 'app-page-content',
  templateUrl: './page-content.component.html',
  styleUrl: './page-content.component.scss',
})
export class PageContentComponent implements OnInit {
  stockInfo?: StockInfo;
  @Output() chatEmit: EventEmitter<string> = new EventEmitter<string>();
  symbol: string = '';
  serverUrl: string = 'http://127.0.0.1:8000';

  constructor(
    public http: HttpClient,
    private stockService: StockService,
    private activatedRoute: ActivatedRoute,
    private fund: FundamentalsService
  ) {}

  ngOnInit() {
    this.symbol = this.activatedRoute.snapshot.params['ticker'];
    this.stockInfo = {} as StockInfo;

    this.stockInfo.stockNews = this.http.get<NewsItem[]>(
      `${this.serverUrl}/stocks/${this.symbol}/stock-news`
    );
    this.stockInfo.technicalInsight = this.http
      .get<string>(`${this.serverUrl}/ask/${this.symbol}`)
      .pipe(take(1));

    this.stockInfo.priceHistory = this.http
      .get<string>(`${this.serverUrl}/historic/${this.symbol}`)
      .pipe(take(1));

    this.stockInfo.stockNews = this.http
      .get<{ news: NewsItem[] }>(
        `${this.serverUrl}/stocks/${this.symbol}/stock-news`
      )
      .pipe(map((x) => x.news))
      .pipe(take(1));

    this.stockInfo.sectorNews = this.http
      .get<{ news: NewsItem[] }>(
        `${this.serverUrl}/stocks/${this.symbol}/sector-news`
      )
      .pipe(map((x) => x.news))
      .pipe(take(1));

    this.stockInfo.generalInsights = this.http
      .get<{ reports: Insight[] }>(
        `${this.serverUrl}/stocks/${this.symbol}/reports-analysis`
      )
      .pipe(map((x) => x.reports))
      .pipe(take(1));

    this.stockInfo.fundamentalData = this.http
      .get<FundamentalData>(
        `${this.serverUrl}/stocks/${this.symbol}/market-cap`
      )
      .pipe(take(1));

    this.stockInfo.stock = this.fund
      .getAllTickers()
      .pipe(
        map((x) => x.find((x) => x.symbol === this.symbol))
      ) as Observable<Stock>;
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
