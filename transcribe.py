import os
import whisper
import torch
import time


def transribe(fileName, input_model):

    print("pass1")

    model = whisper.load_model(input_model)

    print("pass3")


    # Add directory into content folder
    checkDownLoadFolder = os.path.exists("download")
    if not checkDownLoadFolder:
        os.mkdir("download")

    # load audio and pad/trim it to fit 30 seconds
    # 注意⇨完全にaudioをダウンロードしきった状態でないと切れる
    audio = whisper.load_audio(fileName)

    print("pass2")


    outputTextsArr = []
    while audio.size > 0:
        start = time.time()

        tirmedAudio = whisper.pad_or_trim(audio)
        # trimedArray.append(tirmedAudio)
        startIdx = tirmedAudio.size
        audio = audio[startIdx:]

        # make log-Mel spectrogram and move to the same device as the model
        mel = whisper.log_mel_spectrogram(tirmedAudio).to(model.device)

        # detect the spoken language
        _, probs = model.detect_language(mel)
        # print(f"Detected language: {max(probs, key=probs.get)}")

        # decode the audio
        options = whisper.DecodingOptions(fp16 = False)
        result = whisper.decode(model, mel, options)

        # print the recognized text
        outputTextsArr.append(result.text)

        print(time.time() - start)


    outputTexts = ' '.join(outputTextsArr)

    #動画の削除
    os.remove(fileName)

    # Write into a text file
    with open(f"download/{fileName}.txt", "w", encoding="UTF-8") as f:
        f.write(f"▼ Transcription of {fileName}\n")
        f.write(outputTexts)
    
    return "success"