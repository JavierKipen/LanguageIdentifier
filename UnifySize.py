import numpy as np
import glob, os
import soundfile as sf
import wave
import glob, os
import struct
import random

def get_wav_samples(wav): ##https://stackoverflow.com/questions/7769981/how-to-convert-wav-file-to-float-amplitude
    astr = wav.readframes(wav.getnframes())
    a = struct.unpack("%ih" % (wav.getnframes() * wav.getnchannels()), astr)
    a = [float(val) / pow(2, 15) for val in a]
    return a

def float_to_int_bytes(data_in):
    data_out = [val * pow(2, 15) for val in data_in]
    data_out = np.int16(data_out)
    data_ret = bytes(data_out)
    return data_ret

src_dir="C:/Users/Javier/PycharmProjects/TP2Voz/Datasets/de"
dest_dir="C:/Users/Javier/PycharmProjects/TP2Voz/DatasetsPreProcessed/de"
i=0;
os.chdir(src_dir)

desired_duration=5;
dataset_desired_length=2000;

for file in glob.glob("*.wav"):
    win = wave.open(file, 'r')
    rate = win.getframerate();
    nsamples=win.getnframes();
    duration=win.getnframes()/rate;
    raw_audio= get_wav_samples(win)
    if duration > 4 and np.std(raw_audio) > 1e-5 and i<dataset_desired_length: ##Si es muy corto o de muy poco volumen se lo omite.
        i = i + 1
        fout = dest_dir + "/"+ str(i) + ".wav"
        wout = wave.open(fout, "w")
        wout.setframerate(rate)
        wout.setsampwidth(win.getsampwidth())
        wout.setnchannels(1)

        if duration >= desired_duration :
            raw_audio_out=raw_audio[0:desired_duration*rate]
        else:
            samples_to_add=int(desired_duration * rate-nsamples);
            zeros_to_add=np.zeros((samples_to_add,)).tolist()
            if random.randint(0, 1):
                raw_audio_out = raw_audio + zeros_to_add
            else:
                raw_audio_out = zeros_to_add + raw_audio
        wout.writeframesraw(float_to_int_bytes(raw_audio_out))
        wout.close()
    win.close()
