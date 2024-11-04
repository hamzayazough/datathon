import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';
import { StockPageComponent } from './pages/stock-page/stock-page/stock-page.component';
import { HomePageComponent } from './pages/home-page/home-page/home-page.component';

const routes: Routes = [{ path: 'stock/:ticker', component: StockPageComponent }, { path: '', component: HomePageComponent}];

@NgModule({
  imports: [RouterModule.forRoot(routes)],
  exports: [RouterModule],
})
export class AppRoutingModule {}
