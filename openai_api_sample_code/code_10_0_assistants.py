# Assistants create_assistant
# cookbook: https://cookbook.openai.com/examples/assistants_api_overview_python
from openai import OpenAI
import pprint

client = OpenAI()
model_4o_mini = "gpt-4o-mini"

"""
JSON のフィールドに入力し、事前定義された一連の手順を推論して、
ユーザーの会話と取得された関連情報に基づいて最終的な応答を生成します。
tools_type = [code_interpreter, file_search, functions]
"""


def create_assistant_interpreter(instructions, name):
    # (1) code_interpreterツールを持つアシスタントを作成します。
    # ここに作成される。=> https://platform.openai.com/assistants/
    # code_interpreterを使用することで、アシスタントがユーザーの質問に対してコードを記述し、
    # その結果を計算して返答することができます。
    my_assistant = client.beta.assistants.create(
        instructions=instructions,
        name=name,
        tools=[{"type": "code_interpreter"}],
        model=model_4o_mini,
    )
    return my_assistant


def create_assistant_files(instructions_file_search):
    # code_interpreterツール付きのアシスタントを作成
    """
    # モデルを呼び出し、ツールを使用してタスクを実行できるアシスタントを構築します。
    アシスタントで有効になっているツールのリスト。アシスタントごとに最大
    128個のツールを設定できます。ツールのタイプは
    code_interpreter、、、file_searchまたはのいずれかですfunction。
    """
    my_assistant = client.beta.assistants.create(
        instructions=instructions_file_search,
        name="HR Helper",
        tools=[{"type": "file_search"}],
        tool_resources={"file_search": {"vector_store_ids": ["vs_123"]}},
        model=model_4o_mini
    )
    return my_assistant

def question_with_assistant(my_assistant):
    # 作成したアシスタントを使用してコードを実行
    response = my_assistant.interact(
        messages=[
            {"role": "user", "content": "What is the sum of the numbers from 1 to 10?"}
        ]
    )
    # 結果の表示
    # print(response['choices'][0]['message']['content'])
    return response.choise[0].message.content

def create_assistant_functions(instructions):
    """
    #
    """
    my_assistant = client.beta.assistants.create(
        instructions=instructions,
        name="HR Helper",
        tools=[{"type": "function"}],
        tool_resources={"function": {"vector_store_ids": ["vs_123"]}},
        model=model_4o_mini
    )
    return my_assistant


def list_assistants(limit=20):
    my_assistants = client.beta.assistants.list(
        order="desc",
        limit=20,
    )
    return my_assistants.data


def retrieval_assistant():
    my_assistant = client.beta.assistants.retrieve("asst_abc123")
    return my_assistant


def update_assistant():
    my_updated_assistant = client.beta.assistants.update(
        "asst_abc123",
        instructions="あなたは人事ボットで、ファイルにアクセスし、会社のポリシーを 常にどちらかのファイルの情報を使って回答してください。",
        name="HR Helper",
        tools=[{"type": "file_search"}],
        model=model_4o_mini
    )

    return my_updated_assistant


def delete_assistant(delete_model_name):
    # delete_model_name = "asst_abc123"
    response = client.beta.assistants.delete(delete_model_name)
    return response


def main():
    # Step 1: Create an Assistant
    # instructions = "あなたは数学の家庭教師です。質問をされたら、Pythonコードを書いて実行し、質問に答えます。"
    # name = "Math Tutor"
    # assistant = create_assistant_interpreter(instructions, name)
    # pprint.pprint(assistant.id)
    # id='asst_LeZ4YcFrUoTDE3JQV9P6nPI1'

    # Step 2: Create a Thread
    thread = client.beta.threads.create()
    #
    # Step 3: Add a Message to the Thread
    message=client.beta.threads.messages.create(
        thread_id=thread.id,
        role="user",
        content="What's the weather in San Francisco today and the likelihood it'll rain?",
    )
    pprint.pprint(message)

    # Step 4: Create a Run



    # instructions_file_search= ''

if __name__ == '__main__':
    main()

"""
response = {
  "id": "asst_abc123",
  "object": "assistant",
  "created_at": 1698984975,
  "name": "Math Tutor",
  "description": null,
  "model": "gpt-4o",
  "instructions": "You are a personal math tutor. When asked a question, write and run Python code to answer the question.",
  "tools": [
    {
      "type": "code_interpreter"
    }
  ],
  "metadata": {},
  "top_p": 1.0,
  "temperature": 1.0,
  "response_format": "auto"
}

"""
