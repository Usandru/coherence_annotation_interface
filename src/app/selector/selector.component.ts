import { Component, OnInit, EventEmitter, Output } from '@angular/core';

@Component({
  selector: 'app-selector',
  templateUrl: './selector.component.html',
  styleUrls: ['./selector.component.scss']
})
export class SelectorComponent implements OnInit {

  constructor() { }

//  selectSet;
  args: string;

/*   sets = [
    {id: 1, name:'set1'},
    {id: 2, name:'set2'},
]; */
  
  ngOnInit() {
  }

  @Output() startSession: EventEmitter<any> = new EventEmitter();
    onConfirm() {
        console.log(this.args) //this.selectSet.name + "_" + 
        this.startSession.emit(this.args); //this.selectSet.name + "_" + 
    }

  @Output() goBack: EventEmitter<any> = new EventEmitter();
    onBack() {
      this.goBack.emit("initial");
    }
  
}
