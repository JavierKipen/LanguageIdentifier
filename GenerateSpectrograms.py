import wave
import glob, os
import numpy as np
import struct
import librosa as lr
import librosa.display
import h5py


def get_wav_samples(wav): ##https://stackoverflow.com/questions/7769981/how-to-convert-wav-file-to-float-amplitude
    astr = wav.readframes(wav.getnframes())
    a = struct.unpack("%ih" % (wav.getnframes() * wav.getnchannels()), astr)
    a = [float(val) / pow(2, 15) for val in a]
    return a


src_dir="C:/Users/Javier/PycharmProjects/TP2Voz/DatasetsPreProcessed/"
window_time=0.02; #20ms para la voz con overlap es todo lo que está bien
rate= 16000; #Asegurarse que windowsize se pueda dividir por 2! (Para el overlap.
window_size=int(window_time*rate)
audio_len=5 * rate
n_windows= int(2*(audio_len - window_size) / window_size)
nmels=128

n_audios_per_lang=10

whole_dataset=np.zeros((n_audios_per_lang*3,nmels,501))
dict={0:"de",1:"en",2:"es"}
index=0
for lang in range(3):
    os.chdir(src_dir+dict[lang])
    for file in glob.glob("*.wav"):
        win = wave.open(file, 'r')
        speech_samples = np.array(get_wav_samples(win))
        spec= lr.feature.melspectrogram(speech_samples, sr=rate, n_mels=128, n_fft=2048, hop_length=int(window_size/2), win_length=window_size, window='hamming', center=True, pad_mode='reflect', power=2.0)
        whole_dataset[index,:,:] = lr.core.amplitude_to_db(spec)
        win.close()
        index += 1
        if index % n_audios_per_lang == 0:
            break

n_train=int(n_audios_per_lang*3*0.8)
n_valid=int(n_audios_per_lang*3*0.1)
n_test=int(n_audios_per_lang*3*0.1)

dataset_target=np.zeros((1,n_audios_per_lang*3))
dataset_target[0,n_audios_per_lang:n_audios_per_lang*2]=1;
dataset_target[0,n_audios_per_lang*2:n_audios_per_lang*3]=2; #Se ponen los targets

index_permut=np.random.permutation(n_audios_per_lang*3) ##Se desordenan los datos aleatoriamente
dataset_target=dataset_target[0,index_permut]
whole_dataset=whole_dataset[index_permut,:,:];

## Se divide el dataset en train valid y test:

x_tr=whole_dataset[0:n_train,:,:]
y_tr=dataset_target[0:n_train]
x_va=whole_dataset[n_train:n_train+n_valid,:,:]
y_va=dataset_target[n_train:n_train+n_valid]
x_te=whole_dataset[n_train+n_valid:-1,:,:]
y_te=dataset_target[n_train+n_valid:-1]


np.savez("C:/Users/Javier/PycharmProjects/TP2Voz/DatasetsPreProcessed/dataset", x_tr,y_tr,x_va,y_va,x_te,y_te)

del whole_dataset
del dataset_target

npzfile = np.load("C:/Users/Javier/PycharmProjects/TP2Voz/DatasetsPreProcessed/dataset.npy")
npzfile.files
