#
from openai import OpenAI

client = OpenAI()


def create_vector_stores(name):
    # Create a vector store.
    vector_store = client.beta.vector_stores.create(
        name=name  # Support FAQ
    )
    return vector_store  # A vector store object.


def list_vector_stores(name):
    # Returns a list of vector stores.
    vector_stores = client.beta.vector_stores.list()
    return vector_stores  # A list of vector store objects.


def retrieve_vector_stores(vector_store_id):
    # Retrieves a vector store.
    vector_store = client.beta.vector_stores.retrieve(
        vector_store_id=vector_store_id
    )
    return vector_store  # The vector store object matching the specified ID.


def update_vector_stores(vector_store_id, name):
    # Modifies a vector store.
    vector_store = client.beta.vector_stores.update(
        vector_store_id=vector_store_id,
        name=name
    )
    return vector_store  # The modified vector store object.


def delete_vector_stores(vector_store_id):
    # Delete a vector store.
    deleted_vector_store = client.beta.vector_stores.delete(
        vector_store_id=vector_store_id
    )
    return deleted_vector_store




# response
"""
response = {
  "id": "vs_abc123",
  "object": "vector_store",
  "created_at": 1699061776,
  "name": "Support FAQ",
  "bytes": 139920,
  "file_counts": {
    "in_progress": 0,
    "completed": 3,
    "failed": 0,
    "cancelled": 0,
    "total": 3
  }
}
"""

# list object
"""
{
  "object": "list",
  "data": [
    {
      "id": "vs_abc123",
      "object": "vector_store",
      "created_at": 1699061776,
      "name": "Support FAQ",
      "bytes": 139920,
      "file_counts": {
        "in_progress": 0,
        "completed": 3,
        "failed": 0,
        "cancelled": 0,
        "total": 3
      }
    },
    {
      "id": "vs_abc456",
      "object": "vector_store",
      "created_at": 1699061776,
      "name": "Support FAQ v2",
      "bytes": 139920,
      "file_counts": {
        "in_progress": 0,
        "completed": 3,
        "failed": 0,
        "cancelled": 0,
        "total": 3
      }
    }
  ],
  "first_id": "vs_abc123",
  "last_id": "vs_abc456",
  "has_more": false
}
"""
