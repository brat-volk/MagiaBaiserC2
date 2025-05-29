import importlib,os,sqlite3,datetime
from flask import Flask, request, send_file,jsonify
app = Flask(__name__)


#MAIN FUNCTION
#load settings.json
#load modules(builder/listeners/more)
#start a thread for each listener
#start a thread for the web interface

#should i make an internal API and server for the actual implant registration and management instead of leaving it all in the listeners?
#maybe i can just set up the logic as an external .py file that i import into the listeners idk

con = sqlite3.connect(".db", check_same_thread=False)
cur = con.cursor()
start_time = datetime.datetime.now()

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
    return send_file('dash/dash.html')


@app.route('/uptime',methods=['POST'])
def uptime():
    return str(datetime.datetime.now() - start_time)[:-7]

@app.route('/query',  methods=['POST'])
def query_db():
    query = request.get_data(as_text=True)
    print(f"Executing query: {query}")
    
    with con:
        cur.execute(query)
        if query.strip().lower().startswith('select'):
            results = cur.fetchall()
            print(f"Executing query: {results}")
            return jsonify(results)
        return jsonify({"status": "success"})

@app.route('/agent/<string:id>/')
def agent(id):
    return send_file('agent/agent.html')
@app.route('/task/<string:id>/')
def task(id):
    return send_file('task/task.html')

@app.route('/agent/<string:id>/agent.js')
def agentjs(id):
    with open('agent/agent.js') as f:
        meow= f.read()
    return 'var agent_id='+id+';'+meow
@app.route('/task/<string:id>/task.js')
def taskjs(id):
    with open('task/task.js') as f:
        meow= f.read()
    return 'var task_id='+id+';'+meow

@app.route('/<path:target>/<string:id>/<path:path>')
def send_template(target,id,path):
    return send_file(target +'/'+ path)

@app.route('/<path:path>')
def serve(path):
    return send_file('dash/'+path)

