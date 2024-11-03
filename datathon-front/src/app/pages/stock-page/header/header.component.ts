import { Component, Output, EventEmitter } from '@angular/core';
@Component({
  selector: 'app-header',
  templateUrl: './header.component.html',
  styleUrl: './header.component.scss',
})
export class HeaderComponent {
  @Output() emitToggleDrawer = new EventEmitter<void>();
  public toggleDrawer() {
    this.emitToggleDrawer.emit();
  }
}
