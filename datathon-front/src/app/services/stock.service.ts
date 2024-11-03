import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';
import { map } from 'rxjs/operators';
import { Stock } from '../interfaces/stock-base.interface';

@Injectable({
  providedIn: 'root'
})
export class StockService {
  private apiUrl = 'http://localhost:8000/stocks';

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
}
