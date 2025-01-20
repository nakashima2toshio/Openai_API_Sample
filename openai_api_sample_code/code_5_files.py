# files
from openai import OpenAI
import requests
import os

OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY")
client = OpenAI()


def create_files(mydata_jsonl, purpose):
    """
    ファイルをアップロード
    さまざまなエンドポイントで使用できるファイルをアップロードします。
    個々のファイルのサイズは最大 512 MB で、
    1 つの組織によってアップロードされるすべてのファイルのサイズは最大 100 GB です。
    """
    response = client.files.create(
        file=open(mydata_jsonl, "rb"),
        purpose=purpose  # "fine-tune"
    )
    return response


def list_files():
    response = client.files.list()
    return response


def retrieve_files(file_name):
    response = client.files.retrieve(file_name)  # "file-abc123"
    return response


def delete_files(file_path):
    response = client.files.delete(file_path)
    return response


def upload_file(upload_id):
    # APIのエンドポイント
    upload_id = upload_id
    url = f"https://api.openai.com/v1/uploads/{upload_id}/parts"

    # ヘッダー（APIキーは実際の値に置き換えてください）
    headers = {
        "Authorization": f"Bearer {OPENAI_API_KEY}",
    }

    # 各パーツデータ（64MB以下で分割されたデータを想定）
    parts = [
        {"data": "data_of_part_1"},
        {"data": "data_of_part_2"},
        {"data": "data_of_part_3"}
    ]

    # 各パーツのpart_idを保存するリスト
    part_ids = []

    # 各パーツを順不同でアップロード
    for part in parts:
        files = {"data": part["data"]}

        response = requests.post(url, headers=headers, files=files)

        # レスポンスからpart_idを取得して保存
        part_id = response.json().get("part_id")
        part_ids.append(part_id)

        print(f"Uploaded part with part_id: {part_id}")

    # アップロードの順番を指定して完了を通知
    complete_url = f"https://api.openai.com/v1/uploads/{upload_id}/complete"
    complete_data = {
        "part_ids": part_ids  # この順序で結合されます
    }

    response = requests.post(complete_url, json=complete_data, headers=headers)

    print("Upload complete response:", response.status_code, response.json())

    return response.status_code, response.json()


# upload - complete upolad
"""
API の用途とステップバイステップの説明
この API の用途は、ファイルを分割してアップロードする際に、全てのパーツが正常にアップロードされたことを通知するために使用されます。このプロセスは、通常大きなファイルを扱う場合や、アップロードの再開をサポートするシステムで使用されます。

ステップ 1: ファイルの分割
大きなファイルを複数の小さな部分（パーツ）に分割します。例えば、大きなビデオファイルをアップロードする場合、ファイルを複数のチャンクに分割することがあります。

ステップ 2: 各パーツのアップロード
それぞれのパーツを API にアップロードします。アップロードが成功するたびに、サーバーはそのパーツの part_id を返します。

ステップ 3: アップロードの完了を通知
全てのパーツのアップロードが完了したら、この complete エンドポイントを使用して、全ての part_id をサーバーに送信し、アップロードが完了したことを通知します。

これにより、サーバーは全てのパーツを結合し、元のファイルを再構築します。エンドポイントは、アップロードが成功したかどうかのステータスを返します。

この一連のステップにより、大きなファイルのアップロードが効率的かつ確実に行われることを保証します。
"""


def endpoint_uploads_complete(upload_file, part_ids):
    # APIのエンドポイント
    url = f"https://api.openai.com/v1/uploads/{upload_file}/complete"

    # ヘッダー（APIキーは実際の値に置き換えてください）
    OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY")
    authorization = f"Bearer {OPENAI_API_KEY}"
    headers = {
        "Authorization": authorization,  # YOUR_API_KEYを実際のAPIキーに置き換えてください
        "Content-Type": "application/json"
    }

    # リクエストデータ
    data = {
        "part_ids": part_ids  # ["part_def456", "part_ghi789"]
    }

    # POSTリクエストを送信
    response = requests.post(url, json=data, headers=headers)

    # レスポンスを表示
    print(response.status_code)
    print(response.json())
    return response.status_code, response.json()


# response
"""
{
  "data": [
    {
      "id": "file-abc123",
      "object": "file",
      "bytes": 175,
      "created_at": 1613677385,
      "filename": "salesOverview.pdf",
      "purpose": "assistants",
    },
    {
      "id": "file-abc123",
      "object": "file",
      "bytes": 140,
      "created_at": 1613779121,
      "filename": "puppy.jsonl",
      "purpose": "fine-tune",
    }
  ],
  "object": "list"
}
"""
