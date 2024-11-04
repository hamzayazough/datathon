// stock-search.component.ts
import { Component, Output, EventEmitter, OnInit } from '@angular/core';
import { FormControl } from '@angular/forms';
import { debounceTime, distinctUntilChanged } from 'rxjs/operators';
import { FundamentalsService } from '../../../services/fundamentals.service';
import { TickerInfo } from '../../../interfaces/ticker-data.interface';


@Component({
  selector: 'app-stock-search',
  templateUrl: './search-bar.component.html',
})
export class StockSearchComponent implements OnInit {
  searchControl = new FormControl('');
  searchResults: TickerInfo[] = [];
  dataResults : TickerInfo[] = [];
  showResults = false;
  @Output() stockSelected = new EventEmitter<any>();

  constructor(private fundamentals: FundamentalsService) {
    this.searchControl.valueChanges.pipe(
      debounceTime(300),
      distinctUntilChanged()
    ).subscribe(value => {
      if (value) {
        this.searchStocks(value);
      } else {
        this.searchResults = [];
        this.showResults = false;
      }
    });
  }
  ngOnInit(): void {
    this.fundamentals.getAllTickers().subscribe((results) => this.dataResults = results);
  }

  searchStocks(query: string) {
    console.log('hello')
    this.searchResults = this.dataResults.filter(stock => this.filter(stock, query)
    ).sort((a,b) => this.sortCompare(a,b,query));
    this.showResults = this.searchResults.length > 0;
  }

  filter(stock: TickerInfo, query: string) {
    const isInSymbol = stock.symbol.toLowerCase().includes(query.toLowerCase());
    if(query.length <= 2)
      return isInSymbol
    else
      return isInSymbol || stock.name.toLowerCase().includes(query.toLowerCase())
  }

  sortCompare(a: TickerInfo, b : TickerInfo, query: string): number {
    const aStartsWithQuery = a.symbol.toLowerCase().startsWith(query);
    if(aStartsWithQuery)
      return -1;

    const bStartsWithQuery = b.symbol.toLowerCase().startsWith(query);
    if(bStartsWithQuery)
      return 1;

    return a.symbol.toLowerCase().includes(query.toLowerCase()) ? -1 : 1;
  }


  selectStock(stock: TickerInfo) {
    this.stockSelected.emit(stock);
    this.searchControl.setValue('');
    this.showResults = false;
  }
}
