from flask import Flask, jsonify
from get_events import get_events
from opensearchpy import OpenSearch

app = Flask(__name__)

events = get_events()

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

opensearch = OpenSearch(hosts=['http://localhost:9200/'])

@app.route('/api', methods=['GET'])
def hello_world():
    # Put all events into opensearchpy cluster. But only include the fields listed in needed variables. Sort by "id" field.
    index_name = 'events'
    index_exists = opensearch.indices.exists(index=index_name)
    if index_exists:
        print(f"Index '{index_name}' already exists.")
    else:
        opensearch.indices.create(index=index_name)
        print(f"Index '{index_name}' created successfully.")
    for event in events:
        event_document = {
            "summary": event["summary"],
            "updated": event["updated"],
            "description": event["description"],
            "start": event["start"]["dateTime"],
            "end": event["end"]["dateTime"],
            "location": event["location"],
            "created": event["created"],
            "htmlLink": event["htmlLink"],
            "id": event["id"]
        }
        opensearch.index(index='events', body=event_document)
        # search_results = opensearch.search(index='events', body={"sort": "id"})
        # print(search_results)
    return jsonify(events)

if __name__ == '__main__':
    app.run()