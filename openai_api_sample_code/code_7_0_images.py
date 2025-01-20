# image create image
import os
import requests
from openai import OpenAI
from PIL import Image
import pprint

model_generate_image = "dall-e-3"
client = OpenAI()


def download_image(url, save_path, file_name):
    # (util) URLから画像をダウンロード
    response = requests.get(url)

    # リクエストが成功したか確認
    if response.status_code == 200:
        # ファイル名を抽出
        # filename = os.path.basename(url)

        # 保存先のフルパスを作成
        full_path = os.path.join(save_path, file_name)

        # 画像を保存
        with open(full_path, 'wb') as file:
            file.write(response.content)

        print(f"画像が正常に保存されました: {full_path}")
    else:
        print(f"画像のダウンロードに失敗しました。ステータスコード: {response.status_code}")


def generate_images(prompt, size):
    # (1) プロンプトが与えられると、モデルは新しい画像を生成します。
    response = client.images.generate(
        model=model_generate_image,
        prompt=prompt,  # "A cute baby sea otter",
        n=1,  # 生成する画像の数
        size=size  # "1024x1024"
    )
    return response


def generate_image(image_in="akita_inu.png", image_out="akita_inu_mask.png"):
    # (1_1) 画像を開く
    img = Image.open("akita_inu.png").convert("RGBA")
    # 画像サイズを取得
    width, height = img.size

    # 新しい画像データリスト
    new_data = []

    # 特定の色を透明にする
    for item in img.getdata():
        # ここで透明にする色を指定します。例: 白 (255, 255, 255)
        if item[:3] == (255, 255, 255):
            new_data.append((255, 255, 255, 0))  # 透明にする
        else:
            new_data.append(item)

    # 新しいデータを元に画像を作成
    img.putdata(new_data)

    # 透明な画像を保存
    img.save("akita_inu_mask.png", "PNG")


def edit_images(image_in, image_mask, prompt, n=1):
    # (2) 元の画像とプロンプトを指定して、編集または拡張された画像を作成します。
    response = client.images.edit(
        image=open(image_in, "rb"),  # open("otter.png", "rb"),
        mask=open(image_mask, "rb"),  # open("mask.png", "rb"),
        prompt=prompt,  # "A cute baby sea otter wearing a beret",
        n=n,
        size="1024x1024"
    )
    return response


def create_variation_images(image_file_path, n=2):
    # (3) 指定された画像のバリエーションを作成します。
    response = client.images.create_variation(
        image=open(image_file_path, "rb"),
        n=n,
        size="1024x1024"
    )
    return response


def list_images():
    # (4) 現在入手可能なモデルをリストし、所有者や在庫状況などの各モデルの基本情報を提供します。
    response = client.models.list()
    return response


def main():
    # (1) プロンプトや入力画像が与えられると、モデルは新しい画像を生成します。
    prompt = "夏の公演で散歩している秋田犬"
    size = "1024x1024"
    response1 = generate_images(prompt, size)
    print(response1)
    save_path = './'
    url = response1.data[0].url
    file_name = 'akita_inu.png'
    download_image(url, save_path, file_name)

    """
    ImagesResponse(created=1724105566, 
    data=[Image(b64_json=None, revised_prompt='An Akita dog taking a stroll during a summer performance', 
    url='https://oaidalleapiprodscus.blob.core.windows.net/private/org-oCdLdxm1UFDyjxEUcfi29KLo/user-BrLHCafLCYdOZZs9pB5xd7ui/img-2LjXo7PFwPUAGDnYxiCPCnq4.png?st=2024-08-19T21%3A12%3A46Z&se=2024-08-19T23%3A12%3A46Z&sp=r&sv=2024-08-04&sr=b&rscd=inline&rsct=image/png&skoid=d505667d-d6c1-4a0a-bac7-5c84a87759f8&sktid=a48cca56-e6da-484e-a814-9c849652bcb3&skt=2024-08-19T18%3A33%3A14Z&ske=2024-08-20T18%3A33%3A14Z&sks=b&skv=2024-08-04&sig=d6xUptiwtmo6h9%2Bnq/4PLrfFYBqwyWBiJuGUO95ZpbM%3D')])
    """

    # (2) 元の画像とプロンプトを指定して、編集または拡張された画像を作成します。
    # generate_image(image_in="akita_inu.png", image_out="akita_inu_mask.png")

    # image_in = './akita_inu.png'
    # image_mask = './akita_inu_mask.png'
    # prompt = "背景には桜の木があり満開です。"
    # response2 = edit_images(image_in, image_mask, prompt, n=1)
    # pprint.pprint(response2)


if __name__ == "__main__":
    main()

"""
response = {
  "created": 1589478378,
  "data": [
    {
      "url": "https://..."
    },
    {
      "url": "https://..."
    }
  ]
}
"""
# edit images
"""
response = {
  "created": 1589478378,
  "data": [
    {
      "url": "https://..."
    },
    {
      "url": "https://..."
    }
  ]
}

"""

"""
response = {
  "created": 1589478378,
  "data": [
    {
      "url": "https://..."
    },
    {
      "url": "https://..."
    }
  ]
}
"""
# list images
"""
{
  "object": "list",
  "data": [
    {
      "id": "model-id-0",
      "object": "model",
      "created": 1686935002,
      "owned_by": "organization-owner"
    },
    {
      "id": "model-id-1",
      "object": "model",
      "created": 1686935002,
      "owned_by": "organization-owner",
    },
    {
      "id": "model-id-2",
      "object": "model",
      "created": 1686935002,
      "owned_by": "openai"
    },
  ],
  "object": "list"
}
"""
