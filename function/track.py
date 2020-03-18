import numpy as np
from scipy.io import wavfile
import os.path as path
import json

import function.midiFunctions as mf
import function.midiConstants as md

class trackList:

    def __init__(self, num_tracks=5):

        self.num_tracks = num_tracks
        self.sample_rate = 44100
        self.final_mag = 30000

        self.trackInfo = [None for i in range(num_tracks)]
        self.currentData = None

        self.init_tracks()

    def init_tracks(self):

        # Trackstart: where in individual track to begin reading data (default is 0)
        # Trackend: where in individual track to end reading data (default is len(track.data))
        # Finallocation: where in final track to begin playing individual track (default is 0)

        # template = {"object": None, "trackstart": None, "trackend": None, "finalposition": None, "tempomult": None, "keyshift": None}

        for i in range(self.num_tracks):
            self.trackInfo[i] = {"object": None, "trackstart": 0, "trackend": 0, "finalposition": 0, "tempomult": 1, "keyshift": 0, "volume": 1.0}

        print(self.trackInfo)
    
    def write_to_array(self):

        len_final = 0

        # Find how long the final track will be
        for track in self.trackInfo:

            if not track is None:
                track_end = self.sample_rate * (track["finalposition"] + (track["trackend"] - track["trackstart"]))
                if track_end > len_final:
                    len_final = track_end

        self.currentData = np.zeros(len_final, dtype=np.int16)

        # Determine which track has highest magnitude, use this to normalize track later
        max_mag = 0
        for track in self.trackInfo:

            max_mag = max(max_mag, np.mean(track["object"].data))

            if not track["object"] is None:
                self.currentData[self.sample_rate * track["finalposition"]:self.sample_rate * (track["finalposition"] + (track["trackend"] - track["trackstart"]))] += \
                    track["object"].data[track["trackstart"]:track["trackend"]]


        # Normalize to maximimum magnitude, maintain bit depth
        if (abs(max(self.currentData)) > abs(min(self.currentData))):
            self.currentData = np.round(self.currentData * (32767 / abs(max(self.currentData))))
        else:
            self.currentData = np.round(self.currentData * (32767 / abs(min(self.currentData))))


class track:

    def __init__(self, bit_depth=16, sample_rate=44100):

        self.type = "Record"

        self.sample_rate = sample_rate
        self.bit_depth = bit_depth
        self.datatype = 'int' + str(bit_depth)

        self.data = np.empty(0, dtype=self.datatype)

        # Track length in seconds
        self.track_length = 0

    # Set the data for the output .wav file
    def set_data(self, data):

        self.data = data
        self.update_track_length()

    # Called every time the track length changes
    def update_track_length(self):

        self.track_length = len(self.data) / self.sample_rate

    # Layer tracks over each other, maintain original magnitude
    def layer_tracks(self, track_list):

        num_tracks = len(track_list)

        # Determine which track has highest magnitude, use this to normalize track later
        max_mag = 0
        new_track = np.empty(0)

        for i in range(num_tracks):

            max_mag = max(max_mag, np.mean(track_list[i]))

            if (len(track_list[i]) > len(new_track)):
                new_track = np.pad(new_track, (0, len(track_list[i]) - len(new_track)), 'constant')
            else:
                track_list[i] = np.pad(track_list[i], (0, len(new_track) - len(track_list[i])), 'constant')
            
            new_track = np.add(new_track, track_list[i])

        # Normalize to maximimum magnitude, maintain bit depth
        # track = np.round(track * (max_mag / np.mean(track)))
        if abs(max(new_track)) > abs(min(new_track)):
            new_track = np.round(new_track * (32767 / abs(max(new_track))))
        else:
            new_track = np.round(new_track * (32767 / abs(min(new_track))))
        
        new_track = np.array(new_track, self.datatype)
        self.update_track_length()
        return new_track

    def add_effects(self, **kwargs):

        for effect in kwargs:

            param = kwargs[effect]

            if effect == "phaser":
                phase = np.sin(np.linspace(0, param * self.track_length * 2 * np.pi, len(self.data)))
                self.data = np.array(self.data * phase)

            if effect == "decay":
                decay = np.power(np.e, np.linspace(0, param, len(self.data)))
                self.data = np.array(self.data * decay)

            # Default flanger range will be 20ms (882 samples), param is period of effect in seconds
            if effect == "flanger":
                flange = int(self.sample_rate * 0.005)

                # Array by which the index for each data point will be phase shifted
                new_track = np.empty(len(self.data))
                shift_array = np.array(flange * np.sin(np.linspace(0, (self.track_length / param) * 2 * np.pi, len(self.data))), 'int')
                print(min(shift_array))
                for i in range(len(new_track) - flange):

                    new_track[i] = self.data[i - shift_array[i]]

                self.data = self.layer_tracks([self.data, new_track])


