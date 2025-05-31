var code_block = document.getElementById('code');

function httpPost(url,query)
{
  var xmlHttp = new XMLHttpRequest();
  xmlHttp.open( "POST", url, false );
  xmlHttp.send(query);
  return xmlHttp.responseText;
}

function deleteTask(){
  httpPost('/query',"DELETE FROM tasks WHERE tasks.id="+task_id);
  window.location.replace('../../')
}

function save(){
  var is_registered = JSON.parse(httpPost('/query',"SELECT COUNT(1) FROM tasks WHERE tasks.id="+task_id));
  if(is_registered[0]!=0){
    httpPost('/query',"UPDATE tasks SET content = '"+code_block.innerText+"' WHERE id="+task_id);
  }else{
    httpPost('/query',"INSERT INTO tasks (id, author, link, content, tags) VALUES (" + task_id + ",'LOCAL','LOCAL','"+code_block.innerText+"','meow')");
  }
}


document.addEventListener('DOMContentLoaded', function() {
  code_block.innerText = JSON.parse(httpPost('/query','SELECT tasks.content FROM tasks WHERE tasks.id = ' + task_id));
});