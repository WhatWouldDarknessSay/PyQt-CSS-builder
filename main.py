from PyQt5 import QtCore, QtGui, QtWidgets, QtWebEngineWidgets
import sys
from PyQt5.QtWidgets import QApplication, QMainWindow
from math import sqrt, factorial
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import Qt, QSize
import os


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("CSS Builder")
        MainWindow.resize(600, 400)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.centralwidget)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.webwidget = QtWidgets.QWidget(self.centralwidget)

        self.webwidget.setObjectName("webwidget")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.webwidget)
        self.verticalLayout_2.setObjectName("verticalLayout_2")

        self.webEngineView = QtWebEngineWidgets.QWebEngineView(self.webwidget)
        self.webEngineView.load(QtCore.QUrl().fromLocalFile(os.path.split(os.path.abspath(__file__))[0]+r'\index.html'))
        self.webEngineView.setFixedWidth(350)
        self.webEngineView.setFixedHeight(350)
        self.verticalLayout_2.addWidget(self.webEngineView)

        self.apply_btn = QtWidgets.QPushButton(self.webwidget)
        self.apply_btn.setObjectName("apply_btn")
        self.verticalLayout_2.addWidget(self.apply_btn)
        self.horizontalLayout.addWidget(self.webwidget)
        self.scrollArea = QtWidgets.QScrollArea(self.centralwidget)
        self.scrollArea.setWidgetResizable(True)
        self.scrollArea.setObjectName("scrollArea")
        self.scrollAreaWidgetContents = QtWidgets.QWidget()
        self.scrollAreaWidgetContents.setGeometry(QtCore.QRect(0, 0, 213, 244))
        self.scrollAreaWidgetContents.setObjectName("scrollAreaWidgetContents")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.scrollAreaWidgetContents)
        self.verticalLayout.setObjectName("verticalLayout")
        # outline width
        self.outlinewidth_frame = QtWidgets.QFrame(self.scrollAreaWidgetContents)
        self.outlinewidth_frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.outlinewidth_frame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.outlinewidth_frame.setObjectName("outline_frame")
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout(self.outlinewidth_frame)
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.outlinewidth_lbl = QtWidgets.QLabel(self.outlinewidth_frame)
        self.outlinewidth_lbl.setObjectName("ouline_lbl")
        self.horizontalLayout_3.addWidget(self.outlinewidth_lbl)
        self.outlinewidth_val = QtWidgets.QSpinBox(self.outlinewidth_frame)
        self.outlinewidth_val.setObjectName("outline_val")
        self.horizontalLayout_3.addWidget(self.outlinewidth_val)
        self.verticalLayout.addWidget(self.outlinewidth_frame)
        # outline style
        self.outlinestyle_frame = QtWidgets.QFrame(self.scrollAreaWidgetContents)
        self.outlinestyle_frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.outlinestyle_frame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.outlinestyle_frame.setObjectName("outline_frame")
        self.horizontalLayout_4 = QtWidgets.QHBoxLayout(self.outlinestyle_frame)
        self.horizontalLayout_4.setObjectName('horizontalLayout_4')
        self.outlinestyle_lbl = QtWidgets.QLabel(self.outlinestyle_frame)
        self.outlinestyle_lbl.setObjectName("oulinestyle_lbl")
        self.horizontalLayout_4.addWidget(self.outlinestyle_lbl)

        self.outlinestyle_val = QtWidgets.QComboBox(self.outlinestyle_frame)
        self.outlinestyle_val.addItems(['dotted', 'dashed', 'solid', 'double', 'groove', 'ridge', 'inset', 'outset', 'none', 'hidden'])
        self.outlinestyle_val.setObjectName("outlinestyle_val")
        self.horizontalLayout_4.addWidget(self.outlinestyle_val)
        self.verticalLayout.addWidget(self.outlinestyle_frame)

        self.scrollArea.setWidget(self.scrollAreaWidgetContents)
        self.horizontalLayout.addWidget(self.scrollArea)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 513, 21))
        self.menubar.setObjectName("menubar")
        self.menuFile = QtWidgets.QMenu(self.menubar)
        self.menuFile.setObjectName("menuFile")
        self.menuAbout = QtWidgets.QMenu(self.menubar)
        self.menuAbout.setObjectName("menuAbout")
        self.menuCSS = QtWidgets.QMenu(self.menubar)
        self.menuCSS.setObjectName("menuCSS")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)
        self.actionSave_Preset = QtWidgets.QAction(MainWindow)
        self.actionSave_Preset.setObjectName("actionSave_Preset")
        self.actionLoad_Preset = QtWidgets.QAction(MainWindow)
        self.actionLoad_Preset.setObjectName("actionLoad_Preset")
        self.actionGithub = QtWidgets.QAction(MainWindow)
        self.actionGithub.setObjectName("actionGithub")
        self.actionCopy_Text = QtWidgets.QAction(MainWindow)
        self.actionCopy_Text.setObjectName("actionCopy_Text")
        self.actionClear = QtWidgets.QAction(MainWindow)
        self.actionClear.setObjectName("actionClear")
        self.menuFile.addAction(self.actionSave_Preset)
        self.menuFile.addAction(self.actionLoad_Preset)
        self.menuAbout.addAction(self.actionGithub)
        self.menuCSS.addAction(self.actionCopy_Text)
        self.menuCSS.addAction(self.actionClear)
        self.menubar.addAction(self.menuFile.menuAction())
        self.menubar.addAction(self.menuCSS.menuAction())
        self.menubar.addAction(self.menuAbout.menuAction())

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.apply_btn.setText(_translate("MainWindow", "Применить"))
        self.outlinewidth_lbl.setText(_translate("MainWindow", "Outline width"))
        self.outlinestyle_lbl.setText(_translate("MainWindow", "Outline style"))
        self.menuFile.setTitle(_translate("MainWindow", "File"))
        self.menuAbout.setTitle(_translate("MainWindow", "About"))
        self.menuCSS.setTitle(_translate("MainWindow", "CSS"))
        self.actionSave_Preset.setText(_translate("MainWindow", "Save Preset"))
        self.actionLoad_Preset.setText(_translate("MainWindow", "Load Preset"))
        self.actionGithub.setText(_translate("MainWindow", "Github"))
        self.actionCopy_Text.setText(_translate("MainWindow", "Copy Text"))
        self.actionClear.setText(_translate("MainWindow", "Clear"))


