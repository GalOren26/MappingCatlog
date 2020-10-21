import { Component, OnInit, Output, EventEmitter } from '@angular/core';
import { Model } from '@models/model.dt';
import { DataService } from '@services/data.service';
import { Observable } from 'rxjs';
@Component({
  selector: 'app-model-list',
  templateUrl: './model-list.component.html',
  styleUrls: ['./model-list.component.scss'],
})
export class ModelListComponent implements OnInit {
  models: Observable<Model[]>;
  selectedModel: Observable<Model>;
  constructor(private data: DataService) {}

  onModelChange($event: Model): void {
    this.data.setSelectedModel($event);
  }

  ngOnInit(): void {
    this.models = this.data.getAllModels();
    this.selectedModel = this.data.getSelectedModel();
  }
}
