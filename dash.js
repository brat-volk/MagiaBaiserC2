const agentList = document.getElementById('agentList');

let agents=[];


function refresh() {
    let reply = httpGet('/agents');
    agents = JSON.parse(reply);
    agentList.innerHTML = '';
    agents.forEach(agent => agentList.innerHTML+='<li> '+ agent.id + ' - '+ agent.os + ' - ' + agent.domain + ' </li>');
}
function panic() {
    document.getElementById('body').innerHTML ='PANIC';
}
function httpGet(theUrl)
{
    var xmlHttp = new XMLHttpRequest();
    xmlHttp.open( "GET", theUrl, false );
    xmlHttp.send( null );
    return xmlHttp.responseText;
}

document.addEventListener('DOMContentLoaded', function() {
        refresh();
});