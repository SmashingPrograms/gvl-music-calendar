from flask import Flask, jsonify
from get_events import get_events
import sqlite3

app = Flask(__name__)

events = get_events()

conn = sqlite3.connect('db/data.db')
c = conn.cursor()
c.execute('''CREATE TABLE events
                (summary text, updated text, description text, start text, end text, location text, created text, htmlLink text, id text)''')
conn.commit()
conn.close()

# needed variables
# - summary (title)
# - updated
# - description
# - start["dateTime"]
# - end["dateTime"]
# - location
# - created
# - htmlLink
# - id


@app.route('/api', methods=['GET'])
def hello_world():
    # put all events into database. Use id as primary key. If id already exists, update the event. Name each column the name in needed variables, and look for the name in the json object.
    for event in events:
        conn = sqlite3.connect('db/data.db')
        c = conn.cursor()
        c.execute("INSERT INTO events VALUES ('{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}')".format(event['summary'], event['updated'], event['description'], event['start']['dateTime'], event['end']['dateTime'], event['location'], event['created'], event['htmlLink'], event['id']))
        conn.commit()
        conn.close()
    conn2 = sqlite3.connect('db/data.db')
    c2 = conn2.cursor()
    c2.execute("SELECT * FROM events")
    data = c2.fetchall()
    # conn2.close()
    return jsonify(data)

if __name__ == '__main__':
    app.run()