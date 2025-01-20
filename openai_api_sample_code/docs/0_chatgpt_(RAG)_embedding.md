### ChatGPT・エンベディング [RAG（Retrieval-Augmented Generation）]手順
##### https://openai.com/index/introducing-improvements-to-the-fine-tuning-api-and-expanding-our-custom-models-program/


| **ステップ**                        | **タスク**                                              | **ChatGPT API**     | **使用例モデル/API**     |
| ----------------------------------- | ------------------------------------------------------- | ------------------- | ------------------------ |
| 手順1: データセットの準備           | データセットを収集し、前処理を行う                      | 使用しない          | N/A                      |
| 手順2: データセットのエンベディング | テキストデータのエンベディングを生成                    | Embedding API       | `text-embedding-ada-002` |
| 手順3: エンベディングの保存         | エンベディングをベクターデータベースに保存              | 使用しない          | N/A                      |
| 手順4: ユーザークエリの処理         | ユーザークエリのエンベディングを生成                    | Embedding API       | `text-embedding-ada-002` |
| 手順5: ドキュメントの取得           | 上位N個の関連ドキュメントをベクターデータベースから取得 | 使用しない          | N/A                      |
| 手順6: 応答の生成                   | 取得したドキュメントとクエリを組み合わせて応答を生成    | Chat Completion API | `gpt-4`                  |
| 手順7: 最終回答の返却               | 生成された応答をユーザーに返す                          | 使用しない          | N/A                      |

#### 手順1: データセットの準備

- タスク: データセットを収集し、前処理を行う。これは、検索に使用するドキュメントやテキストデータを含みます。
- アクション:
  関連するすべてのドキュメントを収集します。
  テキストデータをクリーンアップして不要な情報を削除します。
  ドキュメントを適切なチャンクに分割し、各チャンクがモデルのトークン制限内に収まるようにします。
  ChatGPT API: このステップではAPIを使用しません。

#### 手順2: データセットのエンベディング

- タスク: ChatGPTのAPIを使用して、テキストデータの各チャンクに対してエンベディングを生成します。
- アクション:
  各ドキュメントまたはチャンクに対して、ChatGPTのAPIを使用してエンベディングを生成します。
  これらのエンベディングをベクターデータベースや効率的な検索が可能な構造に格納します。

```python
from openai import OpenAI

client = OpenAI()
# エンベディングを生成する例
response = client.embeddings.create(
    input="これはサンプルのドキュメントチャンクです。",
    model="text-embedding-ada-002"  # または他のエンベディングモデル
)

embedding = response['data'][0]['embedding']
```

ChatGPT API: Embedding API（例: text-embedding-ada-002）

#### 手順3: ベクターデータベースにエンベディングを保存

- タスク: エンベディングをベクターデータベースに保存し、高速で効率的な類似検索を可能にします。
- アクション:
  ベクターデータベース（例: Pinecone、FAISSなど）を選択します。
  メタデータ（例: ドキュメントID）とともにエンベディングをインデックス化します。
  ChatGPT API: このステップではAPIを使用しません。

#### 手順4: ユーザーのクエリ処理

- タスク: ユーザーがクエリを送信した際に、同じエンベディングモデルを使用してクエリをエンベディングし、ベクターデータベースから最も類似したドキュメントを取得します。
- アクション:
  ユーザーのクエリに対してChatGPTのAPIを使用してエンベディングを生成します。

```python
from openai import OpenAI

client = OpenAI()
query_embedding = client.embeddings.create(
    input="ユーザーのクエリテキスト。",
    model="text-embedding-ada-002"
)['data'][0]['embedding']
```

ベクターデータベースを使用して、クエリエンベディングに最も類似したドキュメントを検索します。
ChatGPT API: Embedding API（例: text-embedding-ada-002）

#### 手順5: 関連ドキュメントの取得

- タスク: ベクターデータベースから最も関連性の高い上位N個のドキュメントチャンクを取得します。
- アクション:
  クエリエンベディングを使用して、ベクターデータベースから最も類似した上位N個のドキュメントエンベディングを検索します。
  対応するドキュメントチャンクやテキストパッセージを抽出します。
  ChatGPT API: このステップではAPIを使用しません。

#### 手順6: 取得したドキュメントを使用して応答を生成

- タスク: 取得したドキュメントとユーザーのクエリを組み合わせて、ChatGPTを使用して一貫した情報豊かな応答を生成します。
- アクション:
  ユーザーのクエリと取得したドキュメントを含むプロンプトを構築します。
  ChatGPTのAPIを使用して、このプロンプトに基づいて応答を生成します。

```python
from openai import OpenAI

client = OpenAI()
response = client.chat.completions.create(
    model="gpt-4-mini",  # 適切なGPTモデルを選択
    messages=[
        {"role": "system", "content": "あなたは有用なアシスタントです。"},
        {"role": "user", "content": "ユーザーのクエリテキスト。"},
        {"role": "assistant", "content": "関連ドキュメント1の内容。"},
        {"role": "assistant", "content": "関連ドキュメント2の内容。"}
    ]
)
```

ChatGPT API: Chat Completion API

#### 手順7: 最終的な回答の返却

- タスク: 生成された応答をユーザーに返します。
- アクション:
  応答を適切にフォーマットして、ユーザーインターフェースに返します。
  ChatGPT API: このステップではAPIを使用しません。
