import { Component, OnInit } from '@angular/core';
//import { ApiService } from './services/api.service';
import { HttpClient } from '@angular/common/http';

@Component({
  selector: 'app-root',
  templateUrl: './app.component.html',
  styleUrls: ['./app.component.scss']
})
export class AppComponent implements OnInit {
  title = 'experiment';
  isCollapsed = true;

  text1:String = '';
  text2:String = '';
  ExperimentState:JSON;
  mode:String = 'selector';
  flask_serv_path:String = 'http://52.31.82.25:80/';

  user_name:String;
  annotation_position = -1;
  annotation_length = -1;
  annotation_content:String[][];
  annotation_mode:String[];

  somenumber = 0;

  constructor(private httpClient: HttpClient) {
    //nothing goes in this crime against programming
  }

  ngOnInit() {
  }

  fetchSession(name) {
    this.httpClient.put(this.flask_serv_path + 'fetchsession', {'Identity': name}).subscribe(userSession => {
      this.ExperimentState = userSession as JSON;
      this.annotation_content = this.ExperimentState["Content"];
      this.annotation_mode = this.ExperimentState["Mode"];
      this.annotation_position = this.ExperimentState["Position"];
      this.annotation_length = this.ExperimentState["Length"];

      this.updatePosition();
    })
  }

  updatePosition() {
    this.text1 = this.annotation_content[this.annotation_position][0];
    this.text2 = this.annotation_content[this.annotation_position][1];
    this.mode = this.annotation_mode[this.annotation_position];
  }

  annotate(evt) {
    this.httpClient.put(this.flask_serv_path + 'annotate', {'ID': this.user_name, 'Content': evt, 'Position': this.annotation_position}).subscribe(nothing => {
      this.annotation_position = this.annotation_position + 1;
      this.updatePosition();
    })
  }

  newSession(evt) {
    console.log(evt)
    this.httpClient.put(this.flask_serv_path + 'session', {'session': evt}).subscribe(nothing =>{
    this.httpClient.get(this.flask_serv_path + 'annotate').subscribe(data => {
      this.ExperimentState = data as JSON;
      this.mode = this.ExperimentState["InputMethod"];
      this.text1 = this.ExperimentState["LeftText"]
      this.text2 = this.ExperimentState["RightText"]
    })
  })
  }
}
