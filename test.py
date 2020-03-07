import midiFunctions as mf
import numpy as np
import scipy.io.wavfile as wavfile
import soundfile
import os
import matplotlib.pyplot as plt
import spectrumAnalysis as spec
import datetime
import track

x = track.trackList()

a = np.array([1, 2, 3, 4, 5])
a += np.array([1, 1, 1, 1, 1])
print(a)
exit()
in_string = 'C:/PythonProject/GuitarBand/MBD.wav'
out_string = 'C:/PythonProject/GuitarBand/samp.wav'

samp, data = wavfile.read(in_string)
data = data[:2500000]

data = mf.stereo_to_mono(data)

new_data = mf.resample(data, 44100, new_rate=88200)
'''
spec = np.fft.fft(data)
freq = np.fft.fftfreq(len(data), 1/samp)

passfreq = 554.37

for i in range(len(freq)):
    if ((freq[i] < -1045) or (freq[i] > 1045)):
        
        spec[i] = 0.01

plt.plot(freq, np.abs(spec))
plt.show()
new_data = np.array(np.real(np.fft.ifft(spec)), np.int16)
print(new_data)
'''
wavfile.write(out_string, 88200, new_data)
