## モデルをシステム内のツール、関数、データなどに接続する場合は、関数呼び出しを使用する必要があります。
## モデルがユーザーに応答するときに出力を構造化したい場合は、構造化されたresponse_format 

#### tools: 関数呼び出し
- https://platform.openai.com/docs/guides/function-calling
```pythohn
# 追加情報
# structured_outputs: 関数定義内でstrict: trueを設定することで、
# 構造化された出力を使用できます。
# この機能は、gpt-4-0613およびgpt-3.5-turbo-0613以降のモデルで利用可能です。
{
  "functions": [  # モデルが呼び出せる関数を定義します。
    {.            # 各関数には名前、説明、そしてパラメータの定義が含まれます。
      "name": "get_weather",  # 関数名
      "description": "指定された都市の現在の天気を取得します。",
      "parameters": {
        "type": "object",
        "properties": {　      # 関数の引数の定義、複数：列挙する
          "city": {　
            "type": "string",
            "description": "天気を取得する都市の名前"
          }
        },
        "required": ["city"].  # 必須の引数名
      }
    }
  ],
  "function_call": {           # 呼び出す関数の名前と引数を指定します。
    "name": "get_weather",
    "arguments": {
      "city": "San Francisco"
    }
  },
  "tool_choice": "weather_api", # 使用するツールを指定します。
  "finish_reason": "tool_calls" # 関数呼び出しの完了理由を示します。
}
```
