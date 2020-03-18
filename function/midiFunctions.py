import function.midiConstants as md
import numpy as np
from scipy.io import wavfile
import os.path as path
import json

def midi_to_freq(midi):

    freq = 440 * 2 ** ((midi - 69) / 12)
    return freq

def freq_to_midi(freq):

    midi = int(np.round(12 * np.log2(freq/440) + 69))
    #print(md.NOTE_VALUE_MAP_SHARP[midi])
    return(midi)

def make_note(note, magnitude, track_length, bit_depth, sample_rate=44100, decay_rate=0):

    # Note can either be a string (ex. 'C_5') or a midi number (ex. 72), not a frequency
    midi = 0
    if type(note) == str:
        
        # If note is not flat (either sharp or normal), read from SHARP map
        if note[1] == 's' or note[1] == '_':

            try:
                midi = md.NOTE_NAME_MAP_SHARP[note]
            except KeyError:
                raise KeyError('%s is not a valid midi note' % note)

        # If note is flat, read from FLAT map
        elif note[1] == 'b':

            try:
                midi = md.NOTE_NAME_MAP_FLAT[note]
            except KeyError:
                raise KeyError('%s is not a valid midi note' % note)

    # If note is already an int (midi note), continue
    elif type(note) == int:
        
        if note > 127 or note < 0:
            raise ValueError('Midi note %d out of range 0-127' % note)

        midi = note

    else:
        raise TypeError('Note must be either int or string type')

    freq = midi_to_freq(midi)
    track = np.linspace(0, freq * track_length * 2 * np.pi, int(track_length * sample_rate))
    track = np.round(magnitude * np.sin(track))

    if decay_rate > 0:
        # -4 is used to signify the 2% point
        decay = np.power(np.e, np.linspace(0, len(track) * (-4) / (decay_rate * sample_rate), len(track)))
        track *= decay

    track = np.array(track, 'int' + str(bit_depth))

    return track

def stereo_to_mono(data):

    mono_data = np.zeros(len(data))
    for i in range(len(data)):
        mono_data[i] = int(data[i][0] / 2 + data[i][1] / 2)
    return mono_data

def resample(data, old_rate, new_rate=44100):

    ratio = old_rate / new_rate
    new_data = np.zeros(int(len(data) / ratio) + 1, dtype=np.int16)
    maxf = 0
    print(ratio)
    print(len(data) / len(new_data))
    print(len(data))
    print(len(new_data))
    print((len(new_data) - 2) * ratio)
    for i in range(len(new_data) - 20):

        f = int(np.floor(i*ratio))
        q = i*ratio - f
        new_data[i] = int(q*data[f] + (1-q)*data[f+1])
        if new_data[i] > maxf:
            maxf = new_data[i]

    print(maxf)
    return new_data