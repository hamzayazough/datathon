import { NgModule } from '@angular/core';
import {
  BrowserModule,
  provideClientHydration,
} from '@angular/platform-browser';

import { AppRoutingModule } from './app-routing.module';
import { AppComponent } from './app.component';
import { StockListComponent } from './pages/landing-page/stock-list/stock-list.component';
import { InputBarComponent } from './pages/landing-page/input-bar/input-bar.component';
import { StockPageComponent } from './pages/stock-page/stock-page/stock-page.component';
import { PageContentComponent } from './pages/stock-page/page-content/page-content.component';
import { MatSidenavModule } from '@angular/material/sidenav';
import { MatButtonModule } from '@angular/material/button';
import { ChatComponent } from './pages/stock-page/chat/chat.component';
import { provideAnimationsAsync } from '@angular/platform-browser/animations/async';
import { HeaderComponent } from './pages/stock-page/header/header.component';
import { MatIconModule } from '@angular/material/icon';
import { FormsModule } from '@angular/forms';
import { MatProgressSpinnerModule } from '@angular/material/progress-spinner';
import { HttpClientModule } from '@angular/common/http';

import { HomePageComponent } from './pages/home-page/home-page/home-page.component';
import { StockSearchComponent } from './pages/home-page/search-bar/search-bar.component';
import { ReactiveFormsModule } from '@angular/forms';
import { HttpClientModule } from '@angular/common/http';
const matModules = [
  MatSidenavModule,
  MatButtonModule,
  MatIconModule,
  FormsModule,
  MatProgressSpinnerModule,
];
@NgModule({
  declarations: [
    AppComponent,
    StockListComponent,
    InputBarComponent,
    StockPageComponent,
    PageContentComponent,
    ChatComponent,
    HeaderComponent,
    HomePageComponent,
    // SearchBarComponent,
    StockSearchComponent,
  ],
  imports: [
    BrowserModule,
    AppRoutingModule,
    ReactiveFormsModule,
    HttpClientModule,
    HttpClientModule,
    ...matModules,
  ],
  providers: [provideClientHydration(), provideAnimationsAsync()],
  bootstrap: [AppComponent],
})
export class AppModule {}
