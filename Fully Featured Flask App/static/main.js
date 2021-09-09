document.querySelector('.message').style.background = "none";
var tds = document.getElementsByTagName("td");
var ths = document.getElementsByTagName("th");
sun = document.querySelector("#sun")
moon = document.querySelector("#moon")
body = document.querySelector("body")


if (window.localStorage.getItem('theme') == 'light') {
  
  for(var i = 0, j = tds.length; i < j; ++i){
    tds[i].style.color = "black";
  }
    
  for(var i = 0, j = ths.length; i < j; ++i){
    ths[i].style.color = "black";
  }
  sun.style.display = "block";
  moon.style.display = "none";
  body.style.background = '#fff';
  body.style.color = "#24252e";  
  
} else {
  for(var i = 0, j = tds.length; i < j; ++i){
       tds[i].style.color = "white";
  }
    
  for(var i = 0, j = ths.length; i < j; ++i){
    ths[i].style.color = "white";
  }
  sun.style.display = "none"
  moon.style.display = "block"
  moon.style.color = "#fff"
  moon.style.background = "black"
  body.style.background = "#24252a"
  body.style.color = "#fff"
 
}


function change(){
  if ((moon.style.display == "none") && (sun.style.display == "block")) {
   
    sun.style.display = "none"
    moon.style.display = "block"
    moon.style.color = "#fff"
    moon.style.background = "black"
    body.style.background = "#24252a"
    body.style.color = "#fff"
    window.localStorage.clear()
    window.localStorage.setItem('theme', 'dark')
    for(var i = 0, j = tds.length; i < j; ++i){
       tds[i].style.color = "#fff";
    }
      
   for(var i = 0, j = ths.length; i < j; ++i){
      ths[i].style.color = "#fff";
   }
    
}   
else {
    
    
    sun.style.display = "block";
    moon.style.display = "none";
    body.style.background = '#fff';
    body.style.color = "#24252e";
    window.localStorage.clear()
    window.localStorage.setItem('theme', 'light')    
    document.querySelector('.message').style.background = "none" 
    for(var i = 0, j = tds.length; i < j; ++i){
       tds[i].style.color = "black";
    }
      
    for(var i = 0, j = ths.length; i < j; ++i){
       ths[i].style.color = "black";
    } 

  }
};