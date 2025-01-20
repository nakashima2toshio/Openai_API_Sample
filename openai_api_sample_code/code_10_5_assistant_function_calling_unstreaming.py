# assistant function calling un-streaming by anthropic
"""
Weather API Base URL: http://api.weatherapi.com/v1
Base URL: http://api.weatherapi.com/v1
 Current weather: http://api.weatherapi.com/v1/current.json
"""
import requests
from openai import OpenAI
import time


def initialize_client():
    return OpenAI()


def create_weather_assistant(client):
    return client.beta.assistants.create(
        instructions="You are a weather bot. Use the provided functions to answer questions about weather for any city.",
        model="gpt-4o",
        tools=[
            {
                "type": "function",
                "function": {
                    "name": "get_weather_data",
                    "description": "Get the current weather data for a specific city",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "city": {
                                "type": "string",
                                "description": "The name of the city"
                            }
                        },
                        "required": ["city"]
                    }
                }
            }
        ]
    )


def create_thread(client):
    return client.beta.threads.create()


def add_message_to_thread(client, thread_id, content):
    return client.beta.threads.messages.create(
        thread_id=thread_id,
        role="user",
        content=content
    )


def create_run_and_poll(client, thread_id, assistant_id):
    run = client.beta.threads.runs.create(
        thread_id=thread_id,
        assistant_id=assistant_id,
    )
    while run.status not in ['completed', 'failed', 'requires_action']:
        time.sleep(1)
        run = client.beta.threads.runs.retrieve(thread_id=thread_id, run_id=run.id)
    return run


def get_coordinates(city):
    url = f"https://nominatim.openstreetmap.org/search?q={city}&format=json&limit=1"
    headers = {
        'User-Agent': 'App/1.0 (nakashima2toshio@gmail.com)'
    }
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        data = response.json()
        if data:
            return float(data[0]['lat']), float(data[0]['lon'])
    return None


def get_weather_data(city):
    coords = get_coordinates(city)
    if coords is None:
        return f"Could not find coordinates for {city}"

    latitude, longitude = coords
    url = f"https://api.met.no/weatherapi/locationforecast/2.0/compact?lat={latitude}&lon={longitude}"
    headers = {
        'User-Agent': 'App/1.0 (nakashima2toshio@gmail.com)'
    }
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        data = response.json()
        current_data = data['properties']['timeseries'][0]['data']['instant']['details']
        temperature = current_data['air_temperature']
        weather_symbol = data['properties']['timeseries'][0]['data']['next_1_hours']['summary']['symbol_code']
        return f"Weather in {city}: Temperature: {temperature}°C, Condition: {weather_symbol}"
    else:
        return f"Failed to fetch weather data for {city}"


def handle_tool_calls(run):
    tool_outputs = []
    for tool in run.required_action.submit_tool_outputs.tool_calls:
        if tool.function.name == "get_weather_data":
            args = eval(tool.function.arguments)
            weather_data = get_weather_data(args['city'])
            tool_outputs.append({
                "tool_call_id": tool.id,
                "output": weather_data
            })
    return tool_outputs


def submit_tool_outputs_and_poll(client, thread_id, run_id, tool_outputs):
    run = client.beta.threads.runs.submit_tool_outputs_and_poll(
        thread_id=thread_id,
        run_id=run_id,
        tool_outputs=tool_outputs
    )
    return run


def display_messages(client, thread_id):
    messages = client.beta.threads.messages.list(thread_id=thread_id)
    for msg in messages:
        print(f"{msg.role}: {msg.content[0].text.value}")


def main():
    """
    [INPUT]:
    - ユーザーが指定する都市の名前（例: "San Francisco"）を含む質問。
    [Process]:
    1. OpenAIクライアントの初期化。
    2. 天気アシスタントの作成。
    3. スレッドの作成。
    4. ユーザーの質問をスレッドに追加。
    5. アシスタントが実行するランの作成とポーリング。
    6. ランがアクションを要求する場合、必要なツールを呼び出し、結果を送信。
    7. ランが完了した場合、アシスタントのレスポンスを表示。
    [OUTPUT]:
    - アシスタントが生成した応答（例: 指定された都市の現在の天気と気温）
    """
    client = initialize_client()
    assistant = create_weather_assistant(client)
    thread = create_thread(client)

    while True:
        user_message = input("Ask about the weather (or type 'quit' to exit): ")
        if user_message.lower() == 'quit':
            break

        add_message_to_thread(client, thread.id, user_message)
        run = create_run_and_poll(client, thread.id, assistant.id)

        if run.status == 'requires_action':
            tool_outputs = handle_tool_calls(run)
            run = submit_tool_outputs_and_poll(client, thread.id, run.id, tool_outputs)

        if run.status == 'completed':
            print("Assistant's response:")
            display_messages(client, thread.id)
        else:
            print(f"Run failed with status: {run.status}")


if __name__ == "__main__":
    main()
