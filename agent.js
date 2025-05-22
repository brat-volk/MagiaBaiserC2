
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

function loadAgentData(){
    let reply = httpPost('/query',"SELECT * FROM actions WHERE actions.implant_id="+agent_id+" ORDER BY actions.date");
    actions = JSON.parse(reply);
    history_box = document.getElementById('history_box');
    history_box.innerHTML = ''; 
    actions.forEach(action => history_box.innerHTML+='<li> '+ action + ' </li>');
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

setInterval(loadAgentData, 5000);
document.addEventListener('DOMContentLoaded', function() {
    loadAgentData();
});

document.getElementById('Overview').style.display = 'block';
document.getElementsByClassName('tablinks')[0].className += ' active';