from openai import OpenAI
import pprint

client = OpenAI()

model_text_to_speech = "tts-1"
model_audio_transcription = "whisper-1"

"""　## 音声テキスト変換
・音声をその言語に書き起こします。
・音声を英語に翻訳して書き起こします。
"""
def create_audio_transcriptions(input_file_path):
    # (1) 文字起こしAPI：Transcribes audio into the input language.
    audio_file = open(input_file_path, "rb")
    transcription = client.audio.transcriptions.create(
        model=model_audio_transcription,
        file=audio_file,
        response_format="text",  # デフォルトのoutputはjson形式。
        # prompt=prompt  # "ZyntriQix, Digique Plus, CynapseFive, VortiQore V8, EchoNix Array, OrbitalLink Seven, DigiFractal Matrix, PULSE, RAPT, B.R.I.C.K., Q.U.A.R.T.Z., F.L.I.N.T."
    )
    return transcription

def create_audio_translations(input_mp3):
    # (2) 入力音声を翻訳：今は、英語へ
    audio_file = open(input_mp3, "rb")
    transcript = client.audio.translations.create(
      model=model_audio_transcription,
      file=audio_file
    )
    return transcript

def main_1():
    # (1) 文字起こし: text_to_speech
    input_file_path = './speech_file.mp3'
    txt =create_audio_transcriptions(input_file_path)
    print(txt)

def main_2():
    # (2) 音声データを翻訳
    input_file_path = './speech_file.mp3'
    txt =create_audio_translations(input_file_path)
    print('英語：',txt)


if __name__ == '__main__':
    # main_1()
    main_2()
