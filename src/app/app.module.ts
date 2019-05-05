import { BrowserModule } from '@angular/platform-browser';
import { NgModule } from '@angular/core';

import { AppRoutingModule } from './app-routing.module';
import { AppComponent } from './app.component';

import { HttpClientModule } from '@angular/common/http';
import { SliderComponent } from './slider/slider.component';
import { BinaryComponent } from './binary/binary.component';
import { ScaleComponent } from './scale/scale.component';
import { SelectorComponent } from './selector/selector.component';
import { Ng5SliderModule } from 'ng5-slider';
import { FormsModule } from '@angular/forms';
import { AlertModule } from 'ngx-bootstrap';

@NgModule({
  declarations: [
    AppComponent,
    SliderComponent,
    BinaryComponent,
    ScaleComponent,
    SelectorComponent,
  ],
  imports: [
    BrowserModule,
    AppRoutingModule,
    Ng5SliderModule,
    HttpClientModule,
    AlertModule.forRoot(),
    FormsModule
  ],
  bootstrap: [AppComponent]
})
export class AppModule { }
