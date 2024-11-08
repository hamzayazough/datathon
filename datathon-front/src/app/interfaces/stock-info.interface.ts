import { Stock } from './stock-base.interface';
import { Insight } from './insight.interface';
import { Observable } from 'rxjs';
export interface FundamentalData {
  shortName?: string;
  sector?: string;
  industry?: string;
  marketCap?: number;
  volume?: number;
  trailingPE?: number;
  forwardPE?: number;
  dividendYield?: number;
  dividendRate?: number;
  exDividendDate?: string | Date;
  beta?: number;
  trailingEps?: number;
  fiftyTwoWeekHigh?: number;
  fiftyTwoWeekLow?: number;
  priceToBook?: number;
}

export interface NewsItem {
  summary: string;
  url: string;
  sentiment: number;
}

export interface StockInfo {
  stock: Observable<Stock>; //Hamza
  stockNews: Observable<NewsItem[]>; //Hamza
  sectorNews: Observable<NewsItem[]>; //Hamza
  technicalInsight: Observable<String>; //Luckas
  generalInsights: Observable<Insight[]>; // Hamza
  priceHistory: Observable<any>; // Luckas
  fundamentalData: Observable<FundamentalData>; //Hamza
}
