import { async, ComponentFixture, TestBed } from '@angular/core/testing';

import { SessionBreakComponent } from './session-break.component';

describe('SessionBreakComponent', () => {
  let component: SessionBreakComponent;
  let fixture: ComponentFixture<SessionBreakComponent>;

  beforeEach(async(() => {
    TestBed.configureTestingModule({
      declarations: [ SessionBreakComponent ]
    })
    .compileComponents();
  }));

  beforeEach(() => {
    fixture = TestBed.createComponent(SessionBreakComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
