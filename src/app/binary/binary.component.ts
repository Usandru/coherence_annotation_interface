import { Component, OnInit, EventEmitter, Output } from '@angular/core';

@Component({
  selector: 'app-binary',
  templateUrl: './binary.component.html',
  styleUrls: ['./binary.component.scss']
})
export class BinaryComponent implements OnInit {

  constructor() { }

  args:string = "";

  ngOnInit() {
  }

  @Output() left: EventEmitter<any> = new EventEmitter();
    onLeftClick() {
      let now = new Date();
      let milisecs = now.getTime().toString();
      let comment:string;
      if (this.args === "") {
        comment = this.args;
      }
      else {
        comment = "///" + this.args
      }
      this.right.emit('binary_left' + "_" + milisecs + comment);
      this.args = "";
    }

    @Output() right: EventEmitter<any> = new EventEmitter();
    onRightClick() {
      let now = new Date();
      let milisecs = now.getTime().toString();
      let comment:string;
      if (this.args === "") {
        comment = this.args;
      }
      else {
        comment = "///" + this.args;
      }
      this.right.emit('binary_right' + "_" + milisecs + comment);
      this.args = "";
    }
}
