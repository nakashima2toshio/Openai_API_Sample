# data to Faiss-db: 作成データをFaiss-DBに入れローカルで管理・利用できるようにする。
import re
from openai import OpenAI
import numpy as np
import pandas as pd
from sklearn.preprocessing import normalize
import faiss
import os

# model_vector = "text-embedding-ada-002"
model_embedding_3_small = "text-embedding-3-small"
client = OpenAI()

data_file_txt = '../openai_api_docs_sumup/doc_01_0_chat_completions.txt'


def split_into_paragraphs(file_path):
    print('1-splitting file into paragraphs --------')
    # ファイルを読み込み、段落とPythonコードブロックに分割する
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            content = file.read()

        python_blocks = re.findall(r'```python.*?```', content, re.DOTALL)
        non_python_parts = re.split(r'```python.*?```', content, flags=re.DOTALL)

        paragraphs = []
        for part in non_python_parts:
            paragraphs.extend([p.strip() for p in part.split('\n\n') if p.strip()])

        return paragraphs, python_blocks
    except FileNotFoundError:
        print(f"Error: File not found at {file_path}")
        return [], []
    except Exception as e:
        print(f"Error reading file: {e}")
        return [], []


def get_embeddings(texts):
    # テキストのリストを受け取り、OpenAI APIを使用してそれぞれのベクトル表現を取得する
    print('2-get_embeddings -------')
    print(texts)  #  = text.replace("\n", " ")
    emb_list = []
    try:
        for text in texts:
            response = client.embeddings.create(
                input=text,
                model=model_embedding_3_small
            )
            emb_list.append(response.data[0].embedding)
        return emb_list
    except Exception as e:
        # client.error.OpenAIError) as e:
        print(f"OpenAI API error: {e}")
        return []


def create_faiss_index(embeddings):
    print('3-create_faiss_index ---------------')
    # 与えられたベクトル表現を使用してFaissインデックスを作成する
    d = len(embeddings[0])  # ベクトルの次元数
    index = faiss.IndexFlatL2(d)
    index.add(np.array(embeddings).astype(np.float32))
    return index


def search_chunk(query, index, df_normalized, k=5):
    print('4-search_chunk ---------------')
    # クエリを受け取り、Faissインデックスを使用して最も類似したk個のチャンクを検索する
    query_embeddings = get_embeddings([query])
    if not query_embeddings:
        print("Failed to generate query embedding.")
        return []

    query_embedding = query_embeddings[0]
    query_embedding = normalize([query_embedding], axis=1)
    D, I = index.search(np.array(query_embedding).astype(np.float32), k)
    return df_normalized.iloc[I[0]]['chunk'].tolist()


def process_data():
    print('5-process_data ---------------')
    # テキストデータを読み込み、ベクトル化し、正規化してFaissインデックスを作成する
    paragraphs, python_blocks = split_into_paragraphs(data_file_txt)
    chunks = paragraphs + python_blocks
    if not chunks:
        print("No data to process. Exiting.")
        return None, None

    chunk_embeddings = get_embeddings(chunks)
    if not chunk_embeddings:
        print("Failed to generate embeddings. Exiting.")
        return None, None

    df = pd.DataFrame(chunk_embeddings)
    df['chunk'] = chunks

    normalized_embeddings = normalize(df.drop(columns=['chunk']), axis=1)
    df_normalized = pd.DataFrame(normalized_embeddings)
    df_normalized['chunk'] = df['chunk']

    index = create_faiss_index(normalized_embeddings)

    return index, df_normalized


def save_data(index, df_normalized):
    print('6-save_data ---------------')
    # FaissインデックスとデータフレームをファイルとしてLOCALに保存する
    index_file = 'chunk_embeddings.index'
    faiss.write_index(index, index_file)
    print(f"Faiss index saved to {index_file}")

    csv_file = 'chunk_data.csv'
    df_normalized.to_csv(csv_file, index=False)
    print(f"Chunk data saved to {csv_file}")


def main():
    # メイン処理：データの処理、保存、およびサンプル検索を実行する
    index, df_normalized = process_data()
    if index is not None and df_normalized is not None:
        save_data(index, df_normalized)
        print("Process completed successfully.")

        # サンプル検索
        # query = "テキスト生成モデルの概要とコード例を記述しなさい。"
        query = "Provide an overview of the text generation model and code examples."
        print('question is : ', query)
        results = search_chunk(query, index, df_normalized)
        print("検索結果:")
        for result in results:
            print(result)

def main2():
    query = "Provide an overview of the text generation model and code examples."

    # results = search_chunk(query, index, df_normalized)
    # print("検索結果:")
    # for result in results:
    #     print(result)


if __name__ == '__main__':
    main()

