import sys
import numpy as np
import scipy.io.wavfile as wavfile
import time
import simpleaudio as sa
import datetime

from CSS import *
import midiFunctions as mf
import spectrumAnalysis as spec
import track

from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *


TRACK_TYPES = ['Record', 'Synth', 'Drum machine', 'From file']

class mainScreen(QWidget):

    def __init__(self):
        super(mainScreen, self).__init__()

        self.initUI()
        # self.initSetForm()
        self.trackList = track.trackList()

    def initUI(self):

        self.setStyleSheet(MAIN_WINDOW_STYLE)
        self.grid = QGridLayout()
        #self.grid.setSpacing(0)

        self.num_tracks = 5
        self.trackNames = []
        self.trackTypeBox = []
        self.loadTrackBtn = []

        #Audio player functions
        self.sample_rate, self.mono = wavfile.read('C:/PythonProject/GuitarBand/MBD.wav')
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
        
        # Static top-of-window elements

        self.grid.addWidget(playButton, 0, 4, 1, 3)
        self.grid.addWidget(stopButton, 0, 7, 1, 3)
        self.grid.addWidget(self.activeNote, 0, 10, 1, 3)
        self.grid.addWidget(self.currentAudioLabel, 1, 3)
        self.grid.addWidget(self.audioSlider, 1, 4, 1, 8)
        self.grid.addWidget(self.audioLengthLabel, 1, 12)

        # Menu to right of window

        self.settingBox = QGroupBox()
        self.settingBoxGrid = QGridLayout()
        self.settingBoxGrid.addWidget(QLabel("Edit Audio"), 0, 0)
        self.settingBox.setLayout(self.settingBoxGrid)
        self.grid.addWidget(self.settingBox, 0, 14, 12, 1)

        guitar_img = QLabel()
        pixmap = QPixmap('C:/PythonProject/GuitarBand/les paul.png')
        pixmap = pixmap.scaledToWidth(216)
        guitar_img.setPixmap(pixmap)
        guitar_img.setMaximumHeight(216)
        guitar_img.setMaximumWidth(384)

        self.grid.addWidget(guitar_img, 0, 0, 2, 3)

        #GUI design
        for i in range(self.num_tracks):

            self.trackNames.append(QLineEdit())
            self.trackNames[i].setFrame(False)
            self.trackNames[i].setPlaceholderText('Track ' + str(i))

            self.trackTypeBox.append(QComboBox())
            self.trackTypeBox[i].addItems(TRACK_TYPES)
            self.trackTypeBox[i].setStyleSheet(RANDOM_BOX_EDIT)
            #print(RANDOM_LINE_EDIT)

            self.loadTrackBtn.append(QPushButton("Load track"))

            self.grid.addWidget(self.trackNames[i], 2*(i+2), 0)
            self.grid.addWidget(self.trackTypeBox[i], 2*(i+2)+1, 0)
            self.grid.addWidget(self.loadTrackBtn[i], 2*(i+2), 1)

            #self.trackNames[i].setFixedHeight(45)
            #self.trackNames[i].setFixedWidth(100)
            #self.trackTypeBox[i].setFixedHeight(45)
            #self.trackTypeBox[i].setFixedWidth(100)
        
        #Button functions
        self.trackTypeBox[0].currentIndexChanged.connect(lambda: self.track_type_update(1))
        self.trackTypeBox[1].currentIndexChanged.connect(lambda: self.track_type_update(2))
        self.trackTypeBox[2].currentIndexChanged.connect(lambda: self.track_type_update(3))
        self.trackTypeBox[3].currentIndexChanged.connect(lambda: self.track_type_update(4))
        self.trackTypeBox[4].currentIndexChanged.connect(lambda: self.track_type_update(5))

        self.loadTrackBtn[0].clicked.connect(lambda: self.load_track(1))
        self.loadTrackBtn[1].clicked.connect(lambda: self.load_track(2))
        self.loadTrackBtn[2].clicked.connect(lambda: self.load_track(3))
        self.loadTrackBtn[3].clicked.connect(lambda: self.load_track(4))
        self.loadTrackBtn[4].clicked.connect(lambda: self.load_track(5))

        self.setLayout(self.grid) 
        #self.setGeometry(100, 300, 350, 300)
        self.setWindowTitle('Guitar Band')

    def track_type_update(self, i):
        print("za" + str(i))

    def load_track(self, i):
        fname, _ = QFileDialog.getOpenFileName(self, 'Open file', 'C:/PythonProject')
        self.trackList = mf.fileTrack(fname)
        print(i)

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

    def drag_slider(self):
        self.audioPointer = self.audioSlider.value()
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



if __name__ == '__main__':

    app = QApplication(sys.argv)
    s = mainScreen()
    s.show()
    sys.exit(app.exec_())