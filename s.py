from flask import Flask, request, jsonify
from flask_cors import CORS
import sqlite3

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "https://drajdeep.github.io"}})

DATABASE = 'ip_data.db'

def init_db():
    with sqlite3.connect(DATABASE) as conn:
        conn.execute('CREATE TABLE IF NOT EXISTS ip_addresses (id INTEGER PRIMARY KEY, ip TEXT, type TEXT)')
    conn.close()

@app.route('/save-ip', methods=['POST'])
def save_ip():
    data = request.json
    ip = data['ip']
    ip_type = data['type']
    with sqlite3.connect(DATABASE) as conn:
        conn.execute('INSERT INTO ip_addresses (ip, type) VALUES (?, ?)', (ip, ip_type))
    conn.commit()
    return jsonify({'status': 'success'})

@app.route('/stats', methods=['GET'])
def get_stats():
    with sqlite3.connect(DATABASE) as conn:
        cursor = conn.execute('SELECT type, COUNT(*) as count FROM ip_addresses GROUP BY type')
        results = cursor.fetchall()
    stats = {row[0]: row[1] for row in results}
    return jsonify(stats)

if __name__ == '__main__':
    init_db()
    app.run(host='0.0.0.0', port=5000)
