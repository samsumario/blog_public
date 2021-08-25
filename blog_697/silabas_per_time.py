import sys
import os
import json
import wave

from vosk import Model, KaldiRecognizer, SetLogLevel
from pyverse import Pyverse

SetLogLevel(0)

def save_result(file_name, recognize_sentence_list, total_time):

    with open(file_name, mode="w", encoding="utf_8") as f:

        result_sentence = ""

        #write recognize sentence
        for line in recognize_sentence_list:
            f.write(line + "\n")
            result_sentence = result_sentence + " " + line
        
        #calc result
        total_words = len(result_sentence.split())
        wps_average = total_words / total_time
        total_silabas = Pyverse(result_sentence)
        silabas_average =  total_silabas.count / total_time

        #write result
        f.write("/--- result ---/ \n")
        f.write("total time : " + str(total_time) + "\n")
        f.write("total words : " + str(total_words) + "\n")
        f.write("minute conversion : " + str(wps_average*60) + "\n")
        f.write("total silabas : " + str(total_silabas.count) + "\n")
        f.write("minute conversion : " + str(silabas_average*60) + "\n")


def main(wav_file, save_file):

    if not os.path.exists("model"):
        print ("Please download the model from https://alphacephei.com/vosk/models and unpack as 'model' in the current folder.")
        exit (1)

    wf = wave.open(wav_file, "rb")
    if wf.getnchannels() != 1 or wf.getsampwidth() != 2 or wf.getcomptype() != "NONE":
        print ("Audio file must be WAV format mono PCM.")
        exit (1)

    #vosk setting
    model = Model("model")
    frame_rate = wf.getframerate()
    rec = KaldiRecognizer(model, frame_rate)
    rec.SetWords(True)

    #parameter for speed measure
    time_counter = 0 #sec
    time_width = 0.25 #sec
    previous_sentence = ""
    recognize_sentence_list = []

    #start wav file reading
    while True:
        data = wf.readframes(int(frame_rate * time_width))

        if len(data) == 0:
            break
        
        if rec.AcceptWaveform(data):
            result_sentence = json.loads(rec.Result())['text']
            
            #store sentence
            recognize_sentence_list.append(result_sentence)

            #update measure parameter
            previous_sentence = ""
            time_counter = time_counter + time_width
            
        else:
            current_sentence = json.loads(rec.PartialResult())['partial']

            diff = len(current_sentence.split()) - len(previous_sentence.split())
            
            #update measure parameter
            if diff == 0:
                previous_sentence = ""

            else:
                previous_sentence = current_sentence
                time_counter = time_counter + time_width

    save_result(save_file, recognize_sentence_list, time_counter)

#command example
#python silabas_per_time.py mono.wav result.txt
if __name__ == '__main__':
    main(sys.argv[1], sys.argv[2])