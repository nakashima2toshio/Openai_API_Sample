# embeddings from document and cook book
from openai import OpenAI
import pandas as pd
import tiktoken
import pprint

model_embedding_3_small = "text-embedding-3-small"
client = OpenAI()


def create_embeddings2(input_text, model_name, encoding_format="float"):
    # 入力テキストを表す埋め込みベクトルを作成します。
    # (ex.) input="The food was delicious and the waiter..."
    response = client.embeddings.create(
        model=model_name,
        input=input_text,
        encoding_format="float"
    )
    return response

def create_embeddings(input_text, model_name):
    response = client.embeddings.create(
        input="Your text string goes here",
        model="text-embedding-3-small"
    )

    return response.data[0].embedding

"""
データセットから埋め込みを取得する:
https://cookbook.openai.com/examples/get_embeddings_from_dataset
"""
def get_embedding(text, model=model_embedding_3_small):
   text = text.replace("\n", " ")
   return client.embeddings.create(input = [text], model=model).data[0].embedding

def main():
    input_text = "The food was delicious and the waiter..."
    model_name = model_embedding_3_small
    res = create_embeddings(input_text, model_name)
    pprint.pprint(res)

    data = {
        "combined": ["Sample text 1", "Sample text 2"]  # 実際のデータに置き換える
    }

    df = pd.DataFrame(data)
    df['ada_embedding'] = df['combined'].apply(lambda x: get_embedding(x, model=model_embedding_3_small))
    df.to_csv('./data/embedded_1k_reviews.csv', index=False)


if __name__ == "__main__":
    main()
