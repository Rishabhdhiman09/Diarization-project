from django.shortcuts import render
from django.http import HttpResponse
from django.conf import settings
from django.core.files.storage import FileSystemStorage
import matplotlib.pyplot as plt
import os
import glob
import pyAudioAnalysis as paa
from pyAudioAnalysis import audioSegmentation
from itertools import groupby
from pydub import AudioSegment
from pydub.silence import split_on_silence
import soundfile as sf
from . import summarizer, speechTextAzure
import math
import datetime
com_text = []
full_text = []
def home(request):
    return render(request, 'home.html', {'name': 'Rishabh'})
def transcript(request):
    full_text.clear()
    pwd = os.getcwd()
    file_format = str(request.POST["file_format"])
    meeting_title = str(request.POST["meeting_title"])
    num_speakers = int(request.POST["num_speakers"])
    meeting_start_time = str(request.POST["meeting_start_time"])
    min_sil_time = int(request.POST["min_sil_len"])
    myfile = request.FILES['multimedia']
    fs = FileSystemStorage()
    filename = fs.save(myfile.name, myfile)
    if file_format == "mp3":
        src = os.path.join(pwd, filename)
        dst = os.path.join(pwd, filename.split(".")[0]) + ".wav"
        sound = AudioSegment.from_mp3(src)
        sound.export(dst, format="wav")
        filename = os.path.join(pwd, filename.split(".")[0]) + ".wav"
    else:
        pass
    uploaded_file_url = fs.url(filename)
    result = audioSegmentation.speaker_diarization(filename = os.path.join(pwd, filename), plot_res = False, n_speakers = 2, mid_window=2.0, mid_step=0.2, 
                             short_window=0.05, lda_dim=35)
    sep_list = [list(j) for i, j in groupby(result)]


    time_list = []
    for list_ in sep_list:
        values = list_[:int(len(list_)/5)]
        for e in values:
            time_list.append(int(e))

    
    # Start hour, minute of meeting
    start_hour = int(meeting_start_time.split(":")[0])
    start_min = int(meeting_start_time.split(":")[1])
    def get_large_audio_transcription(path):
        # open the audio file using pydub
        sound = AudioSegment.from_wav(path)  
        # split audio sound where silence is 700 miliseconds or more and get chunks
        chunks = split_on_silence(sound,
            # experiment with this value for your target audio file
            min_silence_len = min_sil_time,
            # adjust this per requirement
            silence_thresh = sound.dBFS-14,
            # keep the silence for 1 second, adjustable as well
            keep_silence=500,
        )
        folder_name = "audio-chunks"
        # create a directory to store the audio chunks
        if not os.path.isdir(folder_name):
            os.mkdir(folder_name)
        whole_text = ""
        # process each chunk 
        total_speech_len = 0
        for i, audio_chunk in enumerate(chunks, start=1):
            # export audio chunk and save it in
            # the `folder_name` directory.
            chunk_filename = os.path.join(folder_name, f"chunk{i}.wav")
            audio_chunk.export(chunk_filename, format="wav")
            
            f = sf.SoundFile(chunk_filename)
            
            chunk_len = (len(f) / f.samplerate)
            try:
                current_speaker = time_list[int(total_speech_len + chunk_len/2)]
            except:
                current_speaker = time_list[-1]
            
            total_speech_len += chunk_len
            # time calculations
            start = datetime.datetime(100,10,10,start_hour, start_min, 0)
            end = start + datetime.timedelta(0, int(total_speech_len))
            # recognize the chunk
            # with sr.AudioFile(chunk_filename) as source:
            #     audio_listened = r.record(source)
            #     # try converting it to text
            #     try:
            #         text = r.recognize_google(audio_listened)
            #         full_text.append(text)
            #         text = f"Speaker{current_speaker}: {[str(end.time())]} " + text
            #         print(text)
            #     except sr.UnknownValueError as e:
            #         pass
            #     else:
            #         text = f"{text.capitalize()}. "
            #         whole_text += text 
            text = speechTextAzure.speech_text(chunk_filename)
            if len(text) == 0:
                continue
            full_text.append(text)
            text = f"Speaker{current_speaker}: {[str(end.time())]} " + text

            print(text)
            whole_text += text

        #     os.remove(chunk_filename) 
        # # return the text for all chunks detected
        # os.rmdir(folder_name)
        return whole_text
    complete_text = get_large_audio_transcription(os.path.join(pwd, filename))
    com_text.clear()
    com_text.append(complete_text)
    return render(request, 'result.html', {'res': [complete_text.split("."), meeting_start_time, num_speakers, meeting_title]})

def namechange(request):
    global full_text
    pwd = os.getcwd()
    for path in glob.iglob(os.path.join(pwd, '*.wav')):
        os.remove(path)
    for path in glob.iglob(os.path.join(pwd, '*.mp3')):
        os.remove(path)
    names = str(request.POST["spnames"])
    name_list = names.split(" ")[0].split("\r\n")
    for name in name_list:
        sp = name.split(":")[0]
        speaker = name.split(":")[1]
        com_text[0] = com_text[0].replace(sp, speaker)
    text = ". ".join(full_text)
    full_text_ = summarizer.summarize(text)
    return render(request, "namechange.html", {"text": [com_text[0].split("."), full_text_]})
