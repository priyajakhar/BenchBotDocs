import sys
from PyQt6.QtWidgets import (QWidget, QPushButton, QApplication, QLabel)

class mainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        btnsr = QPushButton('START', self)
        btnsr.move(10, 10)
        #btnsr.resize(btnsr.sizeHint())
        btnsr.clicked.connect(start)
        
        l1 = QLabel("Movement", self)
        l1.move(30,50)
        
        l2 = QLabel("Speed", self)
        l2.move(40,80)
        
        l3 = QLabel("Distance (in mm)", self)
        l3.move(40,100)
        
        btn1 = QPushButton(' Forward ', self)
        btn1.move(50, 125)
        btn1.clicked.connect(fw)

        btn2 = QPushButton('Backward', self)
        btn2.move(50, 150)
        btn2.clicked.connect(bw)
        
        btnst = QPushButton('STOP', self)
        btnst.move(10, 200)
        btnst.clicked.connect(stop)
        
        qbtn = QPushButton('Quit', self)
        qbtn.clicked.connect(QApplication.instance().quit)
        qbtn.resize(qbtn.sizeHint())
        qbtn.move(330, 260)

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