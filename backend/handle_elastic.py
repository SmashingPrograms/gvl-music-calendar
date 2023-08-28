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

def get_full_data(es, index_name, document_id):

    # Retrieve the document from the index
    response = es.get(index=index_name, id=document_id)

    # Extract the source data from the response
    source_data = response['_source']

    return source_data

def get_document_ids_in_index(es, index_name):
    # Search query (match all documents)
    search_query = {
        "query": {
            "match_all": {}
        }
    }

    # Perform the search
    search_results = es.search(index=index_name, body=search_query)

    # Extract document IDs from search results
    document_ids = [hit["_id"] for hit in search_results["hits"]["hits"]]

    # Print the list of document IDs
    print("Document IDs in index '{}'".format(index_name))
    for doc_id in document_ids:
        print(doc_id)