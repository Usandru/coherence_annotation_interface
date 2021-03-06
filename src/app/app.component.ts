import { Component, OnInit, ViewChild  } from '@angular/core';
//import { ApiService } from './services/api.service';
import { HttpClient } from '@angular/common/http';
import { ModalDirective } from 'ngx-bootstrap/modal';

@Component({
  selector: 'app-root',
  templateUrl: './app.component.html',
  styleUrls: ['./app.component.scss']
})
export class AppComponent implements OnInit {
  INITIAL_MODE = 'initial';
  SELECTOR_MODE = 'selector';
  BINARY_MODE = 'binary';
  SLIDER_MODE = 'slider';
  BREAK_MODE = 'break';
//  @ViewChild('coreGuideModal', { static: false }) coreGuideModal: ModalDirective;
  @ViewChild('coreGuideModal') coreGuideModal: ModalDirective;

  title = 'experiment';
  isCollapsed = true;
  admin_mode = true;

  // Client-side constants
  flask_serv_path:String = 'http://52.31.82.25:80/';

  // Variables relating to the current state of the client
  text1:String = '';
  text2:String = '';
  mode:String = 'initial';
  getUserMode:String;
  
  // Variables representing the session retrieved from the server
  ExperimentState:JSON;
  user_name:String;
  annotation_position = -1;
  annotation_length = -1;
  annotation_content:String[][];
  annotation_mode:String[];

  constructor(private httpClient: HttpClient) {
    //nothing goes in this crime against programming
  }

  ngOnInit() {
  }

  ngAfterViewInit(){
    this.coreGuideModal.show();
  }

  fetchSession(name) {
    this.httpClient.put(this.flask_serv_path + 'fetchsession', {'ID': name}).subscribe(userSession => {
      this.ExperimentState = userSession as JSON;
      this.annotation_content = this.ExperimentState["Content"];
      this.annotation_mode = this.ExperimentState["Mode"];
      this.annotation_position = this.ExperimentState["Position"];
      this.annotation_length = this.ExperimentState["Length"];

      this.user_name = name;

      if(this.annotation_position === this.annotation_length) {
        this.mode = this.BREAK_MODE;
      }
      else {
        this.updatePosition();
      }
    })
  }

  // utility function to handle the position state incrementing
  iteratePosition() {
    if(this.annotation_position >= this.annotation_length - 1) {
      this.annotation_position = this.annotation_length;
      this.text1 = ""
      this.text2 = ""
      this.mode = this.BREAK_MODE;
    }
    else {
      this.annotation_position = this.annotation_position + 1;
      this.updatePosition();
    }
  }

  // utility function to handle setting the state of the annotation session to the current position
  updatePosition() {
    this.text1 = this.annotation_content[this.annotation_position][0];
    this.text2 = this.annotation_content[this.annotation_position][1];
    this.pickMode(this.annotation_mode[this.annotation_position]);
  }

  // utility function that exists to ensure that the mode-strings are kept uniform when they are provided by the backend
  pickMode(mode_string) {
    switch(mode_string) {
      case 'slider':
        this.mode = this.SLIDER_MODE;
        break;
      case "binary":
        this.mode = this.BINARY_MODE;
        break;
      case "selector":
        this.mode = this.SELECTOR_MODE;
        break;
      case "initial":
        this.mode = this.INITIAL_MODE;
        break;
      default:
        console.log("switch mode error")

    }
  }

  // function called through initial.component, it sets a mode (either "new" or "existing") and switches the input mode to "selector"
  getUser(evt) {
    this.getUserMode = evt;
    this.mode = this.SELECTOR_MODE;
  }

  // utility function that switches to a different mode specified in the argument passed on by the specific component
  goBack(evt) {
    this.pickMode(evt);
  }

  newSession(evt) {
    switch(this.getUserMode) {
      case "new":
        if (this.admin_mode) {
          this.newUserParams(evt);
        }
        else {
          this.newUser(evt);
        }
        break;
      case "existing":
        this.fetchSession(evt);
    }
  }

  annotate(evt) {
    this.httpClient.put(this.flask_serv_path + 'annotate', {'ID': this.user_name, 'Content': evt, 'Position': this.annotation_position}).subscribe(nothing => {
      this.iteratePosition();
    })
  }

  newUser(name) {
    this.httpClient.put(this.flask_serv_path + 'generateuserdefault', {'ID': name}).subscribe(nothing => {
      //catch errors or something
      this.fetchSession(name);
    })
  }

  newUserParams(input:String) {
    let param_list = input.split(' ');
    let param_json = {
      "ID": param_list[0],
      "Group" : param_list[1],
      "Offset" : param_list[2],
      "Blocks" : param_list[3]
    }
    this.httpClient.put(this.flask_serv_path + 'generateuser', param_json).subscribe(nothing => {
      //do some error handling but this is admin only so lower priority
    })
  }

  extendSession() {
    this.httpClient.put(this.flask_serv_path + 'extendsession', {'ID': this.user_name}).subscribe(nothing => {
      //catch errors somehow
      this.fetchSession(this.user_name);
    })
  }

  extendUser(name) {
    this.httpClient.put(this.flask_serv_path + 'extenduser', {'ID': name}).subscribe(nothing => {
      //admin function to low-priority
    })
  }

}
