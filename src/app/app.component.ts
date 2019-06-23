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


  constructor(private httpClient: HttpClient) {
    //nothing goes in this crime against programming
  }

  ngOnInit() {
  }

  annotate(evt) {
    this.httpClient.put('http://127.0.0.1:5002/annotate', {'annotation': evt}).subscribe(nothing => {
    this.httpClient.get('http://127.0.0.1:5002/annotate').subscribe(data => {
      this.ExperimentState = data as JSON;
      this.State = this.ExperimentState["InputMethod"];
      this.text1 = this.ExperimentState["LeftText"]
      this.text2 = this.ExperimentState["RightText"]
    })
  })
  }

  newSession(evt) {
    console.log(evt)
    this.httpClient.put('http://127.0.0.1:5002/session', {'session': evt}).subscribe(nothing =>{
    this.httpClient.get('http://127.0.0.1:5002/annotate').subscribe(data => {
      this.ExperimentState = data as JSON;
      this.State = this.ExperimentState["InputMethod"];
      this.text1 = this.ExperimentState["LeftText"]
      this.text2 = this.ExperimentState["RightText"]
    })
  })
  }
}
