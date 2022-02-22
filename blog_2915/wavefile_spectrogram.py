import numpy as np
from scipy import signal
from scipy.io import wavfile
import matplotlib.pyplot as plt

# load wav file
samplerate, data = wavfile.read('file_name.wav')
time = data.shape[0] / samplerate
print("file length = {} sec".format(time))

# stereo to mono
if(len(data.shape) > 1):
    data = data[:,0] #Left channel
    
#Spectrogram(STFT)
N=512*7
freqs, times, Sxx = signal.spectrogram(data, fs=samplerate, window='han',
                                    nperseg=N, noverlap=N-100)

# graph setting
plt.pcolormesh(times, freqs, 10 * np.log(np.abs(Sxx)), cmap = 'inferno')

plt.ylim([0, 2000])
plt.xlim([0, 5])

plt.ylabel('Frequency [Hz]')
plt.xlabel('Time [sec]')

cbar = plt.colorbar()
cbar.ax.set_ylabel("Intensity [dB]")

plt.show()

