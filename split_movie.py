from pydub import AudioSegment

def split_movie(audio_name, endtime_ms):

        sound = AudioSegment.from_file(audio_name, format="mp3")
        splitted_sound = sound[:endtime_ms]

        copy_audio_name = audio_name

        audio_name = "Splitted_"+str(audio_name)

        splitted_sound.export(audio_name, format="mp3")

        return copy_audio_name, audio_name

        
