# Index name to delete
from elasticsearch import Elasticsearch

def delete_index(es, index_name):
    print(f"Deleting index {index_name}...")

    # Delete the index
    response = es.indices.delete(index=index_name)

    # Check if the deletion was successful
    if response.get("acknowledged"):
        print(f"Index '{index_name}' deleted successfully.")
    else:
        print(f"Failed to delete index '{index_name}'.")

def create_index(es, index_name, data):
    doc_type = "_doc"
    response = es.index(index=index_name, doc_type=doc_type, body=data)

    # Check if the insertion was successful
    if response["result"] == "created":
        print("Data inserted successfully.")
    else:
        print("Failed to insert data.")

def get_list_of_indexes(es):
    index_list = es.indices.get_alias("*").keys()

    return index_list