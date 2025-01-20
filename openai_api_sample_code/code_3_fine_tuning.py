# fine-tuning
# default
import os
from openai import OpenAI
import pprint

model_4o_mini = "gpt-4o-mini"
model_4o_mini_fine_tuning = "gpt-4o-mini-2024-07-18"
OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY")

client = OpenAI()


def create_fine_tuning_jobs(training_file, model_4o_mini):
    # 指定されたデータセットから新しいモデルを作成するプロセスを開始する微調整ジョブを作成します。
    response = client.fine_tuning.jobs.create(
        training_file=training_file,
        model=model_4o_mini
    )
    return response


def list_fine_tuning_jobs():
    return client.fine_tuning.jobs.list()


def cancel_fine_tuning_jobs(job_id):
    response = client.fine_tuning.jobs.cancel(job_id)
    return response


def create_fine_tuning_job_epochs(training_file, model_4o_mini, n_epochs=2):
    response = client.fine_tuning.jobs.create(
        training_file=training_file,
        model=model_4o_mini,
        hyperparameters={
            "n_epochs": n_epochs
        }
    )
    return response


def create_fine_tuning_jobs_validation(training_file, validation_file, model_4o_mini):
    response = client.fine_tuning.jobs.create(
        training_file=training_file,
        validation_file=validation_file,
        model=model_4o_mini
    )
    return response


def checkpoint_fine_tuning_jobs(job_id):
    import requests

    # APIエンドポイント
    url = f"https://api.openai.com/v1/fine_tuning/jobs/{job_id}/checkpoints"
    # ヘッダー情報
    headers = {
        "Authorization": f"Bearer {OPENAI_API_KEY}"
    }
    # リクエストの送信
    response = requests.get(url, headers=headers)
    return response.json()


def list_events(fine_tuning_job_id, limit=2):
    response = client.fine_tuning.jobs.list_events(
        fine_tuning_job_id=fine_tuning_job_id,
        limit=limit
    )
    return response


def retrieve_fine_tuning_job(job_id):
    response = client.fine_tuning.jobs.retrieve(job_id)
    return response


def main():
    # (pre-1) get id
    # response = client.files.create(
    #     file=open("./finetune_data_prompt_completions.jsonl", "rb"),
    #     purpose="fine-tune"
    # )
    # pprint.pprint(response)

    # (2) cansel
    job_id = 'ftjob-CGMnQGNlHR1GM0EhiuehEbhX'
    response = cancel_fine_tuning_jobs(job_id)
    pprint.pprint(response)


    # (2) list
    # res = list_fine_tuning_jobs()
    # pprint.pprint(res)

    # (3) create jobs
    # training_file_id = 'file-a60nysadW9FoT7iwRf66ILdu'
    # response1 = create_fine_tuning_jobs(training_file_id, model_4o_mini_fine_tuning)
    # pprint.pprint(response1)


if __name__ == "__main__":
    main()