class MyWidget(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        with open('style.css', 'r') as cssfile:
            self.current_css = cssfile.read()[8:-2].split('\n    ')
        print(self.current_css)

        self.outlinestyle_val.currentTextChanged.connect(self.change_outline_style)
        self.outlinewidth_val.textChanged.connect(self.change_outline_width)
        self.apply_btn.clicked.connect(self.apply_action)
    
    def apply_action(self):
        with open('style.css', 'w') as file:
            file.write('.object{' + '\n    '.join(self.current_css) + '\n}')
            
        self.webEngineView.load(QtCore.QUrl().fromLocalFile(os.path.split(os.path.abspath(__file__))[0]+r'\index.html'))
        
    
    def change_outline_width(self):
        tmp_index = None
        for index, i in enumerate(self.current_css):
            if 'outline-width' in i:
                tmp_index = index
        if tmp_index is None:
            self.current_css.append(f'outline-width: {self.outlinewidth_val.value()}px;')  
        else:
            self.current_css[tmp_index] = f'outline-width: {self.outlinewidth_val.value()}px;'
        print(self.current_css)
    
    def change_outline_style(self):
        tmp_index = None
        for index, i in enumerate(self.current_css):
            if 'outline:' in i:
                tmp_index = index
        if tmp_index is None:
            self.current_css.append(f'outline: {self.outlinestyle_val.currentText()};')  
        else:
            self.current_css[tmp_index] = f'outline: {self.outlinestyle_val.currentText()};'
        print(self.current_css)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    ex = MyWidget()
    ex.show()
    sys.exit(app.exec_())