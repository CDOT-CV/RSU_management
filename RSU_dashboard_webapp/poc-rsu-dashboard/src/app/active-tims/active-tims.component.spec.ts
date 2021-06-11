import { ComponentFixture, TestBed } from '@angular/core/testing';

import { ActiveTIMsComponent } from './active-tims.component';

describe('ActiveTIMsComponent', () => {
  let component: ActiveTIMsComponent;
  let fixture: ComponentFixture<ActiveTIMsComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [ ActiveTIMsComponent ]
    })
    .compileComponents();
  });

  beforeEach(() => {
    fixture = TestBed.createComponent(ActiveTIMsComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
