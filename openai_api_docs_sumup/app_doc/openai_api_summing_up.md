## Index　Menu

#### API Referrence: https://platform.openai.com/docs/api-reference/introduction

- Introduction
- Authentication
- Making requests
- Streaming
- code_0_organizations_and_projects.py

#### ENDPoints: https://platform.openai.com/docs/api-reference/audio

#### Audio          : https://platform.openai.com/docs/api-reference/audio

-

#### Chat          : https://platform.openai.com/docs/api-reference/chat

- Create chat completion
- The chat completion object
- The chat completion chunk object

#### Embeddings

- Create embeddings

#### The embedding object

- ---

#### Fine-tuning

- Create fine-tuning job
- List fine-tuning jobs
- List fine-tuning events
- List fine-tuning checkpoints
- Retrieve fine-tuning job
- Cancel fine-tuning
- Training format for chat models
- Training format for completions models
- The fine-tuning job object
- The fine-tuning job event object
- The fine-tuning job checkpoint object

#### Batch

- Create batch
- Retrieve batch
- Cancel batch
- List batch
- The batch object
- The request input object
- The request output object

#### Files

- Upload file
- List files
- Retrieve file
- Delete file
- Retrieve file content
- The file object
-

#### Uploads

- Create upload
- Add upload part
- Complete upload
- Cancel upload
- The upload object
- The upload part object

#### Images

- Create image
- Create image edit
- Create image variation
- The image object

#### Models

#### Moderation's

- Create moderation
- The moderation object

#### Assistants
###### code
  - code_10_0_assistants.py
  - code_10_1_assistant_code_interpriter_unstreaming.py
  - code_10_2_assistant_code_interpriter_streaming_unstreaming.py
  - code_10_3_assistant_file_search_unstreaming.py
  - code_10_4_assistant_file_search_streaming.py
  - code_10_5_assistant_function_calling_unstreaming.py
  - code_10_6_assistant_function_calling_streaming.py 
#### Threads
#### Messages
#### Runs
- code_13_runs.py
#### Run Steps
#### Vector Stores
#### Vector Store Files
#### Vector Store File Batches
#### Streaming



#### Runs

#### Runs steps

- code_14_run_steps.py

#### Vector stores

#### Vector store files

#### Vector store file Batches

#### Streaming

├── code_10_11_structured_outputs_pydantic_zod.py
├── code_10_10_structured_outputs.py
├── code_10_12_json_mode.py
├── code_10_13_structured_outputs_spec.md

├── app_1_chat_completions_on_excel.py
├── app_3_function_calling_with_gradio.py
├── app_5_embedding_RAG.md
├── app_6_1_make_fine_tuning_data_from_paragraph_dict_simple.py
├── app_6_3_make_fine_tuning_data_from_python_dict_simple.py
├── b16_assistant.md
├── batch_input.jsonl
├──

├── code_11_thread.py
├── code_11_threads.py
├── code_12_messages.py

├── code_14_run_steps.py
├── code_15_vector_stores.py
├── code_16_vector_store_files.py
├── code_17_vector_store_file_batches.py
├── code_18_streaming.py
├── code_1_0_chat_completions.py
├── code_1_2_text_to_speech.py
├── code_1_3_speech_to_text.py
├── code_1_4_function_calling.py
├── code_1_4_function_calling_tools_spec.md
├── code_2_0_embeddings.py
├── code_2_embedding.py
├── code_3_fine_tuning.py
├── code_4_batch.py
├── code_5_files.py
├── code_7_0_images.py
├── code_7_2_vision.py
├── code_8_models.py
├── code_9_moderations.py

## 01 text generation

```python
from openai import OpenAI
import pprint

client = OpenAI()

response = client.chat.completions.create(
  model="gpt-4o-mini",
  messages=[
    {"role": "system", "content": "You are a helpful assistant."},
    {"role": "user", "content": "What is a LLM?"}
  ]
)
pprint.pprint(response)
```

