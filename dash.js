const agentList = document.getElementById('agentList');

let agents=[];


function refresh() {
    let reply = httpPost('/query',"SELECT * FROM implants");
    agents = JSON.parse(reply);
    agentList.innerHTML = '';
    agents.forEach(agent => agentList.innerHTML+='<a href=/agent/'+ agent[0] +'><button><li> '+ agent + ' </li></button></a>');
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

document.addEventListener('DOMContentLoaded', function() {
        refresh();
});