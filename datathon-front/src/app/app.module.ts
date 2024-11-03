import { NgModule } from '@angular/core';
import { BrowserModule, provideClientHydration } from '@angular/platform-browser';

import { AppRoutingModule } from './app-routing.module';
import { AppComponent } from './app.component';
import { StockListComponent } from './pages/landing-page/stock-list/stock-list.component';
import { InputBarComponent } from './pages/landing-page/input-bar/input-bar.component';

@NgModule({
  declarations: [
    AppComponent,
    StockListComponent,
    InputBarComponent
  ],
  imports: [
    BrowserModule,
    AppRoutingModule
  ],
  providers: [
    provideClientHydration()
  ],
  bootstrap: [AppComponent]
})
export class AppModule { }