## 02 vision

```python
import os
import base64
import requests

# OpenAI API Key
api_key = os.getenv('OPENAI_API_KEY')

# Function to encode the image
def encode_image(image_path):
  with open(image_path, "rb") as image_file:
    return base64.b64encode(image_file.read()).decode('utf-8')

# Path to your image
image_path = "path_to_your_image.jpg"
# Getting the base64 string
base64_image = encode_image(image_path)

headers = {
  "Content-Type": "application/json",
  "Authorization": f"Bearer {api_key}"
}

payload = {
  "model": "gpt-4o-mini",
  "messages": [
    {
      "role": "user",
      "content": [
        {
          "type": "text",
          "text": "What’s in this image?"
        },
        {
          "type": "image_url",
          "image_url": {
            "url": f"data:image/jpeg;base64,{base64_image}"
          }
        }
      ]
    }
  ],
  "max_tokens": 300
}

response = requests.post("https://api.openai.com/v1/chat/completions", headers=headers, json=payload)
```

## function call

#### toolsとtool_choiceの仕様

##### tools

- toolsは、モデルに渡す関数のリストを定義します。
- これにより、モデルは入力に応じて適切な関数を呼び出すためのJSONオブジェクトを生成します。
- 各関数は以下の属性を持ちます：
- name: 関数の名前
- description: 関数の説明
- parameters: 関数の引数を定義するオブジェクト。この中には以下の属性が含まれます：
  - type: 引数のタイプ（通常は"object"）
  - properties: 各引数のプロパティを定義するオブジェクト
  - required: 必須の引数のリスト

##### tool_choice

- tool_choiceは、モデルが関数をどのように呼び出すかを制御します。以下の3つのオプションがあります：
- auto（デフォルト）：モデルが自動的に関数を呼び出すかどうか、そしてどの関数を呼び出すかを決定します。
- required: モデルが必ず一つ以上の関数を呼び出すように強制します。
- 特定の関数名: 特定の関数のみを呼び出すようにモデルを強制します。
- none: 関数呼び出しを無効にし、モデルがユーザー向けのメッセージのみを生成するようにします。

```python
def run_conversation():
    messages = [{"role": "user", "content": "「こんにちは」を英語に翻訳して"}]
    tools = [
        {
            "type": "function",  # 今はfunctionのみ
            "function": {
                "name": "translate_to_english",
                "description": "テキストを英語に翻訳します",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "text": {"type": "string", "description": "翻訳するテキスト"},
                    },
                    "required": ["text"],
                },
            },
        }
    ]

    from openai import OpenAI
    client = OpenAI()
    response = client.chat.completions.create(
    model="gpt-4o",
    messages=messages,
    tools=tools,
    tool_choice={"type": "function", "function": {"name": "translate_to_english"}},
    )
```

###### function call - sample 1

```python
from openai import OpenAI
import json

client = OpenAI()

# Example dummy function hard coded to return the same weather
# In production, this could be your backend API or an external API
def get_current_weather(location, unit="fahrenheit"):
    """Get the current weather in a given location"""
    if "tokyo" in location.lower():
        return json.dumps({"location": "Tokyo", "temperature": "10", "unit": unit})
    elif "san francisco" in location.lower():
        return json.dumps({"location": "San Francisco", "temperature": "72", "unit": unit})
    elif "paris" in location.lower():
        return json.dumps({"location": "Paris", "temperature": "22", "unit": unit})
    else:
        return json.dumps({"location": location, "temperature": "unknown"})

def run_conversation():
    # Step 1: send the conversation and available functions to the model
    messages = [{"role": "user", "content": "What's the weather like in San Francisco, Tokyo, and Paris?"}]
    tools = [
        {
            "type": "function",
            "function": {
                "name": "get_current_weather",
                "description": "Get the current weather in a given location",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "location": {
                            "type": "string",
                            "description": "The city and state, e.g. San Francisco, CA",
                        },
                        "unit": {"type": "string", "enum": ["celsius", "fahrenheit"]},
                    },
                    "required": ["location"],
                },
            },
        }
    ]
    response = client.chat.completions.create(
        model="gpt-4o",
        messages=messages,
        tools=tools,
        tool_choice="auto",  # auto is default, but we'll be explicit
    )
    response_message = response.choices[0].message
    tool_calls = response_message.tool_calls
    # Step 2: check if the model wanted to call a function
    if tool_calls:
        # Step 3: call the function
        # Note: the JSON response may not always be valid; be sure to handle errors
        available_functions = {
            "get_current_weather": get_current_weather,
        }  # only one function in this example, but you can have multiple
        messages.append(response_message)  # extend conversation with assistant's reply
        # Step 4: send the info for each function call and function response to the model
        for tool_call in tool_calls:
            function_name = tool_call.function.name
            function_to_call = available_functions[function_name]
            function_args = json.loads(tool_call.function.arguments)
            function_response = function_to_call(
                location=function_args.get("location"),
                unit=function_args.get("unit"),
            )
            messages.append(
                {
                    "tool_call_id": tool_call.id,
                    "role": "tool",
                    "name": function_name,
                    "content": function_response,
                }
            )  # extend conversation with function response
        second_response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=messages,
        )  # get a new response from the model where it can see the function response
        return second_response
print(run_conversation())
```

###### sample2

```python
import openai
import json

# OpenAIのAPIキーを設定
openai.api_key = 'your-api-key-here'

# ダミーの天気情報を返す関数
def get_current_weather(location, unit="fahrenheit"):
    """指定された場所の現在の天気を取得する"""
    if "tokyo" in location.lower():
        return json.dumps({"location": "Tokyo", "temperature": "10", "unit": unit})
    elif "san francisco" in location.lower():
        return json.dumps({"location": "San Francisco", "temperature": "72", "unit": unit})
    elif "paris" in location.lower():
        return json.dumps({"location": "Paris", "temperature": "22", "unit": unit})
    else:
        return json.dumps({"location": location, "temperature": "unknown"})

# 会話を実行する関数
def run_conversation():
    # ステップ1: 会話と利用可能な関数をモデルに送信
    messages = [{"role": "user", "content": "What's the weather like in San Francisco, Tokyo, and Paris?"}]
    tools = [
        {
            "type": "function",
            "function": {
                "name": "get_current_weather",
                "description": "指定された場所の現在の天気を取得します",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "location": {
                            "type": "string",
                            "description": "都市名、例: San Francisco, CA",
                        },
                        "unit": {"type": "string", "enum": ["celsius", "fahrenheit"]},
                    },
                    "required": ["location"],
                },
            },
        }
    ]

    # OpenAIのAPIを使用してモデルに問い合わせ
    response = openai.ChatCompletion.create(
        model="gpt-4-0613",
        messages=messages,
        functions=tools,
        function_call="auto",  # 自動で関数を選択
    )

    response_message = response['choices'][0]['message']
    tool_calls = response_message.get('function_call')

    # ステップ2: モデルが関数を呼び出そうとしたか確認
    if tool_calls:
        # ステップ3: 関数を呼び出し
        available_functions = {
            "get_current_weather": get_current_weather,
        }
        function_name = tool_calls['name']
        function_to_call = available_functions[function_name]
        function_args = json.loads(tool_calls['arguments'])
        function_response = function_to_call(
            location=function_args.get("location"),
            unit=function_args.get("unit"),
        )

        # ステップ4: 関数の呼び出し情報と関数の応答をモデルに送信
        messages.append(response_message)  # 会話をアシスタントの応答で拡張
        messages.append(
            {
                "role": "function",
                "name": function_name,
                "content": function_response,
            }
        )

        second_response = openai.ChatCompletion.create(
            model="gpt-4-0613",
            messages=messages,
        )
        return second_response['choices'][0]['message']['content']

print(run_conversation())

```

## json mode
