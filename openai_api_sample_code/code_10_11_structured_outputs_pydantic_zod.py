# 構造化された出力
"""
## モデルをシステム内のツール、関数、データなどに接続する場合は、関数呼び出しを使用する必要があります。
## モデルがユーザーに応答するときに出力を構造化したい場合は、構造化されたresponse_format
"""
pass
"""
構造化出力は、モデルが常に指定されたJSON スキーマに準拠した応答を生成することを保証する機能です。
- コードで定義されたスキーマに準拠する非構造化テキストから情報を抽出する方法を示します。

*** 構造化出力は、OpenAI API で 2 つの形式で利用できます。
- 関数呼び出しを使用する場合
- json_schema応答形式を使用する場合
"""

from pydantic import BaseModel
from openai import OpenAI


class CalendarEvent(BaseModel):  #  BaseModelを必ず継承すること。
    name: str
    date: str
    participants: list[str]

def structured_outputs():
    completion = client.beta.chat.completions.parse(
        model=model_4o,
        messages=[
            {"role": "system", "content": "Extract the event information."},
            {"role": "user", "content": "Alice and Bob are going to a science fair on Friday."},
        ],
        response_format=CalendarEvent,
    )
    return completion

def main():
    event = structured_outputs()
    print(event.parsed)
    event = client.completions.choices[0].message.parsed

if __name__ == "__main__":
    model_4o = "gpt-4o-2024-08-06"
    model_4o_mini = "gpt-4o-mini"

    client = OpenAI()
    main()

