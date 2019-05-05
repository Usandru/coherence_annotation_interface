import { Component, OnInit, EventEmitter, Output } from '@angular/core';

@Component({
  selector: 'app-selector',
  templateUrl: './selector.component.html',
  styleUrls: ['./selector.component.scss']
})
export class SelectorComponent implements OnInit {

  constructor() { }

  selectSet;
  args: string;

  sets = [
    {id: 1, name:'set1'},
    {id: 2, name:'set2'},
];
  
  ngOnInit() {
  }

  @Output() startSession: EventEmitter<any> = new EventEmitter();
    onConfirm() {
        console.log(this.selectSet.name + "_" + this.args)
        this.startSession.emit(this.selectSet.name + "_" + this.args);
    }

  
}
