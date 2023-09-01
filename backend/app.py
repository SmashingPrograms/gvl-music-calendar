from flask import Flask, jsonify
from get_events import get_calendar_events
from elasticsearch import Elasticsearch
from handle_elastic import delete_index, create_index, get_list_of_indexes, get_full_data, get_document_ids_in_index
import json
import time
import threading

app = Flask(__name__)

def read_textfile(path):
    return open(path, 'r').read()

private_folder = "../private"
username_path = f"{private_folder}/username.txt"
password_path = f"{private_folder}/password.txt"

username=read_textfile(username_path)
password=read_textfile(password_path)


index_name = "test_index_two"
document_id = "DnmcO4oBGg9DdxoO92xb"

es = Elasticsearch("https://localhost:9200", http_auth=(username, password), verify_certs=False)



update_lock = threading.Lock()

print("Before update function")
def update_elasticsearch_data():
    print("During update function outside while loop")
    while True:
        with update_lock:
            # Fetch data from Google Calendar (replace with your implementation)
            events = get_calendar_events()

            # Update the specific document in Elasticsearch with the fetched data
            es.index(index=index_name, id=document_id, document=events)
            print("Around again...")

            # Sleep for 10 seconds before the next update
            time.sleep(10)

# Create a thread for the update task

update_thread = threading.Thread(target=update_elasticsearch_data)

update_thread.start()



# Start the update thread when the Flask app is started
# @app.before_first_request
# def before_first_request()
@app.route('/api', methods=['GET'])
def hello_world():
    es = Elasticsearch("https://localhost:9200", http_auth=(username, password), verify_certs=False)
    print("Get the current ElasticSearch data:")
    # events = get_events()
    event_data = get_full_data(es, index_name, document_id)
    
    return event_data


if __name__ == '__main__':
    print("I GOT BACK TO MAIN")
    app.run()