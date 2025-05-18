const agentList = document.getElementById('agentList');

let agents=[];


function refresh() {
    let reply = httpPost('/query',"SELECT * FROM implants");
    agents = JSON.parse(reply);
    agentList.innerHTML = '';
    agents.forEach(agent => agentList.innerHTML+='<a href=/agent/'+ agent[0] +'><button><li> '+agent[0] + ' - ' + agent[4] + '\\' + agent[5] + (Math.abs(new Date() - new Date(agent[2].replace(/-/g,'/')))>30000?'<div class="offline">offline':'<div class="online">online') +'</div></li></button></a>');
}
function panic() {
    document.getElementById('body').innerHTML ='PANIC';
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