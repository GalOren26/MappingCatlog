import { BrowserModule } from '@angular/platform-browser';
import { NgModule, CUSTOM_ELEMENTS_SCHEMA } from '@angular/core';

import { AppRoutingModule } from './app-routing.module';
import { AppComponent } from './app.component';
import { BrowserAnimationsModule } from '@angular/platform-browser/animations';
import { ModelListComponent } from './components/model-list/model-list.component';
import { ModelViewerComponent } from './components/model-viewer/model-viewer.component';
import { MatListModule } from '@angular/material/list';
import { MatCardModule } from '@angular/material/card';
import { MatButtonModule } from '@angular/material/button';
import { FlexLayoutModule } from '@angular/flex-layout';
import { MatDialogModule } from '@angular/material/dialog';
import { MatSelectModule } from '@angular/material/select';
import { MatFormFieldModule } from '@angular/material/form-field';
import { LeafletModule } from '@asymmetrik/ngx-leaflet';
import { MapViewerComponent } from './components/map-viewer/map-viewer.component';
import { ModelViewerDialogComponent } from './components/model-viewer-dialog/model-viewer-dialog.component';
import { HttpClientModule } from '@angular/common/http';
@NgModule({
  declarations: [
    AppComponent,
    ModelListComponent,
    ModelViewerComponent,
    MapViewerComponent,
    ModelViewerDialogComponent,
  ],
  imports: [
    BrowserModule,
    AppRoutingModule,
    BrowserAnimationsModule,
    LeafletModule,
    FlexLayoutModule,
    MatListModule,
    MatCardModule,
    MatButtonModule,
    MatDialogModule,
    MatSelectModule,
    MatFormFieldModule,
    HttpClientModule,
  ],
  providers: [],
  bootstrap: [AppComponent],
  schemas: [CUSTOM_ELEMENTS_SCHEMA],
})
export class AppModule {}
