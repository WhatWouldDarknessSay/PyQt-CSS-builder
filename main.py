import os
import sqlite3
import sys
import webbrowser

from PyQt5 import QtCore, QtGui, QtWebEngineWidgets, QtWidgets
from PyQt5.QtCore import QSize, Qt
from PyQt5.QtWidgets import QApplication, QColorDialog, QMainWindow


class PyQtDb:
    """ЭТО ВРЕМЕННОЕ РЕШЕНИЕ
    из=за того что sqlite не берет строки
    в которых имеются знаки " и \, я на время
    хранения их в бд, меняю по следующему принципу

    " -> ⋽
    \ -> ⋵

    """

    def __init__(self, table="authorization"):
        self.table = table

    def __iadd__(self, args):
        args = {str(i).replace('"', "⋽"): str(args[i]).replace('"', "⋽") for i in args}
        args = {
            str(i).replace("\\", "⋵"): str(args[i]).replace("\\", "⋵") for i in args
        }
        with sqlite3.connect("database.sqlite") as db:
            db.execute(
                f"""INSERT INTO {self.table} ("{'", "'.join([str(i) for i in args])}")
                 VALUES ("{'", "'.join([str(args[i]) for i in args])}");"""
            )
            db.commit()
        return self

    def select(self, take=None, where=None):
        if where:
            where = {
                str(i).replace('"', "⋽"): str(where[i]).replace('"', "⋽") for i in where
            }
            where = {
                str(i).replace("\\", "⋵"): str(where[i]).replace("\\", "⋵")
                for i in where
            }
        select_text = "SELECT"
        if take:
            select_text += f' {", ".join(take)}'
        else:
            select_text += " *"
        select_text += f" FROM {self.table}"
        if where:
            select_text += " WHERE " + " and ".join(
                [f'"{i}" = "{where[i]}"' for i in where]
            )
        select_text += ";"
        with sqlite3.connect("database.sqlite") as db:
            return db.execute(select_text)

    def update(self, upd, where=None):
        if where:
            where = {
                str(i).replace('"', "⋽"): str(where[i]).replace('"', "⋽") for i in where
            }
            where = {
                str(i).replace("\\", "⋵"): str(where[i]).replace("\\", "⋵")
                for i in where
            }
        upd = {
            i: upd[i].replace('"', "``") if type(upd[i]) is str else upd[i] for i in upd
        }
        with sqlite3.connect("database.sqlite") as db:
            if where:
                db.execute(
                    f"""UPDATE {self.table} SET {', '.join([f'"{i}" = "{upd[i]}"' for i in upd])} 
                    WHERE {' and '.join([f'{i} = "{where[i]}"' for i in where])};"""
                )
            else:
                db.execute(
                    f"""UPDATE {self.table} SET {', '.join([f'"{i}" = "{upd[i]}"' for i in upd])};"""
                )
            db.commit()


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("CSS Builder")
        MainWindow.setFixedSize(600, 400)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.centralwidget)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.webwidget = QtWidgets.QWidget(self.centralwidget)

        self.webwidget.setObjectName("webwidget")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.webwidget)
        self.verticalLayout_2.setObjectName("verticalLayout_2")

        self.webEngineView = QtWebEngineWidgets.QWebEngineView(self.webwidget)
        self.webEngineView.load(
            QtCore.QUrl().fromLocalFile(
                os.path.split(os.path.abspath(__file__))[0] + r"\index.html"
            )
        )
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
        self.horizontalLayout_4.setObjectName("horizontalLayout_4")
        self.outlinestyle_lbl = QtWidgets.QLabel(self.outlinestyle_frame)
        self.outlinestyle_lbl.setObjectName("oulinestyle_lbl")
        self.horizontalLayout_4.addWidget(self.outlinestyle_lbl)

        self.outlinestyle_val = QtWidgets.QComboBox(self.outlinestyle_frame)
        self.outlinestyle_val.addItems(
            [
                "dotted",
                "dashed",
                "solid",
                "double",
                "groove",
                "ridge",
                "inset",
                "outset",
                "none",
                "hidden",
            ]
        )
        self.outlinestyle_val.setObjectName("outlinestyle_val")
        self.horizontalLayout_4.addWidget(self.outlinestyle_val)
        self.verticalLayout.addWidget(self.outlinestyle_frame)
        # outline color
        self.outlinecolor_frame = QtWidgets.QFrame(self.scrollAreaWidgetContents)
        self.outlinecolor_frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.outlinecolor_frame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.outlinecolor_frame.setObjectName("outlinecolor_frame")
        self.horizontalLayout_5 = QtWidgets.QHBoxLayout(self.outlinecolor_frame)
        self.horizontalLayout_5.setObjectName("horizontalLayout_5")
        self.outlinecolor_lbl = QtWidgets.QLabel(self.outlinecolor_frame)
        self.outlinecolor_lbl.setObjectName("outlinecolor_lbl")
        self.horizontalLayout_5.addWidget(self.outlinecolor_lbl)
        self.outlinecolor_val = QtWidgets.QLineEdit(self.outlinecolor_frame)
        self.outlinecolor_val.setPlaceholderText("HEX")
        self.outlinecolor_val.setText("#000000")
        self.outlinecolor_val.setObjectName("outlinecolor_val")
        self.horizontalLayout_5.addWidget(self.outlinecolor_val)
        self.outlinecolor_visualizer = QtWidgets.QPushButton(self.outlinecolor_frame)
        self.outlinecolor_visualizer.setFixedSize(20, 20)
        self.outlinecolor_visualizer.move(10, 0)
        self.outlinecolor_visualizer.setAutoFillBackground(True)
        self.outlinecolor_visualizer.setStyleSheet(
            f"background-color: {self.outlinecolor_val.text()};"
        )
        self.horizontalLayout_5.addWidget(self.outlinecolor_visualizer)
        self.verticalLayout.addWidget(self.outlinecolor_frame)

        # self.outlinecolor_val = QtWidgets.QLineEdit(self.outlinecolor_frame)
        # self.outlinecolor_val.setPlaceholderText('HEX')
        # self.outlinecolor_val.setText('#000000')
        # self.horizontalLayout_5.addWidget(self.outlinecolor_val)

        #

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
        self.outlinecolor_lbl.setText(_translate("MainWindow", "Outline color"))
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
        with open("style.css", "r") as cssfile:
            self.current_css = cssfile.read()[8:-2].split("\n    ")
        print(self.current_css)
        # actions connect
        self.outlinestyle_val.currentTextChanged.connect(self.change_outline_style)
        self.outlinewidth_val.textChanged.connect(self.change_outline_width)
        self.apply_btn.clicked.connect(self.apply_action)
        self.outlinecolor_val.textChanged.connect(self.change_outline_color)
        self.outlinecolor_visualizer.clicked.connect(
            lambda: self.color_event("outline")
        )
        self.actionSave_Preset.triggered.connect(self.save_preset)
        self.actionLoad_Preset.triggered.connect(self.load_preset)
        self.actionCopy_Text.triggered.connect(self.copy_text)
        self.actionClear.triggered.connect(self.clear_css)
        self.actionGithub.triggered.connect(self.github_action)
        # setting values
        self.set_values()

    def set_values(self):
        outline_style = list(filter(lambda x: "outline:" in x, self.current_css))
        if len(outline_style) != 0:
            self.outlinestyle_val.setCurrentText(outline_style[0].split()[1][:-1])
        else:
            self.outlinestyle_val.setCurrentText("solid")
        outline_width = list(filter(lambda x: "outline-width" in x, self.current_css))
        if len(outline_width) != 0:
            self.outlinewidth_val.setValue(int(outline_width[0].split()[1][:-3]))
        else:
            self.outlinewidth_val.setValue(0)
        outline_color = list(filter(lambda x: "outline-color:" in x, self.current_css))
        if len(outline_color) != 0:
            self.outlinecolor_val.setText(outline_color[0].split()[1][:-1])
        else:
            self.outlinecolor_val.setText("#000000")

    def save_preset(self):
        name, ok_pressed = QtWidgets.QInputDialog.getText(
            self, "Save Preset", "Set preset name"
        )
        if ok_pressed:
            with open("style.css", "r") as file:
                db = PyQtDb("presets")
                db += {"name": name, "css_code": file.read()}

    def load_preset(self):
        db = PyQtDb("presets")
        name, ok_pressed = QtWidgets.QInputDialog.getItem(
            self,
            "Load Preset",
            "list of presets",
            list(map(lambda x: x[0], db.select(take=["name"]))),
            0,
            False,
        )
        if ok_pressed:
            with open("style.css", "w") as file:
                file.write(
                    list(db.select(take=["css_code"], where={"name": name}))[0][0]
                )
            with open("style.css", "r") as cssfile:
                self.current_css = cssfile.read()[8:-2].split("\n    ")
                self.set_values()

    def copy_text(self):
        cb = QtGui.QGuiApplication.clipboard()
        cb.clear(mode=cb.Clipboard)
        cb.setText(
            ".object{" + "\n    ".join(self.current_css) + "\n}", mode=cb.Clipboard
        )

    def github_action(self):
        webbrowser.open("https://github.com/WhatWouldDarknessSay/PyQt-CSS-builder")

    def clear_css(self):
        self.current_css = [
            "width: 100px;",
            "height: 50px;",
            "background-color: #727272;",
            "color: white;",
        ]
        self.apply_action()
        self.set_values()

    def apply_action(self):
        with open("style.css", "w") as file:
            file.write(".object{" + "\n    ".join(self.current_css) + "\n}")

        self.webEngineView.load(
            QtCore.QUrl().fromLocalFile(
                os.path.split(os.path.abspath(__file__))[0] + r"\index.html"
            )
        )

    def change_outline_color(self):
        tmp_index = None
        for index, i in enumerate(self.current_css):
            if "outline-color" in i:
                tmp_index = index
        if tmp_index is None:
            self.current_css.append(f"outline-color: {self.outlinecolor_val.text()};")
        else:
            self.current_css[
                tmp_index
            ] = f"outline-color: {self.outlinecolor_val.text()};"
        self.outlinecolor_visualizer.setStyleSheet(
            f"background-color: {self.outlinecolor_val.text()}"
        )
        print(self.current_css)

    def change_outline_width(self):
        tmp_index = None
        for index, i in enumerate(self.current_css):
            if "outline-width" in i:
                tmp_index = index
        if tmp_index is None:
            self.current_css.append(
                f"outline-width: {self.outlinewidth_val.value()}px;"
            )
        else:
            self.current_css[
                tmp_index
            ] = f"outline-width: {self.outlinewidth_val.value()}px;"
        print(self.current_css)

    def change_outline_style(self):
        tmp_index = None
        for index, i in enumerate(self.current_css):
            if "outline:" in i:
                tmp_index = index
        if tmp_index is None:
            self.current_css.append(f"outline: {self.outlinestyle_val.currentText()};")
        else:
            self.current_css[
                tmp_index
            ] = f"outline: {self.outlinestyle_val.currentText()};"
        print(self.current_css)

    def color_event(self, obj):
        color = QColorDialog.getColor().name()
        if obj == "outline":
            self.outlinecolor_val.setText(color)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    ex = MyWidget()
    ex.show()
    sys.exit(app.exec_())
