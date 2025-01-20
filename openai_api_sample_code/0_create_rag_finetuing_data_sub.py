# based on Text-files
import glob
from openai import OpenAI
import json
import pprint

model_4o_mini = "gpt-4o-mini"
model_chatgpt = "gpt-4o"


class CreateRagFineTuningData:
    """


    """
    def __init__(self):
        self.jsonl_data = []

    def list_txt_files(self):
        return sorted(glob.glob('./*.txt'))

    def generate_prompt_completion(self, content):
        prompt = (
            "From the following document, create about 5 QAs as data for chatgpt's fine-tuning. "
            "Each QA should be in the format: "
            "{'prompt': '<question>', 'completion': '<answer>'}"
        )
        prompt = prompt + "\n\nDocument:\n" + content
        client = OpenAI()
        response = client.chat.completions.create(
            model=model_chatgpt,  # Updated to a more recent model
            messages=[
                {"role": "system", "content": "You are a professional python developer, a helpful assistant and good "
                                              "at chatgpt APIs."},
                {"role": "user", "content": prompt},
            ],
            max_tokens=1000,  # Increased token limit
            n=1,
            stop=None,
            temperature=0.5
        )
        return response.choices[0].message.content

    def process_files(self):
        file_lists = self.list_txt_files()

        for file_path in file_lists:
            with open(file_path, 'r') as file:
                content = file.read()
            qa_data = self.generate_prompt_completion(content)
            try:
                qa_list = json.loads(f"[{qa_data.replace('}{', '},{')}]")
                self.jsonl_data.extend(qa_list)
            except json.JSONDecodeError:
                print(f"Error parsing JSON from file: {file_path}")
                print(f"Generated content: {qa_data}")

    def save_to_jsonl(self):
        with open('fine_tuning_data.jsonl', 'w') as f:
            for item in self.jsonl_data:
                f.write(json.dumps(item) + '\n')

    def main(self):
        self.process_files()
        self.save_to_jsonl()
        print(f"Generated {len(self.jsonl_data)} QA pairs.")
        print("Sample of generated data:")
        pprint.pprint(self.jsonl_data[:5])  # Print first 5 QA pairs


if __name__ == "__main__":
    instance = CreateRagFineTuningData()
    instance.main()
