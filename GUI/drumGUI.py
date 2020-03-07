import sys
import numpy as np
import scipy.io.wavfile as wavfile
import json
import simpleaudio as sa
import time

import midiFunctions as mf
import spectrumAnalysis as spec

from CSS import *

from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *

class saveScreen(QWidget):

    def __init__(self):
        super(saveScreen, self).__init__()

        self.tracks = {}
        self.initUI()

    def initUI(self):

        self.grid = QGridLayout()
        self.filename = QLineEdit()
        self.tempo = QLineEdit()
        self.length = QLineEdit()
        save = QPushButton("Save WAV")
        save.clicked.connect(self.write_wav)
        self.grid.addWidget(QLabel("File name"), 0, 0)
        self.grid.addWidget(QLabel("Tempo"), 1, 0)
        self.grid.addWidget(QLabel("Length"), 2, 0)
        self.grid.addWidget(self.filename, 0, 1)
        self.grid.addWidget(self.tempo, 1, 1)
        self.grid.addWidget(self.length, 2, 1)
        self.grid.addWidget(save, 3, 1, 1, 4)
        self.setLayout(self.grid)
        self.setWindowTitle('Save Window')

    def send_tracks(self, tracks):

        self.tracks = tracks

    def write_wav(self):

        wav = mf.drumTrack("", self.tempo.text(), self.length.text(), isDICT=True, track_data=self.tracks)
        wavfile.write(self.filename.text() + '.wav', 44100, wav.data)

