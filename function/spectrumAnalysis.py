import numpy as np
import matplotlib
from matplotlib.pyplot import *
import scipy.io.wavfile as wavfile
import soundfile
import simpleaudio as sa

import function.midiFunctions as mf
import function.midiConstants as md

NUM_BINS = 85
BASE_FREQ = 27.5
freq_mag = np.zeros(NUM_BINS)
freq_bins_centre = []

for i in range(-1, NUM_BINS + 1):
    freq_bins_centre.append(BASE_FREQ * (2 ** (i/12)))

def get_spectrum(data, sample_rate):

    # data = data[0:int(samp * 0.3)]

    if np.shape(data)[1] == 2:
        data = mf.stereo_to_mono(data)
    
    spectrum = np.abs(np.fft.fft(data))
    freq = np.fft.fftfreq(len(data), 1/sample_rate)

    #Keep only positive frequencies
    spectrum = spectrum[:int(len(spectrum)/2)]
    freq = freq[:int(len(freq)/2)]

    bin_ptr = 1
    bin_low_lim = (freq_bins_centre[bin_ptr] * freq_bins_centre[bin_ptr - 1]) ** 0.5
    bin_high_lim = (freq_bins_centre[bin_ptr] * freq_bins_centre[bin_ptr + 1]) ** 0.5
    freq_mag = np.zeros(NUM_BINS)
    temp_array = []

    for i in range(len(freq)):

        if (freq[i] > bin_low_lim) and (freq [i] < bin_high_lim):
            temp_array.append(spectrum[i])
        elif (freq[i] > bin_high_lim):
            if len(temp_array) == 0:
                temp_array = [0]
            mag = sum(temp_array) / len(temp_array)
            freq_mag[bin_ptr - 1] = mag
            bin_ptr += 1

            if bin_ptr > NUM_BINS:
                break
            
            bin_low_lim = (freq_bins_centre[bin_ptr] * freq_bins_centre[bin_ptr - 1]) ** 0.5
            bin_high_lim = (freq_bins_centre[bin_ptr] * freq_bins_centre[bin_ptr + 1]) ** 0.5
            temp_array = []
        
    freq_mag /= max(freq_mag)

    note_indices = []
    max_notes = []
    bin_dict = {}

    for i in range(1, len(freq_mag)):
        # if (freq_mag[i] > freq_mag[i + 2]) and (freq_mag[i] > freq_mag[i - 2]) and (freq_mag[i] > freq_mag[i - 1]) and (freq_mag[i] > freq_mag[i + 1]):
        # max_notes.append(freq_mag[i])
        # note_indices.append(i + 1)
        bin_dict[md.NOTE_VALUE_MAP_SHARP[mf.freq_to_midi(freq_bins_centre[i])]] = freq_mag[i - 1]

    #print(bin_dict)
    return(bin_dict)
    '''
    for i in range(len(max_notes)):
        print("%.3f: %.1f" % (freq_bins_centre[note_indices[i]], max_notes[i] * 100))



    ax = subplot(111)
    #ax.set_xscale('log')
    #ax.xaxis.set_major_formatter(ScalarFormatter())

    #ax.set_xticks(ticks, labels)
    xscale('log')

    ax.plot(freq_bins_centre[1:-1], freq_mag)
    show()
    '''