from flask import Flask, request, jsonify, send_file
from werkzeug.serving import make_server
import threading, json, datetime

class HTTPListener:
    def __init__(self):
        with open('modules/listeners/HTTP.json') as f:
            cfg = json.load(f)

        self.host = cfg["host"]
        self.port = cfg["port"]
        self.app = Flask(__name__)
        self.server = None
        
        self.app.add_url_rule('/register','register',self.register, methods=['POST'])
        self.app.add_url_rule('/<agent_id>/tasks', 'get_tasks', self.get_tasks, methods=['GET'])
        self.app.add_url_rule('/<agent_id>/tasks', 'post_tasks', self.post_tasks, methods=['POST'])
        self.app.add_url_rule('/<agent_id>/results', 'post_results', self.post_results, methods=['POST'])

    class ServerThread(threading.Thread):
        def __init__(self, app, host, port):
            threading.Thread.__init__(self)
            self.srv = make_server(host, port, app)
            self.ctx = app.app_context()
            self.ctx.push()

        def run(self):
            self.srv.serve_forever()

        def shutdown(self):
            self.srv.shutdown()

    def get_tasks(self, agent_id):
        with open("agents/" + agent_id + "/.tasks","r") as f:
            tasks= f.read()
        if tasks!="":
            self.update_history(agent_id, "task_retrieved", tasks)
        with open("agents/" + agent_id + "/.tasks","w") as f:
            f.write("")
        return tasks
    
    def update_history(self, agent_id, action_type, content):
        with open('agents/'+ agent_id +'/.history') as f:
            data = json.load(f)
        data["actions"].append({"timestamp":str(datetime.datetime.now()), "action_type":action_type, "content":content})
        with open('agents/'+ agent_id +'/.history', 'w') as f:
            json.dump(data, f)


    def post_tasks(self, agent_id):
        return "meowmeowmeowmeow :3"

    def post_results(self, agent_id):        
        return "meowmeowmeowmeow :3"
    
    def register(self):
        return

    def start(self):
        if not self.server:
            self.server = self.ServerThread(self.app, self.host, self.port)
            self.server.start()
            print(f"[*] HTTP listener started on {self.host}:{self.port}")

    def stop(self):
        if self.server:
            self.server.shutdown()
            self.server.join()
            self.server = None
            print("[*] HTTP listener stopped")
    

def module():
    return HTTPListener();



