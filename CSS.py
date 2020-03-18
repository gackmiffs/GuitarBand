from numpy.random import randint

MAIN_WINDOW_STYLE = "QWidget {background-color: rgb(128, 150, 150)}"

SETTING_WINDOW_STYLE = "QGroupBox {background-color: rgb(150, 192, 192); \
                                    max-width: 300px;}"

BUTTON_STYLE_1 = "QPushButton {background-color: rgb(0, 230, 180); \
                                border-style: outset; \
                                border-width: 2px; \
                                border-radius: 10px; \
                                border-color: beige; \
                                padding: 6px; \
                                font: bold 14px;}"

RANDOM_BUTTON = "QPushButton {background-color: rgb(0, %d, %d); \
                                max-width: 100px;}" % (randint(50, 150), randint(100, 255))

RANDOM_COMBO_BOX = "QComboBox {background-color: rgb(0, %d, %d); \
                                max-width: 100px;}" % (randint(50, 150), randint(100, 255))

TITLE_STYLE = "QLabel {font-weight: bold; \
                        font-style: italic; \
                        font-size: 36px; \
                        font-family: Impact; \
                        max-width: 300px;}"

LABEL_STYLE_1 = "QLabel {border-style: solid; \
                            border-width: 1px; \
                            font-size: 10px; \
                            font-weight: bold; \
                            max-width: 30px; \
                            max-height: 30px;\
                            text-align: center;}"

LABEL_STYLE_2 = "QLabel {font-size: 12px bold;}"

CHECKBOX_STYLE = "QCheckBox {spacing: 5px; \
                    max-width: 30px; \
                    max-height: 30px;\
                    } \
                    QCheckBox::indicator:unchecked { \
                        background-color: rgb(96, 96, 96); \
                    } \
                    QCheckBox::indicator:checked { \
                        background-color: rgb(0, 200, 200); \
                    }"

FONT_STYLE_1 = "QLabel {font-size: 14.5em}"