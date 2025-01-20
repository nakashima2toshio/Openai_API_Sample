# ファイルに含まれるtoke数を返す。
# model: text-embedding-3-small
import tiktoken
import pprint

def tokens_for_string(data_l: str, encoding_name: str) -> int:
    """Returns the number of tokens in a text string."""
    encoding = tiktoken.get_encoding(encoding_name)
    num_tokens = len(encoding.encode(data_l))
    return num_tokens

def main():
    file_path1 = './data/python_code_dict.json'
    with open(file_path1, 'r') as fp:
        data_l1 = fp.read()
    num1 = tokens_for_string(data_l1, "cl100k_base")
    print(f"{file_path1} ---> のtoken数は：{num1}")

    file_path2 = './data/paragraph_dict.json'
    with open(file_path2, 'r') as fp:
        data_l2 = fp.read()
    num2 = tokens_for_string(data_l2, "cl100k_base")
    print(f"{file_path2} ---> のtoken数は：{num2}")

if __name__ == '__main__':
    main()
