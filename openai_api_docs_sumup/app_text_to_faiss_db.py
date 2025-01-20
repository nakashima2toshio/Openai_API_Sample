#
import re
import openai
import numpy as np
import pandas as pd
from sklearn.preprocessing import normalize
import faiss

# OpenAI APIキーを設定
openai.api_key = 'your-api-key'

# ファイルを読み込む
with open('./text_generation.txt', 'r') as file:
    content = file.read()

# 段落ごとに分割
paragraphs = re.split(r'\n\s*\n', content)

# コードスニペットを抽出する正規表現
code_pattern = re.compile(r'```python(.*?)```', re.DOTALL)

# extract & translate to code to prompt: xxxx, completions: yyyy
paragraphs = [code_pattern.findall(paragraph) for paragraph in paragraphs]

# 段落とコードスニペットをリストに格納
chunks = []
for paragraph in paragraphs:
    code_matches = code_pattern.findall(paragraph)
    if code_matches:
        for code in code_matches:
            chunks.append(code.strip())
    else:
        chunks.append(paragraph.strip())

# 各チャンクをベクトル化する関数
def get_embedding(text):
    response = openai.Embedding.create(
        input=text,
        model="text-embedding-3-small"
    )
    return response['data'][0]['embedding']

# 各チャンクをベクトル化
chunk_embeddings = []
for chunk in chunks:
    embedding = get_embedding(chunk)
    chunk_embeddings.append(embedding)

# ベクトルデータをデータフレームに変換
df = pd.DataFrame(chunk_embeddings)
df['chunk'] = chunks

# ベクトルデータの正規化
normalized_embeddings = normalize(df.drop(columns=['chunk']), axis=1)
df_normalized = pd.DataFrame(normalized_embeddings)
df_normalized['chunk'] = df['chunk']

# Faissインデックスを作成
d = df_normalized.shape[1] - 1  # ベクトルの次元数
index = faiss.IndexFlatL2(d)

# ベクトルをFaissインデックスに追加
index.add(np.array(df_normalized.drop(columns=['chunk'])))

# Faissインデックスを保存
faiss.write_index(index, 'chunk_embeddings.index')

# 結果を確認
print(df_normalized.head())

# 検索機能の実装例
def search_chunk(query, k=5):
    query_embedding = get_embedding(query)
    query_embedding = normalize([query_embedding], axis=1)
    D, I = index.search(np.array(query_embedding).astype(np.float32), k)
    return df_normalized.iloc[I[0]]['chunk'].tolist()

# サンプル検索
query = "テキスト生成モデルの概要"
results = search_chunk(query)
print("検索結果:")
for result in results:
    print(result)
