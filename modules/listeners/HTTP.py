from flask import Flask, request
import threading

class FlaskListener:
    def __init__(self, host='0.0.0.0', port=80):
        self.host = host
        self.port = port
        self.app = Flask(__name__)
        self.setup_routes()

    def setup_routes(self):
        @self.app.route('/')
        def index():
            return "Flask listener is running!"

        @self.app.route('/api', methods=['POST'])
        def handle_post():
            data = request.json
            print(f"Received POST data: {data}")
            return {"status": "success"}, 200

    def run(self):
        try:
            # Run in a separate thread to avoid blocking
            thread = threading.Thread(
                target=self.app.run,
                kwargs={'host': self.host, 'port': self.port, 'use_reloader': False}
            )
            thread.daemon = True
            thread.start()
            print(f"Flask listener started on {self.host}:{self.port}")
        except Exception as e:
            print(f"Failed to start Flask listener: {e}")

def listener():
    return FlaskListener(host='127.0.0.1', port=80)  # Customize as needed