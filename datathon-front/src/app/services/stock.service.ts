import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';
import { map } from 'rxjs/operators';
import { Stock } from '../interfaces/stock-base.interface';

interface OHLC {
  "Open": any,
  "High":any,
  "Low":any,
  "Close":any,
}

@Injectable({
  providedIn: 'root'
})
export class StockService {
  private apiUrl = 'http://localhost:8000/stocks';
  private technicalAnalysisAPI = 'http://34.219.130.61:57/ask/'
  private stockHistoryAPI = 'http://34.219.130.61/historic/?ticker='

  constructor(private http: HttpClient) {}

  getStocks(): Observable<Stock[]> {
    return this.http.get<Stock[]>(this.apiUrl).pipe(
      map((stocks: Stock[]) => 
        stocks.map(stock => ({
          ...stock,
          changeColor: stock.dayChange >= 0 ? 'green' : 'red'
        }))
      )
    );
  }

  getTAnalysis(ticker: string): Observable<String>{
    return this.http.get<String>(`${this.technicalAnalysisAPI}${ticker}`)
  }

  getHistoricData(ticker: string): Observable<any>{
    return this.http.get<any>(`${this.stockHistoryAPI}${ticker}`) .pipe(map((x)=>x['Close']))
  }
}
