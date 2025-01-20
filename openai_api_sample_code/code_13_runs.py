from openai import OpenAI
from pathlib import Path

client = OpenAI()

# --------------
# 実行：　スレッド上で実行される実行を表します。
# -------------

# --------------------------------------------------------------
def create_threads_runs(thread_id, assistant_id):
    # runs Default
    run = client.beta.threads.runs.create(
        thread_id=thread_id,       # 実行するスレッドの ID。
        assistant_id=assistant_id  # この実行を実行するために使用するアシスタントの ID 。
    )
    return run

# runs Streaming

# runs Streaming with Functions

# --------------------------------------------------------------
# response object
# --------------------------------------------------------------
""" response
{
  "id": "run_abc123",
  "object": "thread.run",
  "created_at": 1699063290,
  "assistant_id": "asst_abc123",
  "thread_id": "thread_abc123",
  "status": "queued",
  "started_at": 1699063290,
  "expires_at": null,
  "cancelled_at": null,
  "failed_at": null,
  "completed_at": 1699063291,
  "last_error": null,
  "model": "gpt-4o",
  "instructions": null,
  "incomplete_details": null,
  "tools": [
    {
      "type": "code_interpreter"
    }
  ],
  "metadata": {},
  "usage": null,
  "temperature": 1.0,
  "top_p": 1.0,
  "max_prompt_tokens": 1000,
  "max_completion_tokens": 1000,
  "truncation_strategy": {
    "type": "auto",
    "last_messages": null
  },
  "response_format": "auto",
  "tool_choice": "auto",
  "parallel_tool_calls": true
}

"""
