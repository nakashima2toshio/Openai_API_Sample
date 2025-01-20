# create_batch_jobs
import pprint
from openai import OpenAI

client = OpenAI()


def create_batches():
    response = client.batches.create(
        input_file_id="file-abc123",
        endpoint="/v1/chat/completions",
        completion_window="24h"
    )
    return response


def list_batches():
    response = client.batches.list()
    return response


def retrieve_batch(batch_id):
    response = client.batches.retrieve(batch_id)
    return response


def cancel_batch(batch_id):
    response = client.batches.cancel(batch_id)
    return response


def main():
    # (1) get id
    response = client.files.create(
        file=open("./batch_input.jsonl", "rb"),
        purpose="fine-tune"
    )
    pprint.pprint(response)
"""
FileObject(id='file-gNLv87GrKE4itZpevsoZmXhF', 
bytes=2201, created_at=1723982961, filename='batch_input.jsonl', 
object='file', purpose='fine-tune', status='processed', status_details=None)
"""

if __name__ == "__main__":
    main()

# request input object
pass
"""
{"custom_id": "request-1", "method": "POST", "url": "/v1/chat/completions", "body": {"model": "gpt-4o-mini", "messages": [{"role": "system", "content": "You are a helpful assistant."}, {"role": "user", "content": "What is 2+2?"}]}}
"""
pass
# request output object
"""
{"id": "batch_req_wnaDys", "custom_id": "request-2", "response": {"status_code": 200, "request_id": "req_c187b3", "body": {"id": "chatcmpl-9758Iw", "object": "chat.completion", "created": 1711475054, "model": "gpt-4o-mini", "choices": [{"index": 0, "message": {"role": "assistant", "content": "2 + 2 equals 4."}, "finish_reason": "stop"}], "usage": {"prompt_tokens": 24, "completion_tokens": 15, "total_tokens": 39}, "system_fingerprint": null}}, "error": null}
"""
# response
pass
"""
response = {
  "id": "batch_abc123",
  "object": "batch",
  "endpoint": "/v1/completions",
  "errors": null,
  "input_file_id": "file-abc123",
  "completion_window": "24h",
  "status": "completed",
  "output_file_id": "file-cvaTdG",
  "error_file_id": "file-HOWS94",
  "created_at": 1711471533,
  "in_progress_at": 1711471538,
  "expires_at": 1711557933,
  "finalizing_at": 1711493133,
  "completed_at": 1711493163,
  "failed_at": null,
  "expired_at": null,
  "cancelling_at": null,
  "cancelled_at": null,
  "request_counts": {
    "total": 100,
    "completed": 95,
    "failed": 5
  },
  "metadata": {
    "customer_id": "user_123456789",
    "batch_description": "Nightly eval job",
  }
}
"""
