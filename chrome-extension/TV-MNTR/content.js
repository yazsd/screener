var i = 1;
delay_ms = 1000
reload_sec = 1
reload_min = [58,28]


function sendGetReq(ts, bs)
{
  try {
    var url = `http://localhost/data?ts=${ts}&bs=${bs}`
    var xmlHttp = new XMLHttpRequest();
    xmlHttp.open( "GET", url, false ); // false for synchronous request
    xmlHttp.send( null );
    return xmlHttp.responseText;
  }
  catch(err) {
    console.log(err.message)
  }
}

function sendPostReq(jsonData){
  var xhr = new XMLHttpRequest();
  var url = "http://localhost:8000/webhook";
  xhr.open("POST", url, true);
  xhr.setRequestHeader("Content-Type", "application/json");
  xhr.onreadystatechange = function () {
      if (xhr.readyState === 4 && xhr.status === 200) {
          var json = JSON.parse(xhr.responseText);
          console.log(json.email + ", " + json.password);
      }
  };
  var data = JSON.stringify({"bs": jsonData});
  xhr.send(data);
}

function entry_or_exit(lt){
  lt_sp = lt.split('</td>')
  rv = 'X'
  for(idx in lt_sp){
      val = lt_sp[idx]
      if(val.includes('trade-x-price')){
          if(val.includes('&nbsp;')){
              rv = 'E'
          }
      } 
  }
  return rv
}

function long_or_short(lt){
  r = 'U'
  el_idx = lt.indexOf('Entry Long')
  xl_idx = lt.indexOf('Exit Long')
  es_idx = lt.indexOf('Entry Short')
  xs_idx = lt.indexOf('Exit Short')
  if((es_idx > -1) || (xs_idx > -1)){
      r = 'S'
  }
  if((el_idx > -1) || (xl_idx > -1)){
      r = 'L'
  }
  return r
}

function extractData(){
  try {
    lt=document.getElementsByTagName('tbody')[0].innerHTML
    ee = entry_or_exit(lt)
    xl = long_or_short(lt)
    pos = ee+xl
    console.log(`pos: ${pos}`)
    return pos
  }
  catch(err) {
    console.log(err.message)
  }
}

function reloadCheck(){
  currentMinute = new Date().getUTCMinutes()
  currentSecond = new Date().getUTCSeconds()
  console.log(`Minute: ${currentMinute}, Seconds: ${currentSecond}`)
  if((currentSecond <= reload_sec) && (reload_min.includes(currentMinute))){
    window.location.reload();
  }
}


function mainLoop() {      
  setTimeout(function() {
    console.log(i);
    i++;
    reloadCheck()      
    bs = extractData();
    ts = JSON.stringify(new Date().toLocaleString())
    if(bs){
      sendGetReq(ts, bs)
    }
    if (true) {        
      mainLoop();          
    }                    
  }, delay_ms)
}

mainLoop(); 
