#!/usr/bin/env python

import sys

from PyQt5 import Qt
from PyQt5.uic import loadUi

# [ms]
TICK_TIME = 100

class StopWatch(Qt.QMainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.ui = loadUi("gui.ui", self)
        self.ui.reset.clicked.connect(self.do_reset)
        self.ui.start.clicked.connect(self.do_start)

        self.timer = Qt.QTimer()
        self.timer.setInterval(TICK_TIME)
        self.timer.timeout.connect(self.tick)

    def keyPressEvent(self, event):
        if event.key() == Qt.Qt.Key_Escape:
            self.close()
        else:
            super().keyPressEvent(event)

    @Qt.pyqtSlot()
    def tick(self):
        time = self.ui.sec.value() + self.ui.min.value() * 60
        time += TICK_TIME/1000
        self.ui.sec.display("%0.1f" % (time % 60))
        self.ui.min.display(time // 60)

    @Qt.pyqtSlot()
    def do_start(self):
        self.timer.start()
        self.ui.start.setText("Pause")
        self.ui.start.clicked.disconnect()
        self.ui.start.clicked.connect(self.do_pause)

    @Qt.pyqtSlot()
    def do_pause(self):
        self.timer.stop()
        self.ui.start.setText("Start")
        self.ui.start.clicked.disconnect()
        self.ui.start.clicked.connect(self.do_start)

    @Qt.pyqtSlot()
    def do_reset(self):
        self.ui.sec.display(0)
        self.ui.min.display(0)

app = Qt.QApplication(sys.argv)

watch = StopWatch()
watch.show()

app.exec_()
