# vector_store_file_batches
from openai import OpenAI

client = OpenAI()


def create_file_batches_vector_store(vector_store_id, file_ids):
    # Create a vector store file batch.
    vector_store_file_batch = client.beta.vector_stores.file_batches.create(
        vector_store_id=vector_store_id,
        file_ids=file_ids  # ["file-abc123", "file-abc456"]
    )
    return vector_store_file_batch


def retrieve_file_batches_vector_store(vector_store_id, file_ids):
    # Retrieves a vector store file batch.
    vector_store_file_batch = client.beta.vector_stores.file_batches.retrieve(
        vector_store_id=vector_store_id,
        batch_id=file_ids
    )
    return vector_store_file_batch


def cancel_file_batches_vector_store(vector_store_id, file_batch_id):
    # ファイル バッチが属するベクター ストアの ID。
    deleted_vector_store_file_batch = client.beta.vector_stores.file_batches.cancel(
        vector_store_id="vs_abc123",
        file_batch_id="vsfb_abc123"
    )
    return deleted_vector_store_file_batch


def list_vector_store_file_batches(vector_store_id):
    # ベクトル ストア ファイルのリストをバッチで返します。
    vector_store_files = client.beta.vector_stores.file_batches.list_files(
        vector_store_id=vector_store_id,
        batch_id="vsfb_abc123"
    )
    return vector_store_files


"""
response = {
  "id": "vsfb_abc123",
  "object": "vector_store.file_batch",
  "created_at": 1699061776,
  "vector_store_id": "vs_abc123",
  "status": "in_progress",
  "file_counts": {
    "in_progress": 1,
    "completed": 1,
    "failed": 0,
    "cancelled": 0,
    "total": 0,
  }
}
"""

# The vector store files batch object
"""
object = {
  "id": "vsfb_123",
  "object": "vector_store.files_batch",
  "created_at": 1698107661,
  "vector_store_id": "vs_abc123",
  "status": "completed",
  "file_counts": {
    "in_progress": 0,
    "completed": 100,
    "failed": 0,
    "cancelled": 0,
    "total": 100
  }
}
"""
