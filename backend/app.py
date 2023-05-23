from flask import Flask, jsonify
from get_events import get_events
# from opensearchpy import OpenSearch
from elasticsearch import Elasticsearch

app = Flask(__name__)

def read_textfile(path):
    return open(path, 'r').read()

private_folder = "../private"
username_path = f"{private_folder}/username.txt"
password_path = f"{private_folder}/password.txt"

username=read_textfile(username_path)
password=read_textfile(password_path)

print("I got here.")

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
# Put all events into opensearchpy cluster. But only include the fields listed in needed variables. Sort by "id" field.

@app.route('/api', methods=['GET'])
def hello_world():
    es = Elasticsearch("https://localhost:9200", http_auth=(username, password), verify_certs=False)
    print("Am I getting this far?")
    # events = get_events()

    
    return es.info().body

if __name__ == '__main__':
    app.run()