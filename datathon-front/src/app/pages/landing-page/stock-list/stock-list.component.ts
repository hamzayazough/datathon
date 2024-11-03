import { Component, OnInit } from '@angular/core';
import { StockService } from '../../../services/stock.service';
import { Stock } from '../../../interfaces/stock-base.interface';

@Component({
  selector: 'app-stock-list',
  templateUrl: './stock-list.component.html',
  styleUrls: ['./stock-list.component.scss'],
})
export class StockListComponent implements OnInit {
  stocks: Stock[] = [];

  constructor(private stockService: StockService) {}

  ngOnInit(): void {
    this.stockService.getStocks().subscribe(
      (data) => {
        this.stocks = data;
      },
      (error) => {
        console.error(
          'Erreur lors de la récupération des données de stock:',
          error
        );
      }
    );
  }
}
