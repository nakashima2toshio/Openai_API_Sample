# 同期処理版：
# document/*.txt からFine-tuning用のデータを作成する。
import re
import glob
from openai import OpenAI
import pathlib
import json
import pprint


class CreateRagFineTuningData:
    def __init__(self):
        self.python_code_to_dict = {}
        self.paragraph_to_dict = {}
        self.py_no = 1
        self.content = ''
        self.jsonl_data = ''

    def list_txt_files(self):
        # /document/ディレクトリ内の .txt ファイルを取得
        return sorted(glob.glob('./document/*.txt'))

    def generate_subtitle(self, code_block, title):
        prompt = f"The title of this code is {title}. Here, a sentence describing the function in detail should be written as a subtitle, with a maximum length of 80 characters. The following is the code:\n\n{code_block}"
        client = OpenAI()
        response = client.chat.completions.create(
            model="gpt-4o-mini",
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
        return response.choices[0].message.content.strip("** ")

    def generate_question(self, paragraph, title):
        prompt = (f"The task here is to read the attached explanatory text and create a question to which the "
                  f"explanatory text answers. Now, the attached explanatory text is part of an explanatory text whose"
                  f" title is {title}. Now, write only the question statement in 80 words or less. The following is "
                  f"the explanatory text that will serve as the answer.:\n\n{paragraph}")
        client = OpenAI()
        response = client.chat.completions.create(
            model="gpt-4o-mini",
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

    def generate_prompt_completion(self, content):
        prompt = ("以下のドキュメントから、chatgptのfine-tuning用のデータとして、QAを全体、および、詳細、個別の事象が把握できるように、"
                  "必要なだけ作成しなさい。"
                  "オブジェクトには 'prompt' キーには質問を入れ、'completion'キーにはその質問に対する回答を入れ、"
                  "JSONL形式で作成しなさい。")
        prompt = prompt + content
        client = OpenAI()
        response = client.chat.completions.create(
            model="gpt-4o-mini",
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

    def split_into_paragraphs(self, file_path):
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

    def process_files(self):
        file_lists = self.list_txt_files()

        for file_path in file_lists:
            file_name_without_extension = pathlib.Path(file_path).stem
            paragraphs, python_blocks = self.split_into_paragraphs(file_path)
            title = file_name_without_extension[3:]

            for python_block in python_blocks:
                subtitle = self.generate_subtitle(python_block, title)
                python_title_subtitle_code = {
                    "no": self.py_no,
                    "title": title,
                    "subtitle": subtitle,
                    "code": python_block
                }
                self.python_code_to_dict[self.py_no] = python_title_subtitle_code
                self.py_no += 1

        self.py_no = 1
        for file_path in file_lists:
            file_name_without_extension = pathlib.Path(file_path).stem
            paragraphs, python_blocks = self.split_into_paragraphs(file_path)
            title = file_name_without_extension[3:]

            for paragraph in paragraphs:
                question = self.generate_question(paragraph, title)
                paragraph_dat = {
                    "py_no": self.py_no,
                    "title": title,
                    "question": question,
                    "paragraph": paragraph
                }
                self.paragraph_to_dict[self.py_no] = paragraph_dat
                self.py_no += 1
                print(f'{self.py_no}_', end='')

        self.py_no = 1
        for file_path in file_lists:
            with open(file_path, 'r') as file:
                self.content = file.read()
            data = dict()
            data = self.generate_prompt_completion(self.content)
            self.jsonl_data = self.jsonl_data + data

            self.py_no += 1
            print(f'{self.py_no}-', end='')

    def save_to_json(self):
        # 辞書をJSONファイルに書き込む
        with open('python_code_to_dict.json', 'w') as fp:
            json.dump(self.python_code_to_dict, fp, indent=4)

        with open('paragraph_to_dict.json', 'w') as f:
            json.dump(self.paragraph_to_dict, f, indent=4)

        with open('para_jsonl_data.json', 'w') as flp:
            json.dump(self.jsonl_data, flp, indent=4)


def main():
    instance = CreateRagFineTuningData()
    instance.process_files()
    instance.save_to_json()


if __name__ == "__main__":
    main()
