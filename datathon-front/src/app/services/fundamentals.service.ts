import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';
import { StockFundamentals } from '../interfaces/stock-fundamentals';
import { TickerInfo } from '../interfaces/ticker-data.interface';

@Injectable({
  providedIn: 'root'
})
export class FundamentalsService {
  private apiUrl = 'http://127.0.0.1:8000/stocks';

  constructor(private http: HttpClient) {}

  getAllTickers(): Observable<TickerInfo[]> {
    return this.http.get<TickerInfo[]>(this.apiUrl);
  }
}
