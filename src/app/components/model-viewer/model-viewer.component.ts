import { Component, OnInit, Input } from '@angular/core';
import { DataService } from '@services/data.service';
import { Observable } from 'rxjs';
import { Model } from '@models/model.dt';

@Component({
  selector: 'app-model-viewer',
  templateUrl: './model-viewer.component.html',
  styleUrls: ['./model-viewer.component.scss'],
})
export class ModelViewerComponent implements OnInit {
  constructor(private data: DataService) {}

  model: Observable<Model>;

  ngOnInit(): void {
    this.model = this.data.getSelectedModel();
  }
}