"""
response = {
  "object": "fine_tuning.job",
  "id": "ftjob-abc123",
  "model": "gpt-4o-mini-2024-07-18",
  "created_at": 1721764800,
  "fine_tuned_model": null,
  "organization_id": "org-123",
  "result_files": [],
  "status": "queued",
  "validation_file": null,
  "training_file": "file-abc123",
}
"""
# list
"""
{
  "object": "list",
  "data": [
    {
      "object": "fine_tuning.job.event",
      "id": "ft-event-TjX0lMfOniCZX64t9PUQT5hn",
      "created_at": 1689813489,
      "level": "warn",
      "message": "Fine tuning process stopping due to job cancellation",
      "data": null,
      "type": "message"
    },
    { ... },
    { ... }
  ], "has_more": true
}
"""
# The fine-tuning job checkpoint object
"""
response = {
  "object": "list"
  "data": [
    {
      "object": "fine_tuning.job.checkpoint",
      "id": "ftckpt_zc4Q7MP6XxulcVzj4MZdwsAB",
      "created_at": 1721764867,
      "fine_tuned_model_checkpoint": "ft:gpt-4o-mini-2024-07-18:my-org:custom-suffix:96olL566:ckpt-step-2000",
      "metrics": {
        "full_valid_loss": 0.134,
        "full_valid_mean_token_accuracy": 0.874
      },
      "fine_tuning_job_id": "ftjob-abc123",
      "step_number": 2000,
    },
    {
      "object": "fine_tuning.job.checkpoint",
      "id": "ftckpt_enQCFmOTGj3syEpYVhBRLTSy",
      "created_at": 1721764800,
      "fine_tuned_model_checkpoint": "ft:gpt-4o-mini-2024-07-18:my-org:custom-suffix:7q8mpxmy:ckpt-step-1000",
      "metrics": {
        "full_valid_loss": 0.167,
        "full_valid_mean_token_accuracy": 0.781
      },
      "fine_tuning_job_id": "ftjob-abc123",
      "step_number": 1000,
    },
  ],
  "first_id": "ftckpt_zc4Q7MP6XxulcVzj4MZdwsAB",
  "last_id": "ftckpt_enQCFmOTGj3syEpYVhBRLTSy",
  "has_more": true
}
"""
# event lists
"""
response = {
  "object": "list",
  "data": [
    {
      "object": "fine_tuning.job.event",
      "id": "ft-event-ddTJfwuMVpfLXseO0Am0Gqjm",
      "created_at": 1721764800,
      "level": "info",
      "message": "Fine tuning job successfully completed",
      "data": null,
      "type": "message"
    },
    {
      "object": "fine_tuning.job.event",
      "id": "ft-event-tyiGuB72evQncpH87xe505Sv",
      "created_at": 1721764800,
      "level": "info",
      "message": "New fine-tuned model created: ft:gpt-4o-mini:openai::7p4lURel",
      "data": null,
      "type": "message"
    }
  ],
  "has_more": true
}
"""
# retrieve
"""
response = {
  "object": "fine_tuning.job",
  "id": "ftjob-abc123",
  "model": "davinci-002",
  "created_at": 1692661014,
  "finished_at": 1692661190,
  "fine_tuned_model": "ft:davinci-002:my-org:custom_suffix:7q8mpxmy",
  "organization_id": "org-123",
  "result_files": [
      "file-abc123"
  ],
  "status": "succeeded",
  "validation_file": null,
  "training_file": "file-abc123",
  "hyperparameters": {
      "n_epochs": 4,
      "batch_size": 1,
      "learning_rate_multiplier": 1.0
  },
  "trained_tokens": 5768,
  "integrations": [],
  "seed": 0,
  "estimated_finish": 0
}
"""
#
"""
object = {
  "object": "fine_tuning.job.event",
  "id": "ftevent-abc123"
  "created_at": 1677610602,
  "level": "info",
  "message": "Created fine-tuning job"
}
"""
# training_format_for_chat_models
"""
{
  "messages": [
    { "role": "user", "content": "What is the weather in San Francisco?" },
    {
      "role": "assistant",
      "tool_calls": [
        {
          "id": "call_id",
          "type": "function",
          "function": {
            "name": "get_current_weather",
            "arguments": "{\"location\": \"San Francisco, USA\", \"format\": \"celsius\"}"
          }
        }
      ]
    }
  ],
  "parallel_tool_calls": false,
  "tools": [
    {
      "type": "function",
      "function": {
        "name": "get_current_weather",
        "description": "Get the current weather",
        "parameters": {
          "type": "object",
          "properties": {
            "location": {
                "type": "string",
                "description": "The city and country, eg. San Francisco, USA"
            },
            "format": { "type": "string", "enum": ["celsius", "fahrenheit"] }
          },
          "required": ["location", "format"]
        }
      }
    }
  ]
}
"""
