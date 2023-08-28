from flask import Flask, jsonify
from get_events import get_events
# from opensearchpy import OpenSearch
from elasticsearch import Elasticsearch
from handle_elastic import delete_index, create_index, get_list_of_indexes, get_full_data, get_document_ids_in_index
import json

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
    events = get_events()

    events = {"events": events,}

    # events = {
    #     "summary": "Team Meeting",
    #     "location": "Conference Room 101",
    #     "start": {
    #         "dateTime": "2023-08-28T10:00:00",
    #         "timeZone": "America/New_York"
    #     },
    #     "end": {
    #         "dateTime": "2023-08-28T11:00:00",
    #         "timeZone": "America/New_York"
    #     },
    #     "description": "Discuss project status and upcoming tasks.",
    #     "attendees": [
    #         {
    #             "email": "john@example.com",
    #             "displayName": "John Doe"
    #         },
    #         {
    #             "email": "jane@example.com",
    #             "displayName": "Jane Smith"
    #         }
    #     ]
    # }
    # Insert the JSON data into Elasticsearch
    index_name = "test_index_two"
    document_id = "DnmcO4oBGg9DdxoO92xb"

    print(get_full_data(es, index_name, document_id))

    # create_index(es, index_name, events)
    
    # get_document_ids_in_index(es, index_name)
    
    # return None
    return es.info()

# @app.route("/oauth2callback")
# def oauth2callback():
#     token = oauth.google.authorize_access_token(
#         TOKEN_URL,
#         redirect_uri=REDIRECT_URI
#     )
#     # Now you can use the `token` to make authorized API requests or exchange it for a refresh token.
#     return "Authorization successful!"


if __name__ == '__main__':
    app.run()