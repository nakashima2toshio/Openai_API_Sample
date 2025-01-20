# 0_extract_text_to_paragraph_and_python_code.py
"""
Overview:

[Input]: 　　カレント・ディレクトリーのテキストファイル（./*.txt）全てから
[Process]:　 テキスト内の　Pyhon-code-block と　その他の説明文（整形して）　を別々に抽出する。
[Output]:　　 ・python_code_dict.json
            　・paragraph_dict.json
"""
# 関数のテスト　<-------- コードの練習。部分の開発
import re
import glob
from openai import OpenAI
import pathlib
import json
import pprint


def list_txt_files():
    # 現在のディレクトリ内の .txt ファイル名のリストを取得
    txt_files = sorted(glob.glob('*.txt'))
    return txt_files


# ChatGPTのAPIを使用してpython-コードブロックに適切なタイトルを生成する関数
def generate_subtitle(code_block, title):
    prompt = f"The title of this code is {title}. Here, a sentence describing the function in detail should be written as a subtitle, with a maximum length of 80 characters. The following is the code:\n\n{code_block}"
    client = OpenAI()
    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {"role": "system",
             "content": "You are a professional python developer, a helpful assistant and good at chatgpt APIs."},
            {"role": "user", "content": prompt},
        ],
        max_tokens=50,
        n=1,
        stop=None,
        temperature=0.5
    )
    # title = response.choices[0].message.content
    return response.choices[0].message.content


def generate_question(paragraph, title):
    prompt = f"The task here is to read the attached explanatory text and create a question to which the explanatory text answers. Now, the attached explanatory text is part of an explanatory text whose title is {title}. Now, write only the question statement in 80 words or less. The following is the explanatory text that will serve as the answer.:\n\n{paragraph}"
    client = OpenAI()
    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {"role": "system",
             "content": "You are a professional python developer, a helpful assistant and good at chatgpt APIs."},
            {"role": "user", "content": prompt},
        ],
        max_tokens=50,
        n=1,
        stop=None,
        temperature=0.5
    )
    return response.choices[0].message.content


def split_into_paragraphs(file_path):
    with open(file_path, 'r') as file:
        content = file.read()

    # Pythonコードブロックを先に抽出し、それ以外の部分(pythonブロックを区切り文字として)を段落に分割
    python_blocks = re.findall(r'```python.*?```', content, re.DOTALL)
    non_python_parts = re.split(r'```python.*?```', content, flags=re.DOTALL)

    paragraphs = []

    # 各非コード部分をさらに段落に分ける
    for part in non_python_parts:
        paragraphs.extend(part.strip().split('\n\n'))

    return paragraphs, python_blocks


file_lists = list_txt_files()
paragraphs = list()
python_blocks = list()

python_code_dict = dict()
paragraph_dict = dict()
py_no = 1
for file_path in file_lists:
    file_name_without_extension = pathlib.Path(file_path).stem
    # ここで文章から、パラグラフとpythonコードを取り出す。
    paragraphs, python_blocks = split_into_paragraphs(file_path)
    title = file_name_without_extension[3:]

    for python_block in python_blocks:
        subtitle = generate_subtitle(python_block, title)
        python_title_subtitle_code = {"no": py_no, "title": title, "subtitle": subtitle, "code": python_block}
        python_code_dict[py_no] = python_title_subtitle_code
        py_no += 1

# Q/A => (jsonl - ex.) {"prompt": "<prompt text>", "completion": "<ideal generated text>"}
py_no = 1
for file_path in file_lists:
    file_name_without_extension = pathlib.Path(file_path).stem
    # ここで文章から、パラグラフとpythonコードを取り出す。
    paragraphs, python_blocks = split_into_paragraphs(file_path)
    title = file_name_without_extension[3:]

    for paragraph in paragraphs:
        question = generate_question(paragraph, title)
        paragraph_dat = dict()
        paragraph_dat["py_no"] = py_no
        paragraph_dat["title"] = title
        paragraph_dat["question"] = question
        paragraph_dat["paragraph"] = paragraph
        paragraph_dict[py_no] = paragraph_dat
        py_no += 1
        print(f'{py_no}_')

    # パラグラフをragデータ用とfine-tuning用にQAに取り出す。

# 修正：json.dump() を使用して辞書をJSONファイルに書き込む
with open('python_code_dict.json', 'w') as fp:
    json.dump(python_code_dict, fp, indent=4)  # indent=4 でフォーマットを見やすく

with open('paragraph_dict.json', 'w') as f:
    json.dump(paragraph_dict, f, indent=4)