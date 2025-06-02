
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

function loadHistory(){
  let reply = httpPost('/query',"SELECT * FROM actions WHERE actions.implant_id="+agent_id+" ORDER BY actions.date");
  actions = JSON.parse(reply);
  history_box = document.getElementById('history_box');
  history_box.innerHTML = ''; 
  actions.forEach(action => history_box.innerHTML+='<li> '+ action + ' </li>');
}

function loadTasks(){
  let r1 = httpPost('/query',"SELECT tasks.*, implant_task.id, implant_task.executed FROM tasks, implant_task WHERE implant_task.task_id = tasks.id AND implant_task.implant_id="+agent_id+" ORDER BY implant_task.id");
  implant_tasks = JSON.parse(r1);
  task_box = document.getElementById('task_box');
  task_box.innerHTML = ''; 
  implant_tasks.forEach(task => task_box.innerHTML+='<li'+(task[6]?' class="executed">':'>')+ task + '<button onclick="deleteTask('+task[5]+')" class="offline">-</button></li>');
  var tmp='<li><select id="new_task">';
  let r2 = httpPost('/query',"SELECT * FROM tasks ORDER BY tasks.id ASC");
  tasks = JSON.parse(r2);
  tasks.forEach(task => tmp+='<option id="'+ task[0] + '">'+task[0]+' </option>');
  tmp+='</select><button onclick=addTask()>+</button></li>';
  task_box.innerHTML+=tmp;
}

function addTask(){
  var meow = document.getElementById("new_task").value;
  var time = httpPost('/time','');
  httpPost('/query',"INSERT INTO implant_task (implant_id, task_id, date, executed) VALUES (" + agent_id + ","+meow+",'"+time+"',0)");
  loadTasks();
}
function deleteTask(id){
  httpPost('/query',"DELETE FROM implant_task WHERE implant_task.id="+id);
  loadTasks();
}

function deleteAgent(){
  httpPost('/query',"DELETE FROM actions WHERE actions.implant_id="+agent_id);
  httpPost('/query',"DELETE FROM implants WHERE implants.id="+agent_id);
  httpPost('/query',"DELETE FROM implant_task WHERE implant_task.implant_id="+agent_id);
  window.location.replace('../../')
}

function httpPost(url,query)
{
  var xmlHttp = new XMLHttpRequest();
  xmlHttp.open( "POST", url, false );
  xmlHttp.send(query);
  return xmlHttp.responseText;
}

setInterval(loadHistory, 5000);
document.addEventListener('DOMContentLoaded', function() {
  loadHistory();
  loadTasks();
});

document.getElementById('Overview').style.display = 'block';
document.getElementsByClassName('tablinks')[0].className += ' active';