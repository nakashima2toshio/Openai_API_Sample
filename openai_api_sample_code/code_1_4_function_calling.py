# 03 function calling - 大規模な言語モデルを外部ツールに接続する方法
"""
* [関数呼び出しは、
- (1) chat completion チャット・コンプリーションAPI
- (2) assistant アシスタントAPI
- (3) batch バッチ API
ステップ1: モデルが呼び出せるコードベースの関数を選択する
        - 関数呼び出しの開始点は、モデルが引数を生成できるようにする独自のコードベース内の関数を選択すること
ステップ2: モデルに関数を記述して、呼び出す方法を知らせる
        -
ステップ3: 関数定義を利用可能な「ツール」としてモデルに渡し、メッセージも渡す
        - tools, message, response の定義
ステップ4: モデル応答を受信して処理する
        -
ステップ5: 関数呼び出しの結果をモデルに返す
        -
"""
# ------------------------------------
""" Assistant tools -------------------
(1) File Search: ファイル検索
- ファイルを処理および検索するための組み込みRAGツール
- https://platform.openai.com/docs/assistants/tools/file-search

(2) Code Interpreter: コードインタープリター
- Pythonコードを書いて実行し、ファイルやさまざまなデータを処理する
- https://platform.openai.com/docs/assistants/tools/code-interpreter

(3) Function Calling: 関数呼び出し
- 独自のカスタム関数を使用してアプリケーションと対話する
- https://platform.openai.com/docs/assistants/tools/function-calling
"""
from openai import OpenAI
import pprint
import json  # 追加: 引数をJSON文字列に変換するために使用

client = OpenAI()
model_4o = 'gpt-4o'

def get_delivery_date(order_id):
    # 配送日を取得するモック
    # 実際のシナリオでは、この関数はデータベースや外部APIを参照します。
    delivery_dates = {
        "order_12345": "2024-09-05",
        "order_67890": "2024-09-10"
    }
    return delivery_dates.get(order_id, "Unknown order ID")


def create_chat_completions_tools(model, messages, tools):
    response = client.chat.completions.create(
        model=model,
        messages=messages,
        tools=tools
    )
    return response

def main():
    tools_name = "get_delivery_date"
    tools_description = "顧客の注文に対する配送日を取得します。例えば、顧客が「私の荷物はどこ？」と尋ねたときにこの機能を呼び出します。"
    tools = [
        {
            "type": "function",
            "function": {
                "name": tools_name,
                "description": tools_description,
                "parameters": {
                    "type": "object",
                    "properties": {
                        "order_id": {
                            "type": "string",
                            "description": "顧客の注文ID。"
                        }
                    },
                    "required": ["order_id"],
                    "additionalProperties": False
                }
            }
        }
    ]

    messages = []
    messages.append({"role": "system",
                     "content": "あなたは親切なカスタマーサポートアシスタントです。提供されたツールを使用して、ユーザーを支援してください。"})
    messages.append({"role": "user", "content": "こんにちは、私の注文の配送日を教えてください。"})
    messages.append(
        {"role": "assistant", "content": "こんにちは！それをお手伝いできます。注文IDを教えていただけますか？"})
    messages.append({"role": "user", "content": "order_12345だと思います。"})

    # get_delivery_dateの関数呼び出しをシミュレート
    order_id = "order_12345"  # ユーザー入力をモック
    delivery_date = get_delivery_date(order_id)

    # argumentsをJSON文字列として渡す
    messages.append({
        "role": "assistant",
        "function_call": {
            "name": tools_name,
            "arguments": json.dumps({"order_id": order_id})  # ここで引数を文字列に変換
        }
    })

    # アシスタントが関数呼び出しの結果を返すと仮定
    messages.append({
        "role": "function",
        "name": tools_name,
        "content": delivery_date
    })

    response = create_chat_completions_tools(model_4o, messages, tools)
    pprint.pprint(response.choices[0].message.content)

if __name__ == '__main__':
    main()
