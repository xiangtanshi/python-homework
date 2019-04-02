
import sys
from function import *
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import (QApplication, QFileDialog, QGridLayout,QLineEdit,
                             QLabel, QPushButton,QWidget)

gender = "male"
age = "20"
beauty = "50.0"
people = "harry"

class face_gui(QWidget):
    global gender,age,beauty,people
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        #按键与文本栏设定
        self.resize(800, 600)     #------特别要注意，如果屏幕太小，使用时将GUI界面放大为全屏显示，以免部分界面被遮住
        self.detectbtn = QPushButton('face_detection', self)
        self.signbtn = QPushButton('sign', self)
        self.quitbtn = QPushButton('quit', self)
        self.label_background = QLabel()         #背景图片
        self.label_background.setFixedSize(300, 200)#设置图片大小
        self.label_detect_picture = QLabel()            #要处理的图片
        self.label_detect_picture.setFixedSize(200, 150)
        self.label_sign_picture = QLabel()
        self.label_sign_picture.setFixedSize(200, 150)
        self.gender_ = QLabel("gender:",self)
        self.age_ = QLabel("age:",self)
        self.beauty_ = QLabel("beauty",self)
        self.signing_ = QLabel("who is coming:")


        # 布局设定
        layout = QGridLayout(self)
        layout.addWidget(self.label_background, 0, 2, 1, 1)  #放背景图片
        layout.addWidget(self.label_detect_picture,1,1,1,1)  #显示正在detect的图片
        layout.addWidget(self.gender_,3,1,1,1)        #性别
        layout.addWidget(self.age_,4,1,1,1,)          #年龄
        layout.addWidget(self.beauty_,5,1,1,1)        #颜值，最小0，最大100
        layout.addWidget(self.detectbtn, 6, 1, 1, 1)
        layout.addWidget(self.label_sign_picture, 7, 1, 1, 1)  #显示正在签到的图片
        layout.addWidget(self.signing_, 8, 1, 1, 1)   #签到
        layout.addWidget(self.signbtn,9,1,1,1)
        layout.addWidget(self.quitbtn, 10, 1, 1, 1)
        #添加文本栏
        self.genderedit = QLineEdit()
        layout.addWidget(self.genderedit,3,2,1,1)
        self.ageedit = QLineEdit()
        layout.addWidget(self.ageedit,4,2,1,1)
        self.beautyedit = QLineEdit()
        layout.addWidget(self.beautyedit,5,2,1,1)
        self.signingedit = QLineEdit()
        layout.addWidget(self.signingedit,8,2,1,1)



        pixmap = QPixmap('face.jpg').scaled(500,300)
        self.label_background.setPixmap(pixmap)


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
        #将目标图片显示
        pixmap_1 = QPixmap(fileName).scaled(200,150)
        self.label_detect_picture.setPixmap(pixmap_1)
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

        #将目标图片展示
        pixmap_2 = QPixmap(filename).scaled(200,150)
        self.label_sign_picture.setPixmap(pixmap_2)

        people = img_search(filename)
        self.signingedit.setText(people)


if __name__ == '__main__':
    a = QApplication(sys.argv)
    w = face_gui()
    w.show()
    sys.exit(a.exec_())
