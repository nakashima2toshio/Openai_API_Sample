# a3_構造化出力による関数呼び出し
"""
構造化された出力
導入
JSON は、アプリケーションがデータを交換するために世界で最も広く使用されている形式の 1 つです。
構造化出力は、モデルが常に指定されたJSON スキーマに準拠した応答を生成することを保証する機能です。
そのため、モデルが必要なキーを省略したり、無効な列挙値を幻覚させたりすることを心配する必要はありません。
構造化出力の利点は次のとおりです。

信頼性の高い型安全性:誤った形式の応答を検証したり再試行したりする必要がない
明示的な拒否:安全性に基づくモデルの拒否がプログラムで検出可能になりました
よりシンプルなプロンプト:一貫したフォーマットを実現するために、強い言葉を使ったプロンプトは不要

[構造化出力と JSON モード]
構造化出力はJSON モードの進化形です。
チャット完了 API、アシスタント API、微調整 API、バッチ API でサポートされています。

# sdk object ---------------
- ステップ1: オブジェクトを定義する
- ステップ2: API呼び出しでオブジェクトを指定する
- ステップ3: エッジケースを処理する
- ステップ4: 生成された構造化データを型安全に使う
- 構造化された出力による拒否

# 手動スキーマ ---------------
ステップ1: スキーマを定義する
ステップ2: API呼び出しでスキーマを指定する
ステップ3: エッジケースを処理する
ステップ4: 生成された構造化データを型安全に使う
構造化された出力による拒否

"""
from pydantic import BaseModel
from openai import OpenAI
import pprint

model_4o = "gpt-4o-2024-08-06"
model_4o_mini = "gpt-4o-mini"
client = OpenAI()

class CalendarEvent(BaseModel):
    name: str
    date: str
    participants: list[str]

def create_chat_completions_structured_output_event(model, messages):
    # (1) structured_output default
    completion = client.beta.chat.completions.parse(
        model="gpt-4o-2024-08-06",
        messages=messages,
        response_format=CalendarEvent,
    )
    return completion.choices[0].message.parsed
"""
- Menu
- (2-1) chain of thought: 思考の連鎖 - 思考の連鎖に基づく数学指導のための構造化された出力
- (2-2) structured data extraction: 構造化データ出力 - 研究論文などの非構造化入力データから抽出するための構造化フィールドを定義できます。
- (2-3) UI generation: UI生成
- (2-4) moderation: 節度
"""
# (2-1) 思考の連鎖に基づく数学指導のための構造化された出力
class Step(BaseModel):
    explanation: str
    output: str

class MathReasoning(BaseModel):
    steps: list[Step]
    final_answer: str

def parse_chat_completions_structured_output(model, messages):
    # (2-1) chain of thought: 思考の連鎖
    completion = client.beta.chat.completions.parse(
        model=model,
        messages=messages,
        response_format=MathReasoning,
    )

    math_reasoning = completion.choices[0].message.parsed
    return math_reasoning

# (2-2) structured data extraction: 構造化データ出力
class ResearchPaperExtraction(BaseModel):
    title: str
    authors: list[str]
    abstract: str
    keywords: list[str]

def parse_chat_completions_structured_data_extraction(model, messages):
    completion = client.beta.chat.completions.parse(
        model=model,
        messages=[
            {"role": "system", "content": "You are an expert at structured data extraction. You will be given unstructured text from a research paper and should convert it into the given structure."},
            {"role": "user", "content": "..."}
        ],
        response_format=ResearchPaperExtraction,
    )
    research_paper = completion.choices[0].message.parsed
    return research_paper

# (2-3) UI generation: UI生成
# (2-4) moderation: 節度

"""
(3) response_formatで構造化出力を使用する方法
新しい SDK ヘルパーで構造化出力を使用して
- モデルの出力を目的の形式に解析したり、
- JSON スキーマを直接指定したりできます。
"""


def main():
    model = model_4o

    # (1) structured outputs default
    messages = [
            {"role": "system", "content": "Extract the event information."},
            {"role": "user", "content": "Alice and Bob are going to a science fair on Friday."},
        ]
    # event = create_chat_completions_structured_output_event(model, messages, response_format)
    # pprint.pprint(event)

    # (2) structured outputs parse:
    # 思考の連鎖
    # モデルに構造化されたステップバイステップの方法で回答を出力するように要求し、
    # ユーザーを解決に導くことができます。
    messages2 = [
        {"role": "system",
         "content": "You are a helpful math tutor. Guide the user through the solution step by step."},
        {"role": "user", "content": "how can I solve 8x + 7 = -23"}
    ]
    response2 = parse_chat_completions_structured_output(model, messages2)
    pprint.pprint(response2)
    for msg in response2.steps:
        print(f"説明: {msg.explanation} - \n出力: {msg.output}")
        print('----------')

    # (3) 研究論文などの非構造化入力データから抽出するための構造化フィールドを定義できます。
    messages3 = ""
    response3 = parse_chat_completions_structured_data_extraction(model, messages3)
    pprint.pprint(response3)


if __name__ == "__main__":
    main()

