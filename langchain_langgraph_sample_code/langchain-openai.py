# pip install langchain-openai
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI

# テンプレート文章を定義し、プロンプトを作成
prompt = ChatPromptTemplate.from_messages([
    ("system", "あなたは優秀な校正者です。"),
    ("user", "次の文章に誤字があれば訂正してください。\n{sentences_before_check}")
])

# OpenAIのモデルのインスタンスを作成
llm = ChatOpenAI(model_name="gpt-4o", temperature=0)

