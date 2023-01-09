# HummingTranslate

立ち上げ方

1.EC2のインスタンスをubuntu22.04で作成。（セキュリティグループの80番を開けておく。）

2.ローカルからssl認証してEC2に入る。

3.このbranchをclone
git clone -b [ブランチ名] [URL] 

4.nginx（1.18.0：推奨）のインストール
sudo apt update && apt install nginx

５.ffmpegのインストール
sudo apt install ffmpeg

6.pipのインストール
pip3 install --upgrade pip

7.whisperのインストール
pip3 install --upgrade --no-deps --force-reinstall git+https://github.com/openai/whisper.git

8.torchのインストール
pip3 install --no-cache-dir torch==1.13.1

9.その他のライブラリのインストール
pip3 install -r requirements.txt

10.nginxの立ち上げ
sudo nginx -c /home/ubuntu/TranscribeAI/config/nginx.conf

11.gunicornのバックグラウンドでの立ち上げ
gunicorn app:app -c config/gunicorn_settings.py -D

12.環境変数の設定
.envに環境変数
DeepL_API_KEY = ""を設定


うまく行かないとき
1.パスが通っているか確認
2.gunicornからログの確認


