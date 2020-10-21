import { Component, OnInit, NgZone } from '@angular/core';
import {
  MapOptions,
  tileLayer,
  latLng,
  polygon,
  Map,
  Layer,
  LatLng,
  LeafletMouseEvent,
  Polygon,
} from 'leaflet';
import { DataService } from '@services/data.service';
import { Observable } from 'rxjs';
import { Model } from '@models/model.dt';
import { MatDialog } from '@angular/material/dialog';
import { ModelViewerDialogComponent } from '@components/model-viewer-dialog/model-viewer-dialog.component';

@Component({
  selector: 'app-map-viewer',
  templateUrl: './map-viewer.component.html',
  styleUrls: ['./map-viewer.component.scss'],
})
export class MapViewerComponent implements OnInit {
  polygons: Polygon[] = [];
  models: Model[];
  map: Map;
  center: LatLng;
  options: MapOptions = {
    layers: [
      tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
        maxZoom: 18,
        attribution:
          '© <a href="https://www.openstreetmap.org/">OpenStreetMap</a> contributors | Made for Masada',
      }),
    ],
    zoom: 10,
    center: latLng(31.76832, 35.22333),
  };

  models$: Observable<Model[]>;

  constructor(
    private data: DataService,
    public dialog: MatDialog,
    private zone: NgZone
  ) {}

  ngOnInit(): void {
    this.models$ = this.data.getAllModels();
  }

  onMapReady($event): void {
    this.map = $event;
    this.models$.subscribe((models) => {
      this.models = models;
      models
        .map((m) => m.coordinates)
        .forEach((coors) => {
          const poly: Polygon<any> = polygon(coors, {
            color: 'black',
          }).on('click', this.onClick.bind(this));
          this.polygons.push(poly);
          this.map.addLayer(poly);
        });
    });
    this.data.getSelectedModel().subscribe((model) => {
      console.log(this.polygons);
      const poly: Polygon = this.polygons.find((p) =>
        p.getLatLngs()[0][0].equals(model.coordinates[0])
      );
      this.zone.run(() => {
        if (poly !== undefined) {
          this.map.fitBounds(poly.getBounds());
        }
      });
    });
  }

  /**
   * onClick($event)
   * @param $event - The event returning when clicking on a layer.
   * returning the Model the layer represents.
   * known issue: only check for the first coordinate to be equal
   * which means this solution will not work if the following happens:
   * a. the coordinates aren't in the same order (arrays must be sorted).
   * b. there's more than one model with the same coordinate.
   */
  onClick($event: LeafletMouseEvent): void {
    const clickedModel = this.models.find((model) =>
      latLng(model.coordinates[0]).equals($event.target.getLatLngs()[0][0])
    );
    this.data.setSelectedModel(clickedModel);
    this.openDialog();
  }

  openDialog(): void {
    const dialogRef = this.dialog.open(ModelViewerDialogComponent, {
      width: '80%',
      height: '80%',
    });

    dialogRef.afterClosed().subscribe((result) => {
      console.log(`Dialog result: ${result}`);
    });
  }
}
