# code_10_11_structured_chain_of_thought
from pydantic import BaseModel
from openai import OpenAI
import pprint

client = OpenAI()

class Step(BaseModel):
    explanation: str
    output: str

class MathReasoning(BaseModel):
    steps: list[Step]
    final_answer: str

def chain_of_thought():
    completion = client.beta.chat.completions.parse(
        model="gpt-4o-2024-08-06",
        messages=[
            {"role": "system", "content": "You are a helpful math tutor. Guide the user through the solution step by step."},
            {"role": "user", "content": "how can I solve 8x + 7 = -23"}
        ],
        response_format=MathReasoning,
    )

    math_reasoning = completion.choices[0].message.parsed
    return math_reasoning

def main():
    response = chain_of_thought()
    pprint.pprint(response.steps)

if __name__ == "__main__":
    main()
