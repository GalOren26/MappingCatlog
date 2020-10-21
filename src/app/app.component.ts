import { Component } from '@angular/core';
import { Model } from '@models/model.dt';
import { LatLng, latLng } from 'leaflet';

@Component({
  selector: 'app-root',
  templateUrl: './app.component.html',
  styleUrls: ['./app.component.scss'],
})
export class AppComponent {
  title = 'map-selector';
}
