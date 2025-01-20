# 節度を作る
# modelations create_moderation
from openai import OpenAI

client = OpenAI()

model_retrieve_4o_mini = "gpt-4o-mini"
model_retrieve_35_turbo_instruct = "gpt-3.5-turbo-instruct"


def create_modelations():
    # テキストが潜在的に有害かどうかを分類します。
    moderation = client.moderations.create(input="I want to kill them.")
    return moderation