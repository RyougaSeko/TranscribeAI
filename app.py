from flask import Flask, request, render_template
import os
from yt_dlp import YoutubeDL
import whisper
import torch
import transcribe
import translate
import glob
from youtubesearchpython import *
import time
import subprocess
from mutagen.mp3 import MP3

app = Flask(__name__)

# Add directory into content folder
checkDownLoadFolder = os.path.exists("download")
if not checkDownLoadFolder:
  os.mkdir("download")


@app.route('/', methods=['GET', 'POST'])
def index():

    if request.method == 'POST':

        url = request.form.get("url")

        movie_id = url.split("watch?v=")[1].split("&ab_channel=")[0]

        #Youtube動画DL
        cmd = "yt-dlp " + "-x --audio-format mp3 " + url
        res = os.system(cmd)

        #mp3ファイルが完全にDLされるまで待機する処理を書きたい。
        while res != 0:
            print(res)
            pass

        #音声のファイル名を習得
        file_list = glob.glob(
            "*" + movie_id + "*.mp3"
        )

        while len(file_list) == 0:
            #mp3ファイルを取得
            file_list = glob.glob(
                "*" + movie_id + "*.mp3"
        )

        # スクリプトを置いたフォルダ内に保存された音声ファイル名取得
        name_list = [os.path.basename(file) for file in file_list]
        audio_name = name_list[0]

        print('audio_name')
        print(audio_name)


        while os.path.exists(audio_name) != True:
            print(f"os.path.exists(audio_name)={os.path.exists(audio_name)}")
            time.sleep(1)
            pass

        time.sleep(5)

        # whisperにかける
        transcribe.transribe(str(audio_name))

        #動画の削除
        os.remove(audio_name)

        #書き起こしたtextのpathを習得
        text_path = f"download/{audio_name}.txt"

        #書き起こした英語の取得
        f = open(text_path, 'r')
        transcripted_txt = f.read()
        f.close()

        #DeepLで翻訳した文章の習得
        translated_txt = translate.translation(text_path)

        #transcibeしたテキストの削除
        os.remove(text_path)

        return render_template('index.html', transcripted_txt = transcripted_txt, translated_txt=translated_txt)
    else:
        return render_template('index.html')

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        

        return render_template('signup.html')
    else:
        return render_template('signup.html')

if __name__ == '__main__':
    app.run()