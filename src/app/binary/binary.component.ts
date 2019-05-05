import { Component, OnInit, EventEmitter, Output } from '@angular/core';

@Component({
  selector: 'app-binary',
  templateUrl: './binary.component.html',
  styleUrls: ['./binary.component.scss']
})
export class BinaryComponent implements OnInit {

  constructor() { }

  ngOnInit() {
  }

  @Output() left: EventEmitter<any> = new EventEmitter();
    onLeftClick() {
        this.left.emit('binary_left');
    }

    @Output() right: EventEmitter<any> = new EventEmitter();
    onRightClick() {
        this.right.emit('binary_right');
    }
}
