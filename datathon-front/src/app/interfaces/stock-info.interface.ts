import { Stock } from './stock-base.interface';
import { Insight } from './insight.interface';
import { Observable } from 'rxjs';
interface FundamentalData {
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

interface NewsItem {
  summary: string;
  url: string;
  sentiment_score: number;
}

export interface StockInfo {
  stock: Observable<Stock>; //Hamza
  stockNews: Observable<NewsItem[]>; //Hamza
  sectorNews: Observable<NewsItem[]>; //Hamza
  technicalInsight: Observable<string>; //Luckas
  generalInsights: Observable<Insight[]>; // Hamza
  priceHistory: Observable<any>; // Luckas
  fundamentalData: Observable<FundamentalData>; //Hamza
}
