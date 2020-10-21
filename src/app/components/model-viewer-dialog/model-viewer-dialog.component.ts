import { Component, OnInit } from '@angular/core';
import { MatDialog } from '@angular/material/dialog';
import { DataService } from '@services/data.service';
import { Observable } from 'rxjs';
import { Model } from '@models/model.dt';

@Component({
  selector: 'app-model-viewer-dialog',
  templateUrl: './model-viewer-dialog.component.html',
  styleUrls: ['./model-viewer-dialog.component.scss'],
})
export class ModelViewerDialogComponent implements OnInit {
  constructor(private data: DataService) {}

  model: Model;
  selectedQuality = 'איכות בינונית';
  qualities = ['איכות נמוכה', 'איכות בינונית', 'איכות גבוהה'];

  ngOnInit(): void {
    this.data.getSelectedModel().subscribe((m) => (this.model = m));
  }

  onClick(): void {
    this.data.downloadCurrentModel(this.model, this.selectedQuality);
  }

  selectionChanged($event): void {
    this.selectedQuality = $event.source.value;
  }
}
