import sys
import cv2
from PyQt5 import QtCore, QtWidgets
from PyQt5.QtCore import QDir, Qt, QUrl, QThread, pyqtSignal, pyqtSlot
from PyQt5.QtGui import QImage, QPixmap
from PyQt5.QtWidgets import (QApplication, QFileDialog, QHBoxLayout, QLabel,
        QPushButton, QSizePolicy, QSlider, QStyle, QVBoxLayout, QWidget)

gl_position = 0
gl_fileName = ''
gl_state = False
gl_curr_frame_num = 0 
cap = []
ret = 0
frame = []
start_frames = []
end_frames = []
class Thread(QThread):
    changePixmap = pyqtSignal(QImage)

    def run(self):
        global gl_state, gl_curr_frame_num, cap, ret, frame
        cap = cv2.VideoCapture(gl_fileName)
        while True:
            if gl_state:
                gl_curr_frame_num = cap.get(cv2.CAP_PROP_POS_FRAMES)
                ret, frame = cap.read()
            if len(frame):
                rgbImage = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                h, w, ch = rgbImage.shape
                bytesPerLine = ch * w
                convertToQtFormat = QImage(rgbImage.data, w, h, bytesPerLine, QImage.Format_RGB888)
                p = convertToQtFormat.scaled(640, 480, Qt.KeepAspectRatio)
                self.changePixmap.emit(p)
                cv2.waitKey(100)

class cvDisp(QWidget):
    def __init__(self):
        super().__init__()
        self.title = 'Video frames viewer'
        self.left = 100
        self.top = 100
        self.width = 640
        self.height = 480
        
        self.initUI()
    
    @pyqtSlot(QImage)
    def setImage(self, image):
        self.label.setPixmap(QPixmap.fromImage(image))

    def initUI(self):
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)
        self.resize(640, 580)
        # create a label
        self.label = QLabel(self)
        self.label.resize(640, 480)
        fileB = QPushButton("File")
        fileB.clicked.connect(self.openFile)

        prev5Button = QPushButton("Prev5")
        prev5Button.clicked.connect(self.previous5Frame)

        prevButton = QPushButton("Prev")
        prevButton.clicked.connect(self.previousFrame)

        nextButton = QPushButton("Next")
        nextButton.clicked.connect(self.nextFrame)

        next5Button = QPushButton("Next5")
        next5Button.clicked.connect(self.next5Frame)

        startB = QPushButton("Start")
        startB.clicked.connect(self.startBProcess)

        endB = QPushButton("End")
        endB.clicked.connect(self.endBProcess)

        savecurrB = QPushButton("Save current frame")
        savecurrB.clicked.connect(self.savecurrBProcess)

        saveallB = QPushButton("Save all frames")
        saveallB.clicked.connect(self.saveallBProcess)

        self.startLabel = QLabel()
        self.startLabel.setGeometry(QtCore.QRect(self.startLabel.x(), self.startLabel.y(), 10, 20))
        self.endLabel = QLabel()
        self.endLabel.setGeometry(QtCore.QRect(self.endLabel.x(), self.endLabel.y(), 10, 20))
        
        self.playButton = QPushButton()
        self.playButton.setEnabled(False)
        self.playButton.setIcon(self.style().standardIcon(QStyle.SP_MediaPlay))
        self.playButton.clicked.connect(self.play)

        controlLayout = QHBoxLayout()
        controlLayout.setContentsMargins(0, 0, 0, 0)
        controlLayout.addWidget(prev5Button)        
        controlLayout.addWidget(prevButton)
        controlLayout.addWidget(self.playButton)
        controlLayout.addWidget(nextButton)
        controlLayout.addWidget(next5Button)   
        startLayout = QHBoxLayout()
        startLayout.addWidget(startB)
        startLayout.addWidget(self.startLabel)
        endLayout = QHBoxLayout()
        endLayout.addWidget(endB)
        endLayout.addWidget(self.endLabel)     

        layout = QVBoxLayout()
        layout.addWidget(fileB)
        layout.addWidget(self.label)
        layout.addLayout(controlLayout)
        layout.addLayout(startLayout)
        layout.addLayout(endLayout)
        layout.addWidget(saveallB)
        layout.addWidget(savecurrB)        
        self.setLayout(layout)


    
    def openFile(self):
        global gl_fileName, gl_state
        fileName, _ = QFileDialog.getOpenFileName(self, "Open file")
        gl_fileName = fileName

        if fileName != '':
            self.playButton.setEnabled(True)
            th = Thread(self)
            th.changePixmap.connect(self.setImage)
            th.start()
    
    def previousFrame(self):
        global cap,ret,frame, gl_curr_frame_num, gl_state
        gl_state = False
        cap.set(cv2.CAP_PROP_POS_FRAMES, gl_curr_frame_num - 1)
        gl_curr_frame_num = cap.get(cv2.CAP_PROP_POS_FRAMES)
        ret, frame = cap.read()

    def nextFrame(self):
        global cap,ret,frame, gl_curr_frame_num, gl_state
        gl_state = False
        cap.set(cv2.CAP_PROP_POS_FRAMES, gl_curr_frame_num + 1)
        gl_curr_frame_num = cap.get(cv2.CAP_PROP_POS_FRAMES)
        ret, frame = cap.read()


    def previous5Frame(self):
        global cap,ret,frame, gl_curr_frame_num, gl_state
        gl_state = False
        cap.set(cv2.CAP_PROP_POS_FRAMES, gl_curr_frame_num - 5)
        gl_curr_frame_num = cap.get(cv2.CAP_PROP_POS_FRAMES)
        ret, frame = cap.read()


    def next5Frame(self):
        global cap,ret,frame, gl_curr_frame_num, gl_state
        gl_state = False        
        cap.set(cv2.CAP_PROP_POS_FRAMES, gl_curr_frame_num + 5)
        gl_curr_frame_num = cap.get(cv2.CAP_PROP_POS_FRAMES)
        ret, frame = cap.read()


    def startBProcess(self):
        global start_frames, gl_curr_frame_num
        start_frames.append(gl_curr_frame_num)
        self.startLabel.setText(str(start_frames))
    
    def endBProcess(self):
        global end_frames, gl_curr_frame_num
        end_frames.append(gl_curr_frame_num)
        self.endLabel.setText(str(end_frames))

    def saveallBProcess(self):
        cap2 = cv2.VideoCapture(gl_fileName)
        index = 0
        while(cap2.isOpened()):
            ret, frame = cap.read()
            if ret:
                index = index + 1
                imName = 'gl_fileName'+str(index)+'.jpg'
                cv2.imwrite(imName, frame)

    def savecurrBProcess(self):
        global ret, frame, gl_curr_frame_num
        print('curr frame func')
        if ret:
            imName = str(gl_curr_frame_num) + '.png'
            cv2.imwrite(imName, frame)
        else:
            error_dialog = QtWidgets.QErrorMessage()
            error_dialog.showMessage('No file opened')

    def play(self):
        global gl_state
        if gl_state:
            gl_state = False
            self.playButton.setIcon(
                    self.style().standardIcon(QStyle.SP_MediaPlay))
        else:
            gl_state = True
            self.playButton.setIcon(
                    self.style().standardIcon(QStyle.SP_MediaPause))


if __name__ == '__main__':
    app = QApplication(sys.argv)
    guiFunc = cvDisp()
    guiFunc.show()
    sys.exit(app.exec_())