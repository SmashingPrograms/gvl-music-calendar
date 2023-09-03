from flask import Flask, jsonify
from flask_cors import CORS
from get_events import get_calendar_events
from elasticsearch import Elasticsearch
from handle_elastic import delete_index, create_index, get_list_of_indexes, get_full_data, get_document_ids_in_index
import json
import time
import threading

def get_attachment_ids(attachments):
    if attachments:
        attachment_ids = []
        for attachment in attachments:
            attachment_ids.append(attachment["fileId"])
        return attachment_ids
    return None

def get_value_from_dictionary(dictionary, key, key2=None):
    if key2:
        if key in dictionary:
            if key2 in dictionary[key]:
                return dictionary[key][key2]
    else:
        if key in dictionary:
            return dictionary[key]
    return None

app = Flask(__name__)
CORS(app)

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
def api():
    es = Elasticsearch("https://localhost:9200", http_auth=(username, password), verify_certs=False)
    print("Get the current ElasticSearch data:")
    # events = get_events()
    event_data = get_full_data(es, index_name, document_id)["events"]
    print(event_data[0])
    filtered_event_data = []
    for event in event_data:
        title = get_value_from_dictionary(event, "summary")
        description = get_value_from_dictionary(event, "description")
        location = get_value_from_dictionary(event, "location")
        start = get_value_from_dictionary(event, "start", "dateTime")
        end = get_value_from_dictionary(event, "end", "dateTime")
        status = get_value_from_dictionary(event, "status") # confirmed, cancelled, etc.
        attachments = get_value_from_dictionary(event, "attachments")
        attachment_ids = get_attachment_ids(attachments)

        # THIS WILL NEED TO BE TRACKED, to see if it has changed
        # sequence = event["sequence"]

        filtered_event = {
            "title": title,
            "description": description,
            "location": location,
            "start": start,
            "end": end,
            "status": status,
            "attachments": attachment_ids,
        }

        filtered_event_data.append(filtered_event)
        # filtered_event_data.append({
        #     "summary": event["summary"],
        #     "start": event["start"],
        #     "end": event["end"]
        # })

    
    return filtered_event_data


if __name__ == '__main__':
    print("I GOT BACK TO MAIN")
    app.run()