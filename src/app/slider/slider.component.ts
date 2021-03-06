import { Component, OnInit, EventEmitter, Output  } from '@angular/core';
import { Options, ChangeContext, PointerType } from 'ng5-slider';

@Component({
  selector: 'app-slider',
  templateUrl: './slider.component.html',
  styleUrls: ['./slider.component.scss']
})
export class SliderComponent implements OnInit {
  
  args:string = "";
  value: number = 0;
  options: Options = {
    floor: -100,
    ceil: 100,
    step: 0.1,
    hideLimitLabels: true,
    hidePointerLabels: true,
    ticksArray: [-100, -50, 0, 50, 100],
    getLegend: (value: number): string => {
      if(value === -100) {
        return 'Meget';
      }
      if (value === -50) {
        return 'Mellem';
      }
      if(value === 0) {
        return 'Start';
      }
      if(value === 100) {
        return 'Meget';
      }
      if (value === 50) {
        return 'Mellem';
      }
    }
  }

  logText: string = '';

  onUserChangeStart(changeContext: ChangeContext): void {
    this.logText += `onUserChangeStart(${this.getChangeContextString(changeContext)})\n`;
  }

  onUserChange(changeContext: ChangeContext): void {
    this.logText += `onUserChange(${this.getChangeContextString(changeContext)})\n`;
  }

  onUserChangeEnd(changeContext: ChangeContext): void {
    this.logText += `onUserChangeEnd(${this.getChangeContextString(changeContext)})\n`;
  }

  getChangeContextString(changeContext: ChangeContext): string {
    return `{pointerType: ${changeContext.pointerType === PointerType.Min ? 'Min' : 'Max'}, ` +
           `value: ${changeContext.value}, ` +
           `highValue: ${changeContext.highValue}}`;
  }

  ngOnInit() {
  }

  @Output() confirm: EventEmitter<any> = new EventEmitter();
  onConfirm() {
    let now = new Date();
    let milisecs = now.getTime().toString();
    let comment:string;
      if (this.args === "") {
        comment = this.args;
      }
      else {
        comment = "///" + this.args;
      }
    this.confirm.emit('slider_' + (this.value) + '_' + milisecs + comment);
    this.value = 0;
    this.args = "";
  }

}
