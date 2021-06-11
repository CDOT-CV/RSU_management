import { NgModule } from '@angular/core';
import { BrowserModule } from '@angular/platform-browser';

import { AppComponent } from './app.component';
import { SidebarModule } from 'ng-sidebar';
import { TotalCountComponent } from './total-count/total-count.component';
import { ActiveTIMsComponent } from './active-tims/active-tims.component';
import { InstallationStatusComponent } from './installation-status/installation-status.component';

@NgModule({
  declarations: [
    AppComponent,
    TotalCountComponent,
    ActiveTIMsComponent,
    InstallationStatusComponent
  ],
  imports: [
    BrowserModule, SidebarModule.forRoot()
  ],
  providers: [],
  bootstrap: [AppComponent]
})
export class AppModule { }
