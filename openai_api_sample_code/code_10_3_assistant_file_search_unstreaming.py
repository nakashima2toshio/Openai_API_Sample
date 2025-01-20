# a16 assistant file search un-streaming
# [ファイル検索]は、
# 独自の製品情報やユーザーが提供するドキュメントなど、モデル外の知識でアシスタントを拡張します。
# OpenAI はドキュメントを自動的に解析してチャンク化し、埋め込みを作成して保存し、
# ベクトル検索とキーワード検索の両方を使用して関連コンテンツを取得し、ユーザーのクエリに回答します。
from openai import OpenAI
import time
import os
import pprint

model_4o_mini = "gpt-4o-mini"
tools_type = "file_search"

def initialize_client():
    return OpenAI()

def create_assistant(client, instructions):
    assistant = client.beta.assistants.create(
        name="Software Developer Assistant",
        instructions=instructions,
        model=model_4o_mini,
        tools=[{"type": tools_type}],
    )
    return assistant

def create_vector_store_and_upload_files(client, file_paths):
    vector_store = client.beta.vector_stores.create(name="Software API Information")
    file_streams = [open(path, "rb") for path in file_paths]
    file_batch = client.beta.vector_stores.file_batches.upload_and_poll(
        vector_store_id=vector_store.id, files=file_streams
    )
    return vector_store, file_batch

def update_assistant_with_vector_store(client, assistant_id, vector_store_id):
    assistant = client.beta.assistants.update(
        assistant_id=assistant_id,
        tool_resources={"file_search": {"vector_store_ids": [vector_store_id]}},
    )
    return assistant

def upload_file_and_create_thread(client, file_path, user_message):
    # さまざまなエンドポイントで使用できるファイルをアップロードします。
    # 個々のファイルのサイズは最大 512 MB で、
    # 1 つの組織によってアップロードされるすべてのファイルのサイズは最大 100 GB です。
    message_file = client.files.create(file=open(file_path, "rb"), purpose="assistants")
    thread = client.beta.threads.create(
        messages=[
            {
                "role": "user",
                "content": user_message,
                "attachments": [
                    {"file_id": message_file.id, "tools": [{"type": "file_search"}]}
                ],
            }
        ]
    )
    return thread

def create_and_poll_run(client, thread_id, assistant_id):
    run = client.beta.threads.runs.create_and_poll(
        thread_id=thread_id, assistant_id=assistant_id
    )
    return run

def display_results(client, thread_id, run_id):
    messages = list(client.beta.threads.messages.list(thread_id=thread_id, run_id=run_id))
    message_content = messages[0].content[0].text
    annotations = message_content.annotations
    citations = []

    for index, annotation in enumerate(annotations):
        message_content.value = message_content.value.replace(annotation.text, f"[{index}]")
        if file_citation := getattr(annotation, "file_citation", None):
            cited_file = client.files.retrieve(file_citation.file_id)
            citations.append(f"[{index}] {cited_file.filename}")

    print(message_content.value)
    print("\n".join(citations))

def main():
    print('Step0: initial ----------------')
    client = initialize_client()

    # ステップ1: アシスタントを作成
    print('Step1: アシスタントを作成 ----------------')
    instructions = """
    "あなたはソフトウェア開発者・OpenAI API利用のエキスパートで、
    ソフトウェア開発者を支援するアシスタントです。
    最新の知識ベースを使って、openaiのAPIに関連する質問に答えてください。
     - 旅程を作成します
     - ホテルを検索したり予約します
     - 交通機関を検索します
     - 出張で行くべきレストランや居酒屋を提案します
     - 出張にかかる概算費用を計算します
    #制約事項
     - ユーザーからのメッセージは日本語で入力されます
     - ユーザーからのメッセージから忠実に情報を抽出し、それに基づいて応答を生成します。
     - ユーザーからのメッセージに勝手に情報を追加したり、不要な改行文字を追加してはいけません
    """
    assistant = create_assistant(client, instructions)
    # assistant_id = assistant.id

    # ステップ2: ファイルをアップロードしてベクターストアに追加
    print('Step2: ファイルをアップロードしてベクターストアに追加 ----------------')
    file_paths = ["./python_code.json", "paragraph_to_dict.json"]
    vector_store, file_batch = create_vector_store_and_upload_files(client, file_paths)
    vector_store.id = vector_store.id

    # ステップ3: アシスタントを更新
    print('Step3: アシスタントを更新 ----------------')
    update_assistant = update_assistant_with_vector_store(client, assistant.id, vector_store.id)
    pprint.pprint(update_assistant)
    print('------------------')

    # ステップ4: スレッドを作成しファイルをアップロード
    print("Step4:ステップ4: スレッドを作成しファイルをアップロード ----------------" )
    thread = upload_file_and_create_thread(client, "./python_code.json", "OpenAiのAPIのサンプルプログラムは？")

    # ステップ5: 実行を作成し、出力を表示
    print('Step5: 実行を作成し、出力を表示 ----------------')
    run = create_and_poll_run(client, thread.id, update_assistant.id)
    display_results(client, thread.id, run.id)

if __name__ == "__main__":
    main()

