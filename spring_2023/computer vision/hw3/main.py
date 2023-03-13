import sys
import random
import argparse
import numpy
numpy.float = numpy.float64
numpy.int = numpy.int_

from PySide2 import QtCore, QtWidgets, QtGui
from skvideo.io import vread

from MotionDetector import MotionDetector

class QtDemo(QtWidgets.QWidget):
    def __init__(self, frames):
        super().__init__()

        self.frames = frames

        self.current_frame = 0

        self.button = QtWidgets.QPushButton("Next Frame")
        self.forward_button = QtWidgets.QPushButton("Forward 10 frames")
        self.backward_button = QtWidgets.QPushButton("Backward 10 frames")

        ########### MY CODE #############
        self.tracker = MotionDetector(frames)
        # self.tracker.test()
        self.current_frame = 2

        # Configure image label
        self.img_label = QtWidgets.QLabel(alignment=QtCore.Qt.AlignCenter)
        h, w, c = self.frames[2].shape
        if c == 1:
            img = QtGui.QImage(self.frames[2], w, h, QtGui.QImage.Format_Grayscale8)
        else:
            img = QtGui.QImage(self.frames[2], w, h, QtGui.QImage.Format_RGB888)
        self.img_label.setPixmap(QtGui.QPixmap.fromImage(img))

        # Configure slider
        self.frame_slider = QtWidgets.QSlider(QtCore.Qt.Orientation.Horizontal)
        self.frame_slider.setTickInterval(1)
        self.frame_slider.setMinimum(0)
        self.frame_slider.setMaximum(self.frames.shape[0]-1)

        self.layout = QtWidgets.QVBoxLayout(self)
        self.button_layout = QtWidgets.QHBoxLayout()
        self.button_layout.addWidget(self.backward_button)
        self.button_layout.addWidget(self.forward_button)
        self.layout.addWidget(self.img_label)
        self.layout.addLayout(self.button_layout)
        self.layout.addWidget(self.button)
        self.layout.addWidget(self.frame_slider)

        # Connect functions
        self.button.clicked.connect(self.on_click)
        self.frame_slider.sliderMoved.connect(self.on_move)
        self.forward_button.clicked.connect(self.forward_click)
        self.backward_button.clicked.connect(self.backward_click)
        

    @QtCore.Slot()
    def forward_click(self):
        if self.current_frame == self.frames.shape[0]-10:
            return
        
        self.current_frame +=10
        self.frame_slider.setValue(self.current_frame)
        if self.current_frame > self.tracker.last_frame_idx:
            self.tracker.update_tracking(self.current_frame)

        h, w, c = self.frames[self.current_frame].shape
        if c == 1:
            img = QtGui.QImage(self.frames[self.current_frame], w, h, QtGui.QImage.Format_Grayscale8)
        else:
            img = QtGui.QImage(self.frames[self.current_frame], w, h, QtGui.QImage.Format_RGB888)
        self.img_label.setPixmap(QtGui.QPixmap.fromImage(img))
    
    @QtCore.Slot()
    def backward_click(self):
        if self.current_frame < 10:
            return
        
        self.current_frame -=10
        self.frame_slider.setValue(self.current_frame)

        # should we call update when backward is click?????
        #self.tracker.update_tracking(self.current_frame)

        h, w, c = self.frames[self.current_frame].shape
        if c == 1:
            img = QtGui.QImage(self.frames[self.current_frame], w, h, QtGui.QImage.Format_Grayscale8)
        else:
            img = QtGui.QImage(self.frames[self.current_frame], w, h, QtGui.QImage.Format_RGB888)
        self.img_label.setPixmap(QtGui.QPixmap.fromImage(img))

    @QtCore.Slot()
    def on_click(self):
        if self.current_frame == self.frames.shape[0]-1:
            return
        
        self.current_frame += 1
        self.frame_slider.setValue(self.current_frame)
        if self.current_frame > self.tracker.last_frame_idx:
            self.tracker.update_tracking(self.current_frame)

        h, w, c = self.frames[self.current_frame].shape
        if c == 1:
            img = QtGui.QImage(self.frames[self.current_frame], w, h, QtGui.QImage.Format_Grayscale8)
        else:
            img = QtGui.QImage(self.frames[self.current_frame], w, h, QtGui.QImage.Format_RGB888)
        self.img_label.setPixmap(QtGui.QPixmap.fromImage(img))

    @QtCore.Slot()
    def on_move(self, pos):
        self.current_frame = pos
        self.tracker.update_tracking(self.current_frame)
        h, w, c = self.frames[self.current_frame].shape
        if c == 1:
            img = QtGui.QImage(self.frames[self.current_frame], w, h, QtGui.QImage.Format_Grayscale8)
        else:
            img = QtGui.QImage(self.frames[self.current_frame], w, h, QtGui.QImage.Format_RGB888)
        self.img_label.setPixmap(QtGui.QPixmap.fromImage(img))


if __name__ == "__main__":

    parser = argparse.ArgumentParser(description="Demo for loading video with Qt5.")
    parser.add_argument("video_path", metavar='PATH_TO_VIDEO', type=str)
    parser.add_argument("--num_frames", metavar='n', type=int, default=-1)
    parser.add_argument("--grey", metavar='True/False', type=str, default=False)
    args = parser.parse_args()

    #how many frames do want to load from the video
    num_frames = args.num_frames

    if num_frames > 0:
        frames = vread(args.video_path, num_frames=num_frames, as_grey=args.grey)
    else:
        frames = vread(args.video_path, as_grey=args.grey)

    app = QtWidgets.QApplication([])

    widget = QtDemo(frames)
    widget.resize(800, 600)
    widget.show()
    sys.exit(app.exec_())