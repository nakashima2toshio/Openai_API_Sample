# gr_show_oython_code.py
import json
import gradio as gr


# JSONファイルを読み込む
def load_data():
    with open("python_code_dict_clean.json", "r", encoding="utf-8") as f:
        data = json.load(f)
    return data


data = load_data()


# 選択肢用のデータを作成
def create_selector_options(data):
    options = []
    for key, value in data.items():
        options.append(f"{value['no']}: {value['title']} - {value['subtitle']}")
    return options


options = create_selector_options(data)


# 選択された項目に対応するコードを表示
def display_code(selected_item):
    # 選択された項目から`no`を取得
    no = selected_item.split(":")[0]
    # 該当する`code`を返す
    code = data[no]["code"]
    return code


# Gradioインターフェースの定義
def gradio_app():
    # セレクターと表示エリアを定義
    selector = gr.Dropdown(choices=options, label="Select no, title, subtitle")
    output = gr.Textbox(label="Code")

    # Gradioのインターフェースを作成
    gr.Interface(fn=display_code, inputs=selector, outputs=output, title="OpenAI API Code Display App").launch()


# アプリケーションを起動
if __name__ == "__main__":
    gradio_app()

