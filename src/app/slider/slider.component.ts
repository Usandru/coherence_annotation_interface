import { Component, OnInit, EventEmitter, Output  } from '@angular/core';
import { Options, ChangeContext, PointerType } from 'ng5-slider';

@Component({
  selector: 'app-slider',
  templateUrl: './slider.component.html',
  styleUrls: ['./slider.component.scss']
})
export class SliderComponent implements OnInit {
  
  value: number = 0;
  options: Options = {
    floor: -100,
    ceil: 100,
    step: 0.1,
    hideLimitLabels: true,
    hidePointerLabels: true
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
    this.confirm.emit('slider_' + (this.value));
    this.value = 0
  }

}
