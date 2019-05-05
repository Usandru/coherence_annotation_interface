import { Component, OnInit, EventEmitter, Output } from '@angular/core';

@Component({
  selector: 'app-scale',
  templateUrl: './scale.component.html',
  styleUrls: ['./scale.component.scss']
})
export class ScaleComponent implements OnInit {

  constructor() { }

  options:Number;

  ngOnInit() {
  }

  @Output() confirm: EventEmitter<any> = new EventEmitter();
  onConfirm() {
    this.confirm.emit('scale_' + this.options.toString);
  }

}
