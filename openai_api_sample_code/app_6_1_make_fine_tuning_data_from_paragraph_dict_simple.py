# make_fine_tuning_data_from_paragraph_dict.py
import os
from openai import OpenAI
import json

client = OpenAI()
model_4o_mini = "gpt-4o-mini"

# OpenAI APIキーの設定
api_key = os.getenv("OPENAI_API_KEY")

# ステップ3: `prompt`と`completion`を生成する関数の作成
def create_finetune_data(data_dict):
    # `prompt`の作成: title, subtitle, code を使用して質問を作成
    prompt_q = f"以下のタイトル、サブタイトルからparagraphが回答となる様な質問を1つ作成してください。\n\nタイトル：{data_dict['title']} \n\n サブタイトル：{data_dict['question']} \n\n説明文：{data_dict['paragraph']} "

    # --- ここで、OpenAI APIを呼び出して、chat completionsを利用する。 ---
    response_q = client.chat.completions.create(
        model=model_4o_mini,  # 使用するモデル
        messages=[
            {"role": "system", "content": "あなたは有能なソフトウェア技術者のアシスタントです。"},
            {"role": "user", "content": prompt_q}
        ]
    )
    prompt = response_q.choices[0].message.content.strip()

    # codeが答。　`completion`
    prompt_a = f"{data_dict['paragraph']} \n\n"

    # 生成された`prompt`と`completion`を含むデータを返す
    val = {"prompt": prompt, "completion": prompt_a}
    return val


def main():
    # JSONファイルからデータを読み込む。
    with open('./paragraph_to_dict.json', 'r') as file:
        data = json.load(file)

    # ファインチューニング用データの生成
    # {"prompt": "prompt-data","completion": "content-data"}
    with open('./paragraph_data.jsonl', 'w', encoding='utf-8') as file:
        for key, value in data.items():
            # ステップ1: 質問データを生成
            prompt_completion_data = create_finetune_data(value)
            # ステップ5: 生成されたデータをJSONL形式で保存
            print(f"{key} --> {prompt_completion_data}")
            file.write(json.dumps(prompt_completion_data, ensure_ascii=False) + "\n")
    print("ファインチューニング用データが'./finetune_data_paragraph.jsonl'に保存されました。")


if __name__ == '__main__':
    main()
