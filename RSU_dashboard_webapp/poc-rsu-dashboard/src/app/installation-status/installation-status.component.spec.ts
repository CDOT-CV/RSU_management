import { ComponentFixture, TestBed } from '@angular/core/testing';

import { InstallationStatusComponent } from './installation-status.component';

describe('InstallationStatusComponent', () => {
  let component: InstallationStatusComponent;
  let fixture: ComponentFixture<InstallationStatusComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [ InstallationStatusComponent ]
    })
    .compileComponents();
  });

  beforeEach(() => {
    fixture = TestBed.createComponent(InstallationStatusComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
