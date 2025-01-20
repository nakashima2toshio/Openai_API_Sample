# chat completion
import gradio as gr
from openai import OpenAI
import json
import pprint

client = OpenAI()
model_chat_completion = "gpt-4o"
model_4o_mini = "gpt-4o-mini"
model_list = [model_chat_completion, model_4o_mini]

model_speech = "whisper-1"


# --------------------------------------------------------------
def create_chat_completions(system_content, user_content):
    # (1) chat completion default
    completion = client.chat.completions.create(
        model=model_chat_completion,
        messages=[
            {"role": "system", "content": system_content},
            {"role": "user", "content": user_content}
        ]
    )
    return completion.choices[0].message


# --------------------------------------------------------------
def create_chat_completions_image_input(q_text, image_url_string):
    # (2) chat_completion_image_input
    image_url_string = image_url_string
    response = client.chat.completions.create(
        model=model_chat_completion,
        messages=[
            {
                "role": "system",
                "content": "あなたは画像の内容について答えるAIです。"
            },
            {
                "role": "user",
                "content": f"{q_text}\nこちらの画像について教えてください: {image_url_string}"
            }
        ],
        max_tokens=300,
    )

    return response.choices[0]


# --------------------------------------------------------------
def create_chat_completions_streaming(system_content, user_content):
    # (3) create.chat.completion streaming
    stream = client.chat.completions.create(
        model=model_chat_completion,
        messages=[
            {"role": "system", "content": system_content},
            {"role": "user", "content": user_content}
        ],
        stream=True
    )
    for chunk in stream:
        if chunk.choices[0].delta.content is not None:
            print(chunk.choices[0].delta.content, end="")
    return stream


# --------------------------------------------------------------
def create_chat_completions_logprobs(role_user_content, top_logprobs=2):
    # (4) chat completions logprobs
    completion = client.chat.completions.create(
        model=model_chat_completion,
        messages=[
            {"role": "user", "content": role_user_content}
        ],
        logprobs=True,
        top_logprobs=top_logprobs
    )

    return completion.choices[0].message, completion.choices[0].logprobs


# --------------------------------------------------------------
def get_current_weather(location, unit="fahrenheit"):
    # 指定された場所の現在の天気を取得する
    if "tokyo" in location.lower():
        return json.dumps({"location": "Tokyo", "temperature": "10", "unit": unit})
    elif "san francisco" in location.lower():
        return json.dumps({"location": "San Francisco", "temperature": "72", "unit": unit})
    elif "paris" in location.lower():
        return json.dumps({"location": "Paris", "temperature": "22", "unit": unit})
    else:
        return json.dumps({"location": location, "temperature": "unknown"})
# --------------------------------------------------------------
tools = [
    {
        "type": "function",                 # 関数呼び出しを定義
        "function": {
            "name": "get_current_weather",
            "description": "Get the current weather in a given location",
            "parameters": {
                "type": "object",           # 必ず、"object"
                "properties": {             # 関数の引数：プロパティー
                    "location": {           # ロケーション
                        "type": "string",   #　型と説明
                        "description": "The city and state, e.g. San Francisco, CA",
                    },
                    "unit": {"type": "string", "enum": ["celsius", "fahrenheit"]},
                },
                "required": ["location"],   # 必須な引数。
            },
        }
    }
]


# function_messages = [{"role": "user", "content": "What's the weather like in Boston today?"}]


def create_chat_completions_functions_with_tools(chat_messages):
    # (5) function-tools
    completion = client.chat.completions.create(
        model=model_chat_completion,
        messages=chat_messages,
        tools=tools,
        tool_choice="auto"
    )
    return completion


# --------------------------------------------------------------
def create_audio_transcription(speech_mp3):
    # (6) audio.transcriptions
    audio_file = open(speech_mp3, "rb")
    transcript = client.audio.transcriptions.create(
        model=model_speech,
        file=audio_file
    )
    return transcript


