import importlib,os
from flask import Flask, send_file
app = Flask(__name__)


#MAIN FUNCTION
#load settings.json
#load modules(builder/listeners/more)
#start a thread for each listener
#start a thread for the web interface

#should i make an internal API and server for the actual implant registration and management instead of leaving it all in the listeners?
#maybe i can just set up the logic as an external .py file that i import into the listeners idk

def load_modules(module_dir):
    modules = []
    module_dir = module_dir.replace("\\", ".")
    module_dir = module_dir.rstrip(".")
    
    for filename in os.listdir(module_dir.replace('.', '\\')):
        if filename.endswith('.py') and not filename.startswith('_'):
            module_name = f"{module_dir}.{filename[:-3]}"
            try:
                module = importlib.import_module(module_name)
                if hasattr(module, 'module'):
                    modules.append(module.module())
            except ImportError as e:
                print(f"Failed to load {module_name}: {e}")
    return modules


listeners = load_modules('modules\\listeners')
for listener in listeners:
    listener.start()











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

