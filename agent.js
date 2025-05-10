function loadAgentData(){
    document.getElementById("box").innerHTML += document.getElementById("agent_id").innerText;
}

document.addEventListener('DOMContentLoaded', function() {
    loadAgentData();
});