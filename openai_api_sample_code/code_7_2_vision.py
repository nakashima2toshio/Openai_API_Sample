# Learn how to use vision capabilities to understand images.
"""
## from Document
視覚機能を使用して画像を理解する方法を学びます。

画像は、主に 2 つの方法でモデルで利用できるようになります。
画像へのリンクを渡すか、リクエストで直接 base64 でエンコードされた画像を渡すかです。
画像はメッセージで渡すことができます
"""
# Quick Start
import os
from openai import OpenAI
import base64
import requests

api_key = os.environ.get('OPENAI_API_KEY')
model_gpt_4o_mini = "gpt-4o-mini"
client = OpenAI()


# --------------------------------------------------------------
def create_chat_completion_with_image_url(q_text: str, image_url_link: str):
    # (1) image URL
    response1 = client.chat.completions.create(
        model=model_gpt_4o_mini,
        messages=[
            {
                "role": "user",
                "content": [
                    {"type": "text", "text": q_text},
                    {
                        "type": "image_url",
                        "image_url": {
                            "url": image_url_link,
                        },
                    },
                ],
            }
        ],
        max_tokens=300,
    )
    return response1.choices[0]


# ------------------------------------------------------------
# (2) Base64エンコードされた画像のアップロード
# Function to encode the bse64 image
def encode_image(image_path):
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode('utf-8')


def create_chat_completion_base64_encoded_image(q_text, image_path):
    # Path to your image
    image_path = image_path  # "path_to_your_image.jpg"

    # Getting the base64 string
    base64_image = encode_image(image_path)

    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {api_key}"
    }

    payload = {
        "model": model_gpt_4o_mini,
        "messages": [
            {
                "role": "user",
                "content": [
                    {
                        "type": "text",
                        "text": q_text
                    },
                    {
                        "type": "image_url",
                        "image_url": {
                            "url": f"data:image/jpeg;base64,{base64_image}"
                        }
                    }
                ]
            }
        ],
        "max_tokens": 300
    }

    response2 = requests.post("https://api.openai.com/v1/chat/completions", headers=headers, json=payload)
    return response2.json()


# ------------------------------------------------------------
# (3) 複数の画像入力
def create_chat_completion_multi_images(q_text, image_url_links):
    response3 = client.chat.completions.create(
        model=model_gpt_4o_mini,
        messages=[
            {
                "role": "user",
                "content": [
                    {
                        "type": "text",
                        "text": q_text,
                    },
                    {
                        "type": "image_url",
                        "image_url": {
                            "url": image_url_links[0],
                        },
                    },
                    {
                        "type": "image_url",
                        "image_url": {
                            "url": image_url_links[1],
                        },
                    },
                ],
            }
        ],
        max_tokens=300,
    )
    #print(response3.choices[0])
    return response3.choices[0]


# ------------------------------------------------------------
# (4) 低忠実度または高忠実度の画像理解
def create_chat_completion_high_base64_encoded_images(q_text, image_url_link):
    response4 = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {
                "role": "user",
                "content": [
                    {"type": "text", "text": q_text},
                    {
                        "type": "image_url",
                        "image_url": {
                            "url": image_url_link,
                            "detail": "high"
                        },
                    },
                ],
            }
        ],
        max_tokens=300,
    )

    # print(response4.choices[0].message.content)
    return response4.choices[0]


# ------------------------------------------------------------

def main():
    q_text = "この画像の説明を詳しく記述しなさい。"
    image_url_link = "https://article-image.travel.navitime.jp/img/NTJmat0459/n_mat0437_1.jpg"
    image_path = './akb48.png'
    image_url_links = ["https://article-image.travel.navitime.jp/img/NTJmat0459/n_mat0437_1.jpg",
                       "https://www.ooigawachaen.co.jp/blog/wp-content/uploads/2020/09/202009_02.jpg"]

    # (1) image_URL画像の説明。
    # response1 = create_chat_completion_with_image_url(q_text, image_url_link)
    # print(response1.message.content.replace('。', '。\n'))

    # (2) Base64エンコードされた画像のアップロード
    # response2 = create_chat_completion_base64_encoded_image(q_text, image_path)  # response2.json()
    # print(response2.message.content.replace('。', '。\n'))

    # (3) 複数の画像入力
    # response3 = create_chat_completion_multi_images(q_text, image_url_links)  # response3.choices[0]
    # print(response3.message.content.replace('。', '。\n'))

    # (4) 低忠実度または高忠実度の画像理解
    response4 = create_chat_completion_high_base64_encoded_images(q_text, image_url_link)
    print(response4.message.content.replace('。', '。\n'))


if __name__ == "__main__":
    main()
