# 0_check_json_format.py
import json
import argparse

file_path = "./python_code_to_dict.json"

def check_json_format(file_path):
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            # ファイル内容を読み込む
            data = file.read()
            # JSONパースを試みる
            json_data = json.loads(data)
        print("ファイルは正しいJSON形式です。")
        print("トップレベルのキー:", list(json_data.keys()))
    except json.JSONDecodeError as e:
        print(f"JSONDecodeError: ファイルは不正なJSON形式です。エラーの詳細: {e}")
    except Exception as e:
        print(f"その他のエラー: {e}")

def main():
    parser = argparse.ArgumentParser(description="Check if a file is in valid JSON format and display its top-level keys.")
    parser.add_argument("./python_code_to_dict.json", help="Path to the JSON file to be checked")
    args = parser.parse_args()

    check_json_format(args.file_path)

if __name__ == "__main__":
    main()

