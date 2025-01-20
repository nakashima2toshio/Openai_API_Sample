# json mode
from openai import OpenAI

model_4o_mini = "gpt-4o-mini"
client = OpenAI()


def create_chat_completion_json_mode(messages):
    # json形式で結果を返す。
    response = client.chat.completions.create(
        model=model_4o_mini,
        response_format={"type": "json_object"},
        messages=messages
    )
    return response.choices[0].message.content


def main():
    messages = [
        {"role": "system", "content": "You are a helpful assistant designed to output JSON."},
        {"role": "user", "content": "Who won the world series in 2020?"}
    ]
    res = create_chat_completion_json_mode(messages)
    print(res)


if __name__ == "__main__":
    main()