# --------------------------------------------------------------
# GradioのChatインターフェイスを定義
def chatbot(input_text):
    # OpenAI APIを呼び出し、回答を取得
    response = client.completions.create(
        model=model_chat_completion,
        prompt=input_text,
        max_tokens=2048,
        temperature=0.7,
    )
    # 回答を返す
    return response.choices[0].text


# --------------------------------------------------------------
def main():
    system_content = "あなたは有能なソフトウェア開発者のアシスタントです。"
    user_content = "プロのソフトウェア開発者向けに、OpenAiのAPIの概要を説明しなさい。"
    user_content2 = 'python gradioの概要を教えて。'
    q_text = "この絵は、どんな絵か説明しなさい。"
    image_url_string = "https://article-image.travel.navitime.jp/img/NTJmat0459/n_mat0437_1.jpg"

    # (1) def create_chat_completions(system_content, user_content)
    chat_messages = create_chat_completions(system_content, user_content)
    print(chat_messages.content)

    # (2) create_chat_completions_image_input(q_text, image_url_string)
    res = create_chat_completions_image_input(q_text, image_url_string)
    print(res)
    # content部分を取得して表示
    content = res.message.content.replace("。", "。\n")
    print(content)

    # (3) create_chat_completions_streaming(system_content, user_content)
    res = create_chat_completions_streaming(system_content, user_content2)
    print(res)

    # (4) chat completions log
    role_user_content = "Hello world!"
    msg, logprobs = create_chat_completions_logprobs(role_user_content, top_logprobs=2)
    pprint.pprint(msg)
    pprint.pprint(logprobs)

    # (5) function-tool
    function_messages = [{"role": "user", "content": "What's the weather like in Boston today?"}]
    response = create_chat_completions_functions_with_tools(function_messages)
    pprint.pprint(response)

    # (6) create_audio_transcription(speech_mp3)
    speech_mp3 = './output.mp3'
    response = create_audio_transcription(speech_mp3)
    print(response)

    # (7) GradioのChat
    demo = gr.Interface(
        fn=chatbot,
        inputs="text",
        outputs="text",
        title="Chatbot",
        description="OpenAI APIを使用した簡単なチャットボット",
    )
    demo.launch()


if __name__ == "__main__":
    main()

# --------------------------------------------------------------
# response object and etc.
# --------------------------------------------------------------
# The chat completion chunk object
"""
obj => JSONL-format
{"id":"chatcmpl-123","object":"chat.completion.chunk","created":1694268190,"model":"gpt-4o-mini", "system_fingerprint": "fp_44709d6fcb", "choices":[{"index":0,"delta":{"role":"assistant","content":""},"logprobs":null,"finish_reason":null}]}
{"id":"chatcmpl-123","object":"chat.completion.chunk","created":1694268190,"model":"gpt-4o-mini", "system_fingerprint": "fp_44709d6fcb", "choices":[{"index":0,"delta":{"content":"Hello"},"logprobs":null,"finish_reason":null}]}
{"id":"chatcmpl-123","object":"chat.completion.chunk","created":1694268190,"model":"gpt-4o-mini", "system_fingerprint": "fp_44709d6fcb", "choices":[{"index":0,"delta":{},"logprobs":null,"finish_reason":"stop"}]}
"""
# The chat completion object
"""
object = {
  "id": "chatcmpl-123",
  "object": "chat.completion",
  "created": 1677652288,
  "model": "gpt-4o-mini",
  "system_fingerprint": "fp_44709d6fcb",
  "choices": [{
    "index": 0,
    "message": {
      "role": "assistant",
      "content": "\n\nHello there, how may I assist you today?",
    },
    "logprobs": null,
    "finish_reason": "stop"
  }],
  "usage": {
    "prompt_tokens": 9,
    "completion_tokens": 12,
    "total_tokens": 21
  }
}
"""
# logprobs
"""
response = {
  "id": "chatcmpl-123",
  "object": "chat.completion",
  "created": 1702685778,
  "model": "gpt-4o-mini",
  "choices": [
    {
      "index": 0,
      "message": {
        "role": "assistant",
        "content": "Hello! How can I assist you today?"
      },
      "logprobs": {
        "content": [
          {
            "token": "Hello",
            "logprob": -0.31725305,
            "bytes": [72, 101, 108, 108, 111],
            "top_logprobs": [
              {
                "token": "Hello",
                "logprob": -0.31725305,
                "bytes": [72, 101, 108, 108, 111]
              },
              {
                "token": "Hi",
                "logprob": -1.3190403,
                "bytes": [72, 105]
              }
            ]
          },
          {
            "token": "!",
            "logprob": -0.02380986,
            "bytes": [
              33
            ],
            "top_logprobs": [
              {
                "token": "!",
                "logprob": -0.02380986,
                "bytes": [33]
              },
              {
                "token": " there",
                "logprob": -3.787621,
                "bytes": [32, 116, 104, 101, 114, 101]
              }
            ]
          },
          {
            "token": " How",
            "logprob": -0.000054669687,
            "bytes": [32, 72, 111, 119],
            "top_logprobs": [
              {
                "token": " How",
                "logprob": -0.000054669687,
                "bytes": [32, 72, 111, 119]
              },
              {
                "token": "<|end|>",
                "logprob": -10.953937,
                "bytes": null
              }
            ]
          },
          {
            "token": " can",
            "logprob": -0.015801601,
            "bytes": [32, 99, 97, 110],
            "top_logprobs": [
              {
                "token": " can",
                "logprob": -0.015801601,
                "bytes": [32, 99, 97, 110]
              },
              {
                "token": " may",
                "logprob": -4.161023,
                "bytes": [32, 109, 97, 121]
              }
            ]
          },
          {
            "token": " I",
            "logprob": -3.7697225e-6,
            "bytes": [
              32,
              73
            ],
            "top_logprobs": [
              {
                "token": " I",
                "logprob": -3.7697225e-6,
                "bytes": [32, 73]
              },
              {
                "token": " assist",
                "logprob": -13.596657,
                "bytes": [32, 97, 115, 115, 105, 115, 116]
              }
            ]
          },
          {
            "token": " assist",
            "logprob": -0.04571125,
            "bytes": [32, 97, 115, 115, 105, 115, 116],
            "top_logprobs": [
              {
                "token": " assist",
                "logprob": -0.04571125,
                "bytes": [32, 97, 115, 115, 105, 115, 116]
              },
              {
                "token": " help",
                "logprob": -3.1089056,
                "bytes": [32, 104, 101, 108, 112]
              }
            ]
          },
          {
            "token": " you",
            "logprob": -5.4385737e-6,
            "bytes": [32, 121, 111, 117],
            "top_logprobs": [
              {
                "token": " you",
                "logprob": -5.4385737e-6,
                "bytes": [32, 121, 111, 117]
              },
              {
                "token": " today",
                "logprob": -12.807695,
                "bytes": [32, 116, 111, 100, 97, 121]
              }
            ]
          },
          {
            "token": " today",
            "logprob": -0.0040071653,
            "bytes": [32, 116, 111, 100, 97, 121],
            "top_logprobs": [
              {
                "token": " today",
                "logprob": -0.0040071653,
                "bytes": [32, 116, 111, 100, 97, 121]
              },
              {
                "token": "?",
                "logprob": -5.5247097,
                "bytes": [63]
              }
            ]
          },
          {
            "token": "?",
            "logprob": -0.0008108172,
            "bytes": [63],
            "top_logprobs": [
              {
                "token": "?",
                "logprob": -0.0008108172,
                "bytes": [63]
              },
              {
                "token": "?\n",
                "logprob": -7.184561,
                "bytes": [63, 10]
              }
            ]
          }
        ]
      },
      "finish_reason": "stop"
    }
  ],
  "usage": {
    "prompt_tokens": 9,
    "completion_tokens": 9,
    "total_tokens": 18
  },
  "system_fingerprint": null
}
"""
