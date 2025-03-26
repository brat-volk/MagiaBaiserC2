import importlib,os
from flask import Flask, send_file
app = Flask(__name__)


#MAIN FUNCTION
#load settings.json
#load modules(builder/listeners/more)
#start a thread for each listener
#start a thread for the web interface

def load_listeners(listener_dir):
    listeners = []
    listener_dir = listener_dir.replace("\\", ".")
    listener_dir = listener_dir.rstrip(".")
    
    for filename in os.listdir(listener_dir.replace('.', '\\')):
        if filename.endswith('.py') and not filename.startswith('_'):
            module_name = f"{listener_dir}.{filename[:-3]}"
            try:
                module = importlib.import_module(module_name)
                if hasattr(module, 'listener'):
                    listeners.append(module.listener())
            except ImportError as e:
                print(f"Failed to load {module_name}: {e}")
    return listeners


listeners = load_listeners('modules\\listeners')
for listener in listeners:
    listener.run()











@app.route('/')
def index():
    return send_file('dash.html')

@app.route('/agents')
def agentslist():
    concatenated_content = "["
    for filename in os.listdir("agents"):
        file_path = os.path.join("agents", filename)
        file_path = os.path.join(file_path, "agent.json")
        if os.path.isfile(file_path):
            with open(file_path, 'r', encoding='utf-8') as file:
                file_content = file.read()
                concatenated_content += file_content + ","  
    return concatenated_content[:len(concatenated_content)-1]+']'


@app.route('/<path:path>')
def serve(path):
    return send_file(path)

