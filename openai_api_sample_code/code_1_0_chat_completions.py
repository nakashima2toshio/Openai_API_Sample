# chat completion
import gradio as gr
from openai import OpenAI
import json
import pprint

client = OpenAI()
model_chat_completion = "gpt-4o"
model_4o_mini = "gpt-4o-mini"
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
system_content = "あなたは有能なソフトウェア開発者のアシスタントです。"
user_content = "プロのソフトウェア開発者向けに、OpenAiのAPIの概要を説明しなさい。"
user_content2 = 'python gradioの概要を教えて。'
q_text = "この絵は、どんな絵か説明しなさい。"
image_url_string = "https://article-image.travel.navitime.jp/img/NTJmat0459/n_mat0437_1.jpg"

def main_1():

    # (1) def create_chat_completions(system_content, user_content)
    chat_messages = create_chat_completions(system_content, user_content)
    print(chat_messages.content)

def main_2():
    # (2) create_chat_completions_image_input(q_text, image_url_string)
    res = create_chat_completions_image_input(q_text, image_url_string)
    print(res)
    # content部分を取得して表示
    content = res.message.content.replace("。", "。\n")
    print(content)

def main_3():
    # (3) create_chat_completions_streaming(system_content, user_content)
    res = create_chat_completions_streaming(system_content, user_content2)
    print(res)

def main_4():
    # (4) chat completions log
    role_user_content = "Hello world!"
    msg, logprobs = create_chat_completions_logprobs(role_user_content, top_logprobs=2)
    pprint.pprint(msg)
    pprint.pprint(logprobs)

def main_5():
    # (5) function-tool
    function_messages = [{"role": "user", "content": "What's the weather like in Boston today?"}]
    response = create_chat_completions_functions_with_tools(function_messages)
    pprint.pprint(response)

def main_6():
    # (6) create_audio_transcription(speech_mp3)
    speech_mp3 = 'data/output.mp3'
    response = create_audio_transcription(speech_mp3)
    print(response)

def multiply(x, y):
    """
    2つの整数 x, y を入力とし、
    'x X y = x*y' という文字列を返す関数
    """
    # 計算
    result = x * y
    # 結果を文字列で整形
    return f"{x} X {y} = {result}"

def concat_strings(x, y):
    """
    2つの文字列 x, y を入力とし、
    x と y を連結した文字列を返す関数
    """
    return f"{x}{y}"

def main_7():
    # (7) GradioのChat
    # Gradio で UI を構築
    with gr.Blocks() as demo:
        gr.Markdown("## INPUT integer・string")

        with gr.Row():
            with gr.Column(scale=1, min_width=300):
                # 入力
                input1 = gr.Number(label="INPUT1: integer", value=1, precision=0)
                input2 = gr.Number(label="INPUT2: integer", value=1, precision=0)
                input3 = gr.Textbox(label="INPUT1: string", value="")
                input4 = gr.Textbox(label="INPUT2: string", value="")
                # ボタン
                button = gr.Button("計算する")
                button2 = gr.Button("連結する")

            with gr.Column(scale=1, min_width=300):
                # 出力
                output = gr.Textbox(label="OUTPUT")

        # ボタンが押されたときに実行する処理
        button.click(
            fn=multiply,  # 実行する関数
            inputs=[input1, input2],  # 関数への入力
            outputs=output  # 関数の出力を表示する場所
        )
        # ボタンが押されたときに実行する処理
        button2.click(
            fn=concat_strings,  # 実行する関数
            inputs=[input3, input4],  # 関数への入力
            outputs=output  # 関数の出力を表示する場所
        )

        # アプリを起動
        demo.launch()

if __name__ == "__main__":
    # main_1()
    # main_2()
    # main_3()
    # main_4()
    # main_5()
    # main_6()
    main_7()

