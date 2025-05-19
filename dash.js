const agentList = document.getElementById('agentList');

let agents=[];

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
    let reply = httpPost('/query',"SELECT * FROM implants");
    agents = JSON.parse(reply);
    agentList.innerHTML = '';
    agents.forEach(agent => agentList.innerHTML+='<a href=/agent/'+ agent[0] +'><button><li> '+agent[0] + ' - ' + agent[4] + '\\' + agent[5] + (Math.abs(new Date() - new Date(agent[2].replace(/-/g,'/')))>30000?'<div class="offline">offline':'<div class="online">online') +'</div></li></button></a>');
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