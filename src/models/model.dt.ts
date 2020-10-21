import { LatLngExpression } from 'leaflet';

export interface Model {
  name: string;
  engName: string;
  coordinates: LatLngExpression[];
  url: string;
}