class mainScreen(QWidget):

    def __init__(self):
        super(mainScreen, self).__init__()

        self.initUI()

    def initUI(self):

        self.grid = QGridLayout()
        self.grid.setSpacing(15)

        self.num_bars = 2
        self.time = 16
        self.sample_rate, self.mono = wavfile.read('C:/PythonProject/GuitarBand/Savage Garden - Crash and Burn (Official Video)-W60IPexop30.wav')
        
        #self.sample_rate = 44100

        self.audioPlayer = None
        self.audioPointer = 0
        self.start_time = 0
        self.pause_time = 0
        self.tracks = {}
        self.checks = []

        self.saveScreenWindow = saveScreen()

        self.activeNote = QLabel('za')
        self.audioTimer = QTimer()
        self.audioTimer.timeout.connect(self.update_active_note)

        addDrum = QPushButton("Add Drum")
        savePattern = QPushButton("Save Pattern")
        readPattern = QPushButton("Read Pattern")
        saveWAV = QPushButton("Save to WAV")
        playButton = QPushButton("PLAY")
        stopButton = QPushButton("STOP")

        addDrum.setStyleSheet(BUTTON_STYLE_1)
        savePattern.setStyleSheet(BUTTON_STYLE_1)
        readPattern.setStyleSheet(BUTTON_STYLE_1)        
        readPattern.setStyleSheet(BUTTON_STYLE_1)

        addDrum.clicked.connect(self.add_track)
        savePattern.clicked.connect(self.save_track)
        readPattern.clicked.connect(self.read_track)
        saveWAV.clicked.connect(self.show_save_screen)
        playButton.clicked.connect(self.play_track)
        stopButton.clicked.connect(self.stop_track)

        self.grid.addWidget(addDrum, 0, 0)
        self.grid.addWidget(savePattern, 1, 0)
        self.grid.addWidget(readPattern, 2, 0)
        self.grid.addWidget(saveWAV, 0, 1, 1, 3)
        self.grid.addWidget(playButton, 0, 4, 1, 3)
        self.grid.addWidget(stopButton, 0, 7, 1, 3)
        self.grid.addWidget(self.activeNote, 0, 10, 1, 3)
        self.grid.addWidget(QLabel("Measure"), 3, 0)
        self.grid.addWidget(QLabel("Beat"), 4, 0)
        self.config_measures()
        self.setLayout(self.grid)
        self.setWindowTitle('Drum Machine')

    def config_measures(self):

        for beat in range(self.num_bars * self.time):
            meas_num = QLabel(str(int(beat/self.time + 1)))
            meas_num.setStyleSheet(LABEL_STYLE_1)
            beat_num = QLabel(str((beat % self.time) + 1))
            beat_num.setStyleSheet(LABEL_STYLE_1)
            self.grid.addWidget(meas_num, 3, beat + 1)
            self.grid.addWidget(beat_num, 4, beat + 1)

    def add_track(self):
        track_name, _ = QFileDialog.getOpenFileName(self, 'Open file', 'C:\PythonProject\GuitarBand\drumsamples\Drum Kits', 'WAV files (*.wav)')
        if track_name == "":
            return
        for key in self.tracks.keys():
            if key == track_name:
                return
        
        self.tracks[track_name] = []
        self.checks.append([])
        row_index = len(self.tracks.keys()) + 4
        label = QLabel(track_name[track_name.find("Drum Kits") + 10:-4].replace('/', ': '))
        label.setStyleSheet(LABEL_STYLE_2)
        self.grid.addWidget(label, row_index, 0)

        #self.config_measures()
        
        for beat in range(self.num_bars * self.time):
            self.checks[-1].append(QCheckBox())
            self.checks[-1][beat].setStyleSheet(CHECKBOX_STYLE)
            self.grid.addWidget(self.checks[-1][beat], row_index, beat + 1)
        
    def read_track(self):
        
        json_name, _ = QFileDialog.getOpenFileName(self, 'Open file', 'C:\PythonProject\GuitarBand', 'JSON files (*.json)')
        with open(json_name) as f:
            self.tracks = json.load(f)

        self.checks = []

        for i, track_name in enumerate(self.tracks.keys()):
            row_index = i + 5
            self.checks.append([])
            label = QLabel(track_name[track_name.find("Drum Kits") + 10:-4].replace('/', ': '))
            label.setStyleSheet(LABEL_STYLE_2)
            self.grid.addWidget(label, row_index, 0)

            #self.config_measures()

            for beat in range(self.num_bars * self.time):
                self.checks[-1].append(QCheckBox())
                self.checks[-1][beat].setStyleSheet(CHECKBOX_STYLE)
                self.grid.addWidget(self.checks[-1][beat], row_index, beat + 1)
                if self.tracks[track_name][beat] == True:
                    self.checks[-1][beat].setChecked(True)
        
    def save_track(self):
        direc = 'DrumMachine/'
        filename, okPressed = QInputDialog.getText(self, "Get text","Drum machine name:", QLineEdit.Normal, "")
        for i, track in enumerate(self.tracks.keys()):
            for beat in self.checks[i]:
                self.tracks[track].append(beat.isChecked())

        track = json.dumps(self.tracks)
        f = open(direc + filename + ".json", "w")
        f.write(track)
        f.close()

    def play_track(self):
        
        if self.audioPlayer:
            if self.audioPlayer.is_playing():
                return
        self.audioTimer.start(294.118)
        self.pause_time = time.time()
        self.audioPlayer = sa.play_buffer(self.mono[self.audioPointer:], 2, 2, self.sample_rate)
        self.start_time = self.pause_time

    def stop_track(self):

        self.audioPlayer.stop()
        self.audioTimer.stop()
        self.pause_time = time.time()
        self.audioPointer += int((self.pause_time - self.start_time) * self.sample_rate)
        if self.audioPointer >= len(self.mono):
            self.audioPointer = 0

    def update_active_note(self):
        
        current_pointer = int(self.audioPointer + (time.time() - self.start_time) * self.sample_rate)
        current_data = self.mono[current_pointer:current_pointer+int(0.294118*self.sample_rate)]
        current_spec = spec.get_spectrum(current_data, self.sample_rate)
        max_note = ''
        max_mag = 0
        for note in current_spec.keys():
            if current_spec[note] > max_mag:
                max_note = note
                max_mag = current_spec[note]

        self.activeNote.setText(max_note)

    def show_save_screen(self):
        self.saveScreenWindow.send_tracks(self.tracks)
        self.saveScreenWindow.show()

if __name__ == '__main__':

    app = QApplication(sys.argv)
    s = mainScreen()
    s.show()
    sys.exit(app.exec_())