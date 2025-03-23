import os
from flask import Flask, send_file
app = Flask(__name__)

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

