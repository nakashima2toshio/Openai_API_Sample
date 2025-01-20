# assistant: code interpreter streaming and un-streaming both
from openai import OpenAI
from typing_extensions import override
from openai import AssistantEventHandler
import time


def initialize_client():
    return OpenAI()


def create_assistant(client):
    return client.beta.assistants.create(
        name="Math Tutor",
        instructions="You are a personal math tutor. Write and run code to answer math questions.",
        tools=[{"type": "code_interpreter"}],
        model="gpt-4"
    )


def create_thread(client):
    return client.beta.threads.create()


def add_message_to_thread(client, thread_id, content):
    return client.beta.threads.messages.create(
        thread_id=thread_id,
        role="user",
        content=content
    )


def create_run_and_wait(client, thread_id, assistant_id):
    run = client.beta.threads.runs.create(
        thread_id=thread_id,
        assistant_id=assistant_id,
        instructions="Please address the user as Jane Doe. The user has a premium account."
    )
    while run.status not in ['completed', 'failed', 'requires_action']:
        time.sleep(1)
        run = client.beta.threads.runs.retrieve(thread_id=thread_id, run_id=run.id)
    return run


def display_messages(client, thread_id):
    messages = client.beta.threads.messages.list(thread_id=thread_id)
    for msg in messages:
        print(f"{msg.role}: {msg.content[0].text.value}")


def display_run_steps(client, thread_id, run_id):
    run_steps = client.beta.threads.runs.steps.list(thread_id=thread_id, run_id=run_id)
    for step in run_steps:
        print(f"Step {step.id}: {step.type}")
        if step.type == 'tool_calls':
            for tool_call in step.step_details.tool_calls:
                print(f"  Tool: {tool_call.type}")
                if tool_call.type == 'code_interpreter':
                    print(f"    Input: {tool_call.code_interpreter.input}")
                    print(f"    Output: {tool_call.code_interpreter.outputs[0].content}")


class EventHandler(AssistantEventHandler):
    @override
    def on_text_created(self, text) -> None:
        print(f"\nassistant > ", end="", flush=True)

    @override
    def on_text_delta(self, delta, snapshot):
        print(delta.value, end="", flush=True)

    def on_tool_call_created(self, tool_call):
        print(f"\nassistant > {tool_call.type}\n", flush=True)

    def on_tool_call_delta(self, delta, snapshot):
        if delta.type == 'code_interpreter':
            if delta.code_interpreter.input:
                print(delta.code_interpreter.input, end="", flush=True)
            if delta.code_interpreter.outputs:
                print(f"\n\noutput >", flush=True)
                for output in delta.code_interpreter.outputs:
                    if output.type == "logs":
                        print(f"\n{output.logs}", flush=True)


def stream_run(client, thread_id, assistant_id):
    with client.beta.threads.runs.stream(
            thread_id=thread_id,
            assistant_id=assistant_id,
            instructions="Please address the user as Jane Doe. The user has a premium account.",
            event_handler=EventHandler(),
    ) as stream:
        stream.until_done()


def main(use_streaming=False):
    client = initialize_client()
    assistant = create_assistant(client)
    thread = create_thread(client)

    user_message = "I need to solve the equation `3x + 11 = 14`. Can you help me?"
    add_message_to_thread(client, thread.id, user_message)

    if use_streaming:
        print("Using streaming version:")
        stream_run(client, thread.id, assistant.id)
    else:
        print("Using non-streaming version:")
        run = create_run_and_wait(client, thread.id, assistant.id)

        if run.status == 'completed':
            print("Assistant's response:")
            display_messages(client, thread.id)
        else:
            print(f"Run failed with status: {run.status}")

        print("\nRun Steps:")
        display_run_steps(client, thread.id, run.id)


if __name__ == "__main__":
    # Set use_streaming to True to use the streaming version
    main(use_streaming=False)