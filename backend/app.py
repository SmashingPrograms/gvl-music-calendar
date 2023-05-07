from flask import Flask, jsonify
import sqlite3

app = Flask(__name__)

conn = sqlite3.connect('db/data.db')
conn.close()

@app.route('/api', methods=['GET'])
def hello_world():
    data = {'message': 'Hello, World!'}
    return jsonify(data)

if __name__ == '__main__':
    app.run()