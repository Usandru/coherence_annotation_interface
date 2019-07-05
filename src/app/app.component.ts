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
  State:String = 'selector';
  flask_serv_path:String = 'http://52.31.82.25:80/';


  constructor(private httpClient: HttpClient) {
    //nothing goes in this crime against programming
  }

  ngOnInit() {
  }

  annotate(evt) {
    this.httpClient.put(this.flask_serv_path + 'annotate', {'annotation': evt}).subscribe(nothing => {
    this.httpClient.get(this.flask_serv_path + 'annotate').subscribe(data => {
      this.ExperimentState = data as JSON;
      this.State = this.ExperimentState["InputMethod"];
      this.text1 = this.ExperimentState["LeftText"]
      this.text2 = this.ExperimentState["RightText"]
    })
  })
  }

  newSession(evt) {
    console.log(evt)
    this.httpClient.put(this.flask_serv_path + 'session', {'session': evt}).subscribe(nothing =>{
    this.httpClient.get(this.flask_serv_path + 'annotate').subscribe(data => {
      this.ExperimentState = data as JSON;
      this.State = this.ExperimentState["InputMethod"];
      this.text1 = this.ExperimentState["LeftText"]
      this.text2 = this.ExperimentState["RightText"]
    })
  })
  }
}
