# messages
from openai import OpenAI

client = OpenAI()


def create_message(thread_id):
    thread_message = client.beta.threads.messages.create(
        thread_id=thread_id,  # ex. "thread_abc123"
        role="user",
        content="How does AI work? Explain it in simple terms.",
    )
    return thread_message


def list_messages(thread_id):
    thread_messages = client.beta.threads.messages.list(thread_id)
    return thread_messages.data


def retrieve_message(message_id, thread_id):
    message = client.beta.threads.messages.retrieve(
        message_id=message_id,
        thread_id=thread_id,
    )
    return message


def update_message(message_id, thread_id, metadata):
    message = client.beta.threads.messages.update(
        message_id=message_id,
        thread_id=thread_id,
        metadata=metadata,
        # metadata={
        #     "modified": "true",
        #     "user": "abc123",
        # },
    )
    return message


def delete_message(message_id, thread_id):
    deleted_message = client.beta.threads.messages.delete(
        message_id=message_id,
        thread_id=thread_id,
    )
    return deleted_message


"""
response =  {
  "id": "msg_abc123",
  "object": "thread.message",
  "created_at": 1713226573,
  "assistant_id": null,
  "thread_id": "thread_abc123",
  "run_id": null,
  "role": "user",
  "content": [
    {
      "type": "text",
      "text": {
        "value": "How does AI work? Explain it in simple terms.",
        "annotations": []
      }
    }
  ],
  "attachments": [],
  "metadata": {}
}
"""
