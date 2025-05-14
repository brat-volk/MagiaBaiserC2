
function loadAgentData(){
    document.getElementById("box").innerHTML = "HIIIIIIIIIIII!!!!!!!!!!!!!!!!!!! :3 I'm agent "+(agent_id)+"!!!! nyace to mweet youuuu!!!";
    let reply = httpPost('/query',"SELECT * FROM actions WHERE actions.implant_id="+agent_id+" ORDER BY actions.date");
    actions = JSON.parse(reply);
    history_box = document.getElementById('history_box');
    history_box.innerHTML = ''; 
    actions.forEach(action => history_box.innerHTML+='<li> '+ action + ' </li>');
}

function httpPost(url,query)
{
    var xmlHttp = new XMLHttpRequest();
    xmlHttp.open( "POST", url, false );
    xmlHttp.send(query);
    return xmlHttp.responseText;
}

document.addEventListener('DOMContentLoaded', function() {
    loadAgentData();
});