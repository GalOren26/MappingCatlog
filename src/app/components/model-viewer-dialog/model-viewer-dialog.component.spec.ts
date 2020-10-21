import { async, ComponentFixture, TestBed } from '@angular/core/testing';

import { ModelViewerDialogComponent } from './model-viewer-dialog.component';

describe('ModelViewerDialogComponent', () => {
  let component: ModelViewerDialogComponent;
  let fixture: ComponentFixture<ModelViewerDialogComponent>;

  beforeEach(async(() => {
    TestBed.configureTestingModule({
      declarations: [ ModelViewerDialogComponent ]
    })
    .compileComponents();
  }));

  beforeEach(() => {
    fixture = TestBed.createComponent(ModelViewerDialogComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
