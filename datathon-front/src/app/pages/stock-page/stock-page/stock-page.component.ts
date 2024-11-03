import { Component, ViewChild } from '@angular/core';
import { MatSidenav } from '@angular/material/sidenav';

@Component({
  selector: 'app-stock-page',
  templateUrl: './stock-page.component.html',
  styleUrl: './stock-page.component.scss',
})
export class StockPageComponent {
  @ViewChild('sidenav') sidenav!: MatSidenav;
  toggleMatSidenav() {
    this.sidenav.toggle();
  }
}
