# assistant code interpriter
from openai import OpenAI
import time

model_4o_mini = "gpt-4-mini"

def initialize_client():
    return OpenAI()

def create_assistant(client, tools_type, tools_name, tools_instructions):
    return client.beta.assistants.create(
        name=tools_name,
        instructions=tools_instructions,
        tools=[{"type": tools_type}],
        model=model_4o_mini
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

def main():
    tools_type = "code_interpreter"
    tools_name = "Math Tutor"
    tools_instructions = "You are a personal math tutor. Write and run code to answer math questions."

    client = initialize_client()
    assistant = create_assistant(client, tools_type, tools_name, tools_instructions)
    thread = create_thread(client)

    user_message = "I need to solve the equation `3x + 11 = 14`. Can you help me?"
    add_message_to_thread(client, thread.id, user_message)

    run = create_run_and_wait(client, thread.id, assistant.id)

    if run.status == 'completed':
        print("Assistant's response:")
        display_messages(client, thread.id)
    else:
        print(f"Run failed with status: {run.status}")

    print("\nRun Steps:")
    display_run_steps(client, thread.id, run.id)

if __name__ == "__main__":
    main()