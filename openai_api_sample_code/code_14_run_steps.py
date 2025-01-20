# run steps
from openai import OpenAI
client = OpenAI()

# --------------
# 実行手順
# --------------
def thread_run_steps(thread_id, run_id):
    # 実行に属する実行ステップのリストを返します。
    run_steps = client.beta.threads.runs.steps.list(
        thread_id=thread_id,
        run_id=run_id
    )

    return run_steps


def retrieve_run_steps(thread_id, run_id, step_id):
    # Retrieves a run step.
    run_step = client.beta.threads.runs.steps.retrieve(
        thread_id=thread_id,
        run_id=run_id,
        step_id=step_id
    )

    return run_step





"""
response = {
  "object": "list",
  "data": [
    {
      "id": "step_abc123",
      "object": "thread.run.step",
      "created_at": 1699063291,
      "run_id": "run_abc123",
      "assistant_id": "asst_abc123",
      "thread_id": "thread_abc123",
      "type": "message_creation",
      "status": "completed",
      "cancelled_at": null,
      "completed_at": 1699063291,
      "expired_at": null,
      "failed_at": null,
      "last_error": null,
      "step_details": {
        "type": "message_creation",
        "message_creation": {
          "message_id": "msg_abc123"
        }
      },
      "usage": {
        "prompt_tokens": 123,
        "completion_tokens": 456,
        "total_tokens": 579
      }
    }
  ],
  "first_id": "step_abc123",
  "last_id": "step_abc456",
  "has_more": false
}
"""