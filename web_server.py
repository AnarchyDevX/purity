from flask import Flask, request, jsonify
from flask_cors import CORS
import threading
import queue
import time

app = Flask(__name__)
CORS(app)

# Queue pour communiquer avec le bot
verification_queue = queue.Queue()

@app.route('/')
def index():
    return jsonify({"status": "online", "message": "Roblox Verification Server"})

@app.route('/verify', methods=['POST'])
def receive_verification():
    try:
        data = request.get_json()
        
        # Vérifier que les champs requis sont présents
        if not all(key in data for key in ['code', 'username']):
            return jsonify({"error": "Missing required fields"}), 400
        
        code = data.get('code')
        username = data.get('username')
        
        # Envoyer le code au bot via la queue
        verification_queue.put({
            'code': code,
            'username': username,
            'timestamp': time.time()
        })
        
        print(f"[WEB] Verification received: {code} for {username}")
        
        return jsonify({"status": "success", "message": "Verification code received"}), 200
        
    except Exception as e:
        print(f"[WEB] Error processing verification: {e}")
        return jsonify({"error": str(e)}), 500

def get_verification_queue():
    """Retourne la queue de vérification pour le bot"""
    return verification_queue

def run_server(host='0.0.0.0', port=5000):
    """Lance le serveur web dans un thread séparé"""
    def start_server():
        app.run(host=host, port=port, debug=False)
    
    thread = threading.Thread(target=start_server, daemon=True)
    thread.start()
    print(f"[WEB] Server started on http://{host}:{port}")
    return thread

if __name__ == '__main__':
    run_server()
    # Garder le script vivant
    while True:
        time.sleep(1)

