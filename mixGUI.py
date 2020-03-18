import sys
import numpy as np
import scipy.io.wavfile as wavfile
import time
import simpleaudio as sa
import datetime

import function.midiFunctions as mf
import function.spectrumAnalysis as spec
import function.track as track

from CSS import *

from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *


TRACK_TYPES = ['Record', 'Synth', 'Drum Machine', 'From File']

class mainScreen(QWidget):

    def __init__(self):

        super(mainScreen, self).__init__()

        self.trackList = track.trackList()
        self.initUI()

    def initUI(self):

        self.setStyleSheet(MAIN_WINDOW_STYLE)
        self.grid = QGridLayout()

        self.num_tracks = 5

        #######################
        #Audio player functions
        #######################

        self.sample_rate, self.mono = wavfile.read('C:/PythonProject/guitarband/TestWAVs/MBD.wav')
        self.audioPlayer = None
        self.audioPointer = 0
        self.start_time = 0
        self.pause_time = 0
        self.activeNote = QLabel('')
        self.activeNote.setMinimumWidth(25)
        self.audioTimer = QTimer()
        self.audioTimer.timeout.connect(self.update_active_note)
        self.audioSlider = QSlider(Qt.Horizontal)
        self.audioSlider.setMinimum(0)
        self.audioSlider.setMaximum(len(self.mono))
        self.audioSlider.sliderMoved.connect(self.drag_slider)

        self.currentAudioLabel = QLabel((str(datetime.timedelta(seconds=0)))[2:])
        self.audioLengthLabel = QLabel(str(datetime.timedelta(seconds=int(len(self.mono) / 44100)))[2:])
                
        playButton = QPushButton("PLAY")
        stopButton = QPushButton("STOP")
        playButton.clicked.connect(self.play_track)
        stopButton.clicked.connect(self.stop_track)
        
        ###############################
        # Static top-of-window elements
        ###############################

        self.grid.addWidget(playButton, 0, 4, 1, 3)
        self.grid.addWidget(stopButton, 0, 7, 1, 3)
        self.grid.addWidget(self.activeNote, 0, 10, 1, 3)
        self.grid.addWidget(self.currentAudioLabel, 1, 3)
        self.grid.addWidget(self.audioSlider, 1, 4, 1, 8)
        self.grid.addWidget(self.audioLengthLabel, 1, 12)

        guitar_label = QLabel("Guitar Band")
        guitar_label.setStyleSheet(TITLE_STYLE)
        self.grid.addWidget(guitar_label, 0, 0, 2, 3)

        ##################################
        # Settings Menu to right of window
        ##################################

        self.settingBox = QGroupBox()
        self.settingBoxGrid = QGridLayout()

        self.selectTrack = QComboBox()
        self.selectTrack.addItems([str(i) for i in range(1, self.num_tracks + 1)])
        self.activeTrackStart = QLineEdit()
        self.activeTrackEnd = QLineEdit()
        self.activeTrackPosition = QLineEdit()
        self.activeTempoMultiplier = QLineEdit()
        self.activeKeyShift = QLineEdit()
        self.activeVolume = QLineEdit()

        self.selectTrack.currentIndexChanged.connect(self.load_track_params)
        self.activeTrackStart.editingFinished.connect(self.track_start_update)
        self.activeTrackEnd.editingFinished.connect(self.track_end_update)
        self.activeTrackPosition.editingFinished.connect(self.track_position_update)
        self.activeTempoMultiplier.editingFinished.connect(self.tempo_update)
        self.activeKeyShift.editingFinished.connect(self.key_update)
        self.activeVolume.editingFinished.connect(self.volume_update)

        self.settingBoxGrid.addWidget(QLabel("Edit Audio Menu"), 0, 0)
        self.settingBoxGrid.addWidget(self.selectTrack, 1, 0)
        self.settingBoxGrid.addWidget(QLabel("Track Start"), 2, 0)
        self.settingBoxGrid.addWidget(self.activeTrackStart, 3, 0)
        self.settingBoxGrid.addWidget(QLabel("Track End"), 4, 0)
        self.settingBoxGrid.addWidget(self.activeTrackEnd, 5, 0) 
        self.settingBoxGrid.addWidget(QLabel("Track Position"), 6, 0)
        self.settingBoxGrid.addWidget(self.activeTrackPosition, 7, 0)   
        self.settingBoxGrid.addWidget(QLabel("Tempo Multiplier"), 8, 0)
        self.settingBoxGrid.addWidget(self.activeTempoMultiplier, 9, 0)  
        self.settingBoxGrid.addWidget(QLabel("Key Shift"), 10, 0)
        self.settingBoxGrid.addWidget(self.activeKeyShift, 11, 0)        
        self.settingBoxGrid.addWidget(QLabel("Volume"), 12, 0)
        self.settingBoxGrid.addWidget(self.activeVolume, 13, 0)      

        self.settingBox.setLayout(self.settingBoxGrid)
        self.settingBox.setStyleSheet(SETTING_WINDOW_STYLE)
        self.grid.addWidget(self.settingBox, 0, 14, 14, 1)

        #############################
        # Visual indicators per track
        #############################
        
        self.trackNames = []
        self.trackTypeBox = []
        self.loadTrackBtn = []
        
        for i in range(self.num_tracks):

            self.trackNames.append(QLineEdit())
            self.trackNames[i].setFrame(False)
            self.trackNames[i].setPlaceholderText('Track ' + str(i))
            self.trackNames[i].setMaximumWidth(100)

            self.trackTypeBox.append(QComboBox())
            self.trackTypeBox[i].addItems(TRACK_TYPES)
            self.trackTypeBox[i].setStyleSheet(RANDOM_COMBO_BOX)

            self.loadTrackBtn.append(QPushButton("Load track"))

            self.grid.addWidget(self.trackNames[i], 2*(i+2), 0)
            self.grid.addWidget(self.trackTypeBox[i], 2*(i+2)+1, 0)
            self.grid.addWidget(self.loadTrackBtn[i], 2*(i+2), 1)
        
        #Button functions
        self.trackTypeBox[0].currentIndexChanged.connect(lambda: self.track_type_update(0))
        self.trackTypeBox[1].currentIndexChanged.connect(lambda: self.track_type_update(1))
        self.trackTypeBox[2].currentIndexChanged.connect(lambda: self.track_type_update(2))
        self.trackTypeBox[3].currentIndexChanged.connect(lambda: self.track_type_update(3))
        self.trackTypeBox[4].currentIndexChanged.connect(lambda: self.track_type_update(4))

        self.loadTrackBtn[0].clicked.connect(lambda: self.load_track(0))
        self.loadTrackBtn[1].clicked.connect(lambda: self.load_track(1))
        self.loadTrackBtn[2].clicked.connect(lambda: self.load_track(2))
        self.loadTrackBtn[3].clicked.connect(lambda: self.load_track(3))
        self.loadTrackBtn[4].clicked.connect(lambda: self.load_track(4))

        self.setLayout(self.grid) 
        #self.setGeometry(100, 300, 350, 300)
        self.setWindowTitle('Guitar Band')

    '''
    def track_type_update(self, i):
        self.trackList.trackInfo[i]["object"].type = self.trackTypeBox[i].currentText()
    '''

    def load_track(self, i):

        tr_text = ""
        if self.trackTypeBox[i].currentText() == "Drum Machine":
            tr_text = "JSON files (*.json)"
        elif self.trackTypeBox[i].currentText() == "From File":
            tr_text = "WAV files (*.wav)"

        try:
            fname, _ = QFileDialog.getOpenFileName(self, 'Open file', 'C:/PythonProject', tr_text)
        except (FileNotFoundError, IOError):
            print("File not found")

    def play_track(self):
        
        if self.audioPlayer:
            if self.audioPlayer.is_playing():
                return
        self.audioTimer.start(294.118)
        self.pause_time = time.time()
        self.audioPlayer = sa.play_buffer(self.mono[self.audioPointer:], 2, 2, self.sample_rate)
        self.start_time = self.pause_time

    def stop_track(self):

        if self.audioPlayer is None:
            return

        self.audioPlayer.stop()
        self.audioTimer.stop()
        self.pause_time = time.time()
        self.audioPointer += int((self.pause_time - self.start_time) * self.sample_rate)
        if self.audioPointer >= len(self.mono):
            self.audioPointer = 0

    def drag_slider(self):
        self.audioPointer = self.audioSlider.value()
        if self.audioPlayer:            
            if self.audioPlayer.is_playing():
                self.audioPlayer.stop()
                self.audioPlayer = sa.play_buffer(self.mono[self.audioPointer:], 2, 2, self.sample_rate)
        #self.update_active_note()

    def update_active_note(self):
        
        current_pointer = int(self.audioPointer + (time.time() - self.start_time) * self.sample_rate)
        self.audioSlider.setValue(current_pointer)
        self.currentAudioLabel.setText(str(datetime.timedelta(seconds=int(current_pointer/self.sample_rate)))[2:])

        current_data = self.mono[current_pointer:current_pointer+int(0.294118*self.sample_rate)]
        current_spec = spec.get_spectrum(current_data, self.sample_rate)
        max_note = ''
        max_mag = 0
        for note in current_spec.keys():
            if current_spec[note] > max_mag:
                max_note = note
                max_mag = current_spec[note]

        self.activeNote.setText(max_note)

    # TRACK SETTING FUNCTIONS

    def track_start_update(self):
        print(self.trackList.trackInfo[0]["trackstart"])
        self.trackList.trackInfo[int(self.selectTrack.currentText()) - 1]["trackstart"] = float(self.activeTrackStart.text())
        print(self.trackList.trackInfo[0]["trackstart"])

    def track_end_update(self):
        self.trackList.trackInfo[int(self.selectTrack.currentText()) - 1]["trackend"] = float(self.activeTrackEnd.text())

    def track_position_update(self):
        self.trackList.trackInfo[int(self.selectTrack.currentText()) - 1]["finalposition"] = float(self.activeTrackPosition.text())

    def tempo_update(self):
        self.trackList.trackInfo[int(self.selectTrack.currentText()) - 1]["tempomult"] = float(self.activeTempoMultiplier.text())

    def key_update(self):
        self.trackList.trackInfo[int(self.selectTrack.currentText()) - 1]["keyshift"] = int(self.activeKeyShift.text())

    def volume_update(self):
        self.trackList.trackInfo[int(self.selectTrack.currentText()) - 1]["volume"] = float(self.activeVolume.text())

    def load_track_params(self):
        
        # Track for which to load data
        i = int(self.selectTrack.currentText()) - 1
        print(self.trackList.trackInfo)

        self.activeTrackStart.setText(str(self.trackList.trackInfo[i]["trackstart"]))
        self.activeTrackEnd.setText(str(self.trackList.trackInfo[i]["trackend"]))
        self.activeTrackPosition.setText(str(self.trackList.trackInfo[i]["finalposition"]))
        self.activeTempoMultiplier.setText(str(self.trackList.trackInfo[i]["tempomult"]))
        self.activeKeyShift.setText(str(self.trackList.trackInfo[i]["keyshift"]))
        self.activeVolume.setText(str(self.trackList.trackInfo[i]["volume"]))



if __name__ == '__main__':

    app = QApplication(sys.argv)
    s = mainScreen()
    s.show()
    sys.exit(app.exec_())