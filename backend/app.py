from flask import Flask, jsonify
from get_events import get_events
import sqlite3

app = Flask(__name__)

events = get_events()

conn = sqlite3.connect('db/data.db')
conn.close()

@app.route('/api', methods=['GET'])
def hello_world():
    data = events
    return jsonify(events)

if __name__ == '__main__':
    app.run()