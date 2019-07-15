import { Component, OnInit, EventEmitter, Output  } from '@angular/core';

@Component({
  selector: 'app-session-break',
  templateUrl: './session-break.component.html',
  styleUrls: ['./session-break.component.scss']
})
export class SessionBreakComponent implements OnInit {

  constructor() { }

  ngOnInit() {
  }

  @Output() extendSession: EventEmitter<any> = new EventEmitter();
    continue() {
        this.extendSession.emit();
    }

  @Output() goBack: EventEmitter<any> = new EventEmitter();
    onBack() {
      this.goBack.emit("initial");
    }

}
