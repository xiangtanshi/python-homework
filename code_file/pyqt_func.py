
import sys
from function import *
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import (QApplication, QFileDialog, QGridLayout,QLineEdit,
                             QLabel, QPushButton,QWidget)


class face_gui(QWidget):
  
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        #按键与文本栏设定
        self.resize(800, 600)
        self.detectbtn = QPushButton('face_detection', self)
        self.signbtn = QPushButton('sign', self)
        self.quitbtn = QPushButton('quit', self)
        self.label = QLabel()
        
        self.gender_ = QLabel("gender:",self)
        self.age_ = QLabel("age:",self)
        self.beauty_ = QLabel("beauty",self)
        self.signing_ = QLabel("who is coming:")


        # 布局设定
        layout = QGridLayout(self)
        layout.addWidget(self.label, 0, 1, 1, 1)
        layout.addWidget(self.signing_,3,1,1,1)   #3,1,1,1表示第3行第一列
        layout.addWidget(self.gender_,4,1,1,1)
        layout.addWidget(self.age_,5,1,1,1,)
        layout.addWidget(self.beauty_,6,1,1,1)
        layout.addWidget(self.detectbtn, 7, 1, 1, 1)
        layout.addWidget(self.signbtn, 7, 2, 1, 1)
        layout.addWidget(self.quitbtn, 7, 3, 1, 1)
        #添加文本栏
        self.genderedit = QLineEdit()
        layout.addWidget(self.genderedit,4,2,1,1)
        self.ageedit = QLineEdit()
        layout.addWidget(self.ageedit,5,2,1,1)
        self.beautyedit = QLineEdit()
        layout.addWidget(self.beautyedit,6,2,1,1)
        self.signingedit = QLineEdit()
        layout.addWidget(self.signingedit,3,2,1,1)


        #添加背景图片
        pixmap = QPixmap('group.jpg')
        self.label.setPixmap(pixmap)


        # 信号与槽连接
        self.detectbtn.clicked.connect(self.detectSlot)
        self.signbtn.clicked.connect(self.signSlot)
        self.quitbtn.clicked.connect(self.close)



    def detectSlot(self):
        # 调用打开文件diglog
        fileName, tmp = QFileDialog.getOpenFileName(
            self, 'Open Image', './__data', '*.png *.jpg *.bmp')

        if fileName is '':
            return
        #获取api返回信息
        global gender, age, beauty
        face_info = img_detect(fileName)
        gender = face_info[0]['type']
        age =str( face_info[1])
        beauty = str(face_info[2])
        #将结果展示在文本栏
        self.genderedit.setText(gender)
        self.ageedit.setText(age)
        self.beautyedit.setText(beauty)
        return


    def signSlot(self):
        # 调用存储文件dialog
        global people
        filename, tmp = QFileDialog.getOpenFileName(
            self, 'Open Image', './__data', '*.png *.jpg *.bmp')

        if filename is '':
            return

        people = img_search(filename)
        self.signingedit.setText(people)


if __name__ == '__main__':
    a = QApplication(sys.argv)
    w = face_gui()
    w.show()
    sys.exit(a.exec_())
