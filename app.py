from flask import Flask, request, render_template
import os
from yt_dlp import YoutubeDL
import whisper
import torch
import transcribe
import translate
import glob
import time
import subprocess
from mutagen.mp3 import MP3
from pydub import AudioSegment


app = Flask(__name__)

# Add directory into content folder
checkDownLoadFolder = os.path.exists("download")
if not checkDownLoadFolder:
  os.mkdir("download")


@app.route('/', methods=['GET', 'POST'])
def index():

    if request.method == 'POST':

        url = request.form.get("url")

        #Youtube動画DL
        cmd = "yt-dlp " + "-x --audio-format mp3 " + url
        res = os.system(cmd)

        if res != 0:
            return render_template('index.html', error_msg="erro1 無効なURLです")

        #音声のファイル名を習得
        try:
            movie_id = url.split("watch?v=")[1].split("&ab_channel=")[0]
        except:
            try:
                movie_id = url.split("https://youtu.be/")[1]
            except:
                return render_template('index.html', error_msg="erro3 無効なURLです")

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

        if len(name_list) == 0:
            return render_template('index.html', error_msg="error4 無効なURLです")
        
        #音声ファイル名が取得できるまでループ
        while os.path.exists(audio_name) != True:
            print(f"os.path.exists(audio_name)={os.path.exists(audio_name)}")
            time.sleep(1)
            pass

        time.sleep(1)

        #30分以上の動画は最初の30分だけ切り取る
        audio = MP3(audio_name)
        copy_audio_name=""

        if audio.info.length > 1800:
            sound = AudioSegment.from_file(audio_name, format="mp3")
            splitted_sound = sound[:1800000]
            
            #30分以上のmp3を削除
            copy_audio_name = audio_name

            audio_name = "Splitted_"+str(audio_name)

            #splitした後のmp3を出力
            splitted_sound.export(audio_name, format="mp3")

        #MP3への変換をtranscribeの処理が追い越さないようにsleepさせる。
        file_list = glob.glob(
            "*" + movie_id + "*.webm"
        )

        # webmが削除されたら、次へ行く
        while len(file_list) != 0:

            file_list = glob.glob(
            "*" + movie_id + "*.webm"
            )

            time.sleep(1)

        # whisperにかける
        transcribe.transribe(audio_name)

        # 30分以上の動画の削除
        if copy_audio_name != "":
            os.remove(copy_audio_name)

        #書き起こしたtextのpathを習得
        text_path = f"download/{audio_name}.txt"

        #書き起こした英語の取得
        f = open(text_path, 'r', encoding="UTF-8")
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

@app.route('/top', methods=['GET', 'POST'])
def top():
    if request.method == 'POST':

        mail_adress = request.form.get("email")

        print(mail_adress)

        with open('data/mail.txt', 'a') as f:
            f.write(f"{str(mail_adress)}\n")

        return render_template('success.html')
    else:
        return render_template('top.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        

        return render_template('login.html')
    else:
        return render_template('login.html')
