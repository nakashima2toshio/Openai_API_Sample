# OPENAI API Sample
from openai import OpenAI
from openai_api_sample_code.code_1_0_chat_completions import create_chat_completions

client = OpenAI()

model_text_to_speech = "tts-1"
model_audio_transcription = "whisper-1"


def create_audio_speech(input_text, speech_file_path):
    # (1) 入力テキストからオーディオを生成します。
    response = client.audio.speech.create(
        model=model_text_to_speech,
        voice="nova",
        input=input_text  # "The quick brown fox jumped over the lazy dog."
    )
    # response.stream_to_file(speech_file_path)

    with open(speech_file_path, "wb") as f:
        f.write(response.content)


def create_audio_transcriptions(speech_mp3, speech_file_path):
    # (2) デフォルト: 音声を入力言語に書き起こします。
    audio_file = open(speech_mp3, "rb")
    transcript = client.audio.transcriptions.create(
        model=model_audio_transcription,
        file=audio_file
    )
    return transcript


def create_audio_transcription_word_timestamps(speech_mp3):
    # (3) 単語のタイムスタンプ: 音声を入力言語に書き起こします。
    # タイムスタンプの粒度を使用するには、response_format or verbose_jsonを設定する必要があります
    audio_file = open(speech_mp3, "rb")
    transcript = client.audio.transcriptions.create(
        file=audio_file,
        model=model_audio_transcription,
        response_format="verbose_json",
        timestamp_granularities=["word"]
    )
    return transcript


def create_audio_transcriptions_segment_timestamps(speech_mp3):
    # (4) セグメント・タイムスタンプ
    # タイムスタンプの粒度を使用するには、response_format or verbose_jsonを設定する必要があります
    audio_file = open(speech_mp3, "rb")
    transcript = client.audio.transcriptions.create(
        file=audio_file,
        model=model_audio_transcription,
        response_format="verbose_json",
        timestamp_granularities=["segment"]
    )
    return transcript


def create_audio_transcription(speech_file_mp3):
    # (5) 音声を英語に翻訳します。
    audio_file = open(speech_file_mp3, "rb")
    transcript = client.audio.translations.create(
        model=model_audio_transcription,
        file=audio_file
    )
    return transcript

def main_1():
    # (1) 入力テキストからオーディオを生成します。
    input_text = "Hello, my name is Wolfgang and I come from Germany. Where are you heading today?"
    speech_file_path = './speech_file.mp3'
    create_audio_speech(input_text, speech_file_path)

    input_text_j = "こんにちは、私は太郎です。物理学を勉強しています。"
    speech_file_path_j = './speech_file_j.mp3'
    create_audio_speech(input_text_j, speech_file_path_j)

    import subprocess
    subprocess.run(["afplay", speech_file_path_j])

def main_2():
    # (2) def create_chat_completions(system_content, user_content)
    system_content = "あなたは有能な翻訳者のアシスタントです。"
    user_content = "プロのソフトウェア開発者向けに、OpenAiのAPIの概要を説明しなさい。"
    chat_messages = create_chat_completions(system_content, user_content)
    print(chat_messages.content)

def main_3():
    speech_mp3 = "./speech_file.mp3"
    transcript = create_audio_transcriptions_segment_timestamps(speech_mp3)
    print(transcript.text)

    # MP3 を再生する
    import subprocess
    subprocess.run(["afplay", speech_mp3])

def main_4():
    speech_mp3 = "./speech_file.mp3"
    trans = create_audio_transcriptions_segment_timestamps(speech_mp3)
    print(trans.text)

def main_5():
    speech_mp3_j = "./speech_file_j.mp3"
    trans_e = create_audio_transcription(speech_mp3_j)
    print(trans_e.text)

if __name__ == '__main__':
    main_1()
    # main_2()
    # main_3()
    # main_4()
    # main_5()


