from flask import Flask, request, render_template
import os
from yt_dlp import YoutubeDL
import whisper
import torch
import transcribe
import translate
import glob


app = Flask(__name__)

# Add directory into content folder
checkDownLoadFolder = os.path.exists("download")
if not checkDownLoadFolder:
  os.mkdir("download")


@app.route('/', methods=['GET', 'POST'])
def hello():

    if request.method == 'POST':

        url = request.form.get("url")

        #Youtube動画DL
        cmd = "yt-dlp " + "-x --audio-format mp3 " + url
        res = os.system(cmd)

        if res != "0":
            print("error")

        #音声のファイル名を習得
        file_list = glob.glob(
        "*.mp3"
        )  

        while len(file_list) == 0:
            #mp3ファイルを取得
            file_list = glob.glob(
            "*.mp3"
            )  

        # スクリプトを置いたフォルダ内に保存された音声ファイル名取得
        name_list = [os.path.basename(file) for file in file_list]
        audio_name = name_list[0]

        print('audio_name')
        print(audio_name)

        # whisperにかける
        transcribe.transribe(audio_name)

        #動画の削除
        os.remove(audio_name)

        #書き起こしたtextのpathを習得
        text_path = f"download/{audio_name}.txt"

        #DeepLで翻訳した文章の習得
        translated_txt = translate.translation(text_path)

        #transcibeしたテキストの削除
        os.remove(text_path)

        return render_template('translated.html', translated_txt=translated_txt)
    else:
        return render_template('index.html')

if __name__ == '__main__':
    app.run()