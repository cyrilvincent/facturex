import { Component } from '@angular/core';
import { FormControl, FormGroup, Validators } from '@angular/forms';
import { HttpClient, HttpHeaders} from '@angular/common/http'

@Component({
  selector: 'app-root',
  templateUrl: './app.component.html',
  styleUrls: ['./app.component.scss']
})
export class AppComponent {
  myFiles:string [] = [];
  res: any = null
  
   myForm = new FormGroup({
    name: new FormControl('', [Validators.required, Validators.minLength(3)]),
    file: new FormControl('', [Validators.required])
  });
    
  constructor(private http: HttpClient) { }
      
  get f(){
    return this.myForm.controls;
  }

  get date() {
    return new Date();
  }

  

  
     
  onFileChange(event:any) {
        for (var i = 0; i < event.target.files.length; i++) { 
            this.myFiles.push(event.target.files[i]);
        }
  }
      
  submit(){
    console.log("submit")
    const formData = new FormData();
 
    for (var i = 0; i < this.myFiles.length; i++) { 
      formData.append("file[]", this.myFiles[i]);
    }
  
    const httpOptions = {
      headers: new HttpHeaders({ 
        'Access-Control-Allow-Origin':'*',
      })
    };
    
    this.http.post('http://localhost:5000/upload', formData, httpOptions)
      .subscribe(res => {
        console.log(res);
        this.res = res;

      })
  }
}
