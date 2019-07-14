import { Component, OnInit, EventEmitter, Output } from '@angular/core';

@Component({
  selector: 'app-initial',
  templateUrl: './initial.component.html',
  styleUrls: ['./initial.component.scss']
})
export class InitialComponent implements OnInit {

  constructor() { }

  ngOnInit() {
  }

  @Output() getUser: EventEmitter<any> = new EventEmitter();
    newUser() {
      this.getUser.emit("new");
    }
    existingUser() {
      this.getUser.emit("existing");
  }

}
