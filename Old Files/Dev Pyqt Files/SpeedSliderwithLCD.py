import sys
from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import *

class mainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        btnsr = QPushButton('START', self)
        btnsr.clicked.connect(start)
        
        l1 = QLabel("Movement")
        l2 = QLabel("Speed")
        speed = QSlider(Qt.Orientation.Horizontal)
        sp = QLCDNumber(self)
        speed.valueChanged.connect(sp.display)
        l3 = QLabel("Distance (in cm)")
        distance = QLineEdit()
        
        btn1 = QPushButton(' Forward ')
        btn1.clicked.connect(fw)
        btn2 = QPushButton('Backward')
        btn2.clicked.connect(bw)
        
        btnst = QPushButton('STOP')
        btnst.clicked.connect(stop)
        
        qbtn = QPushButton('Quit')
        qbtn.clicked.connect(QApplication.instance().quit)
        qbtn.resize(qbtn.sizeHint())
        qbtn.move(330, 260)
        

        grid = QGridLayout()
        grid.setSpacing(10)

        grid.addWidget(btnsr, 0, 0)
        grid.addWidget(l1, 1, 1)
        grid.addWidget(l2, 2, 2)
        grid.addWidget(l3, 3, 2)
        grid.addWidget(speed, 2, 3)
        grid.addWidget(sp, 2, 4)
        grid.addWidget(distance, 3, 3)
        grid.addWidget(btn1, 4, 3)
        grid.addWidget(btn2, 5, 3)
        grid.addWidget(btnst, 6, 0)
        grid.addWidget(qbtn, 7, 4)

        self.setLayout(grid)
        
        self.setGeometry(100, 100, 400, 300)
        self.setWindowTitle('BenchBot')
        self.show()
        
def start():
    print("Started")

def stop():
    print("Stopped")
    
def fw():
    print("Go up")

def bw():
    print("Back up")    
    
def main():
    app = QApplication(sys.argv)
    win = mainWindow()
    sys.exit(app.exec())

if __name__ == '__main__':
    main()