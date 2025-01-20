# clean_python_code_dict.py
import json
import re

def clean_subtitle(json_data):
    for key, value in json_data.items():
        title = value.get("title", "")
        subtitle = value.get("subtitle", "")
        # 不要な文字列 "# " + title を除去
        # 大文字・小文字を無視して比較するため、両方を小文字に変換して処理
        # さらに先頭の'### ', '## ', '# 'も取り除く
        if subtitle.lower().startswith(f"# {title}\n"):
            json_data[key]["subtitle"] = subtitle[len(f"# {title}"):].strip()

        # 先頭にある "### ", "## ", "# " を正規表現で削除
        subtitle = re.sub(r'^#+\s+', '', subtitle)
        # subtitleを更新
        json_data[key]["subtitle"] = subtitle.strip()

    return json_data

def main():
    in_file = 'python_code_dict.json'
    out_file = 'python_code_dict_clean.json'

    with open (in_file, 'r', encoding='utf-8') as fp:
        json_data = json.load(fp)

    clean_data = clean_subtitle(json_data)

    with open(out_file, 'w', encoding='utf-8') as ofp:
        json.dump(clean_data, ofp, ensure_ascii=False, indent=4)

    print('clean complete')

if __name__ == "__main__":
    main()