class fileTrack(track):

    def __init__(self, filename):

        super(fileTrack, self).__init__()

        self.type = "File"

        if not path.exists(filename):
            raise FileNotFoundError("Cannot find file " + filename)

        self.source_file = filename
        self.extract_features()

    def extract_features(self):

        self.sample_rate, self.data = wavfile.read(self.source_file)
        self.data = self.data.astype(np.int16)
        self.bit_depth = 16

class drumTrack(track):

    def __init__(self, filename, tempo, track_length, isDICT=False, track_data=None):

        super(drumTrack, self).__init__()

        self.type = "Drum machine"

        if not path.exists(filename) and not isDICT:
            raise FileNotFoundError("Cannot find file " + filename)

        self.source_file = filename
        self.tempo = tempo
        self.track_length = track_length # in seconds
        self.drum_dict = {}
        if isDICT:
            self.drum_dict = track_data
        else:
            with open(self.source_file) as f:
                self.drum_dict = json.load(f)
        self.unpack()

    def unpack(self):
            
        self.num_tracks = len(self.drum_dict.keys())
        self.track_list = np.empty((self.num_tracks, int(self.track_length * self.sample_rate)), dtype=np.int16)

        samples_per_beat = int(self.sample_rate / (self.tempo / 60))
        mod = (self.track_length * self.sample_rate) % samples_per_beat

        for i, key in enumerate(self.drum_dict.keys()):
            #print(key)
            _ , temp_data = wavfile.read(key)

            #Stereo to mono conversion
            if temp_data.ndim == 2:
                temp_data = mf.stereo_to_mono(temp_data)

            if len(temp_data) >= samples_per_beat:
                temp_data = temp_data[0:samples_per_beat]
            else:
                temp_data = np.pad(temp_data, (0, samples_per_beat - len(temp_data)), 'constant')
            
            for j, beat in enumerate(self.drum_dict[key]):
                for step in range(0, int(self.track_length * self.sample_rate/samples_per_beat), len(self.drum_dict[key])):
                    if beat == True:
                        if (j + step)*samples_per_beat > (self.track_length * self.sample_rate):
                            continue
                        if (j + step + 1)*samples_per_beat > (self.track_length * self.sample_rate):
                            self.track_list[i][(j + step)*samples_per_beat:(self.track_length * self.sample_rate)] = temp_data[:mod]
                        else:
                            self.track_list[i][(j + step)*samples_per_beat:(j + step + 1)*samples_per_beat] = temp_data

        self.data = self.layer_tracks(self.track_list)


class synthTrack(track):

    def __init__(self, tempo, magnitude=10000, bit_depth=16, sample_rate=44100):

        super(synthTrack, self).__init__()

        self.type = "Synth"

        self.tempo = tempo
        self.magnitude = magnitude
        self.sample_rate = sample_rate
        self.bit_depth = bit_depth
        self.datatype = 'int' + str(bit_depth)

        self.data = np.empty(0, dtype=self.datatype)

        # Track length in seconds
        self.track_length = 0
        self.chord_list = dict()

    def add_to_track(self, num_beats, note_type, notes, chords, decay=0):

        track_list = []
        segment_length = (60 / self.tempo) * 4 * num_beats / note_type
        
        # Add each individual note 
        for i in range(len(notes)):

            track_list.append(mf.make_note(notes[i], self.magnitude, segment_length, self.bit_depth, self.sample_rate, decay_rate=decay))

        for i in range(len(chords)):

            for j in range(len(self.chord_list[chords[i]])):

                track_list.append(mf.make_note(self.chord_list[chords[i]][j], self.magnitude, segment_length, self.bit_depth, self.sample_rate, decay_rate=decay))

        new_track = self.layer_tracks(track_list)

        self.data = np.concatenate((self.data, new_track))
        self.update_track_length()

    # Called every time the track length changes
    def update_track_length(self):

        self.track_length = len(self.data) / self.sample_rate

    # Add any commonly used chords to the chord dictionary
    def add_chords_to_dict(self, chord_name, midi_list):

        if not type(midi_list) == list:
            raise TypeError("midi_list must be list type")

        self.chord_list[chord_name] = midi_list

    # Might not ever use
    def concat_tracks(self, track_list):

        num_tracks = len(track_list)
        new_track = np.array(track_list[0])

        for i in range(1, num_tracks):

            new_track = np.concatenate((new_track, track_list[i]))

        return new_track