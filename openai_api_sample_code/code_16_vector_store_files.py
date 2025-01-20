# vector store files
from openai import OpenAI

client = OpenAI()


def create_vector_store_files(vector_store_id, file_id):
    # Create a vector store file by attaching a File to a vector store.
    vector_store_file = client.beta.vector_stores.files.create(
        vector_store_id=vector_store_id,
        file_id=file_id
    )
    return vector_store_file  # A vector store file object.


def list_vector_store_files(vector_store_id):
    # Returns a list of vector store files.
    vector_store_files = client.beta.vector_stores.files.list(
        vector_store_id=vector_store_id
    )
    return vector_store_files  # A list of vector store file objects.


def retrieve_vector_store_file(vector_store_id, file_id):
    # Retrieves a vector store file.
    vector_store_file = client.beta.vector_stores.files.retrieve(
        vector_store_id=vector_store_id,
        file_id=file_id
    )
    return vector_store_file  # A vector store file object.


def delete_vector_store_file(vector_store_id, file_id):
    # Delete a vector store file.
    # This will remove the file from the vector store but the file itself will not be deleted.
    # To delete the file, use the delete file endpoint.
    deleted_vector_store_file = client.beta.vector_stores.files.delete(
        vector_store_id=vector_store_id,
        file_id=file_id
    )
    return deleted_vector_store_file



"""
response = {
  "id": "file-abc123",
  "object": "vector_store.file",
  "created_at": 1699061776,
  "usage_bytes": 1234,
  "vector_store_id": "vs_abcd",
  "status": "completed",
  "last_error": null
}
"""

# list
"""
{
  "object": "list",
  "data": [
    {
      "id": "file-abc123",
      "object": "vector_store.file",
      "created_at": 1699061776,
      "vector_store_id": "vs_abc123"
    },
    {
      "id": "file-abc456",
      "object": "vector_store.file",
      "created_at": 1699061776,
      "vector_store_id": "vs_abc123"
    }
  ],
  "first_id": "file-abc123",
  "last_id": "file-abc456",
  "has_more": false
}
"""

# vector file object
"""
{
  "id": "file-abc123",
  "object": "vector_store.file",
  "usage_bytes": 1234,
  "created_at": 1698107661,
  "vector_store_id": "vs_abc123",
  "status": "completed",
  "last_error": null,
  "chunking_strategy": {
    "type": "static",
    "static": {
      "max_chunk_size_tokens": 800,
      "chunk_overlap_tokens": 400
    }
  }
}
"""