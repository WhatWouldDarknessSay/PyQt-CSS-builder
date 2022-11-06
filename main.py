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
        MainWindow.setFixedSize(650, 400)
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
        # border-style:
        self.borderstyle_frame = QtWidgets.QFrame(self.scrollAreaWidgetContents)
        self.borderstyle_frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.borderstyle_frame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.borderstyle_frame.setObjectName("borderstyle_frame")
        self.horizontalLayout_7 = QtWidgets.QHBoxLayout(self.borderstyle_frame)
        self.horizontalLayout_7.setObjectName("horizontalLayout_7")
        self.borderstyle_lbl = QtWidgets.QLabel(self.borderstyle_frame)
        self.borderstyle_lbl.setObjectName("borderstyle_lbl")
        self.horizontalLayout_7.addWidget(self.borderstyle_lbl)

        self.borderstyle_val = QtWidgets.QComboBox(self.borderstyle_frame)
        self.borderstyle_val.addItems(
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
        self.borderstyle_val.setObjectName("borderstyle_val")
        self.horizontalLayout_7.addWidget(self.borderstyle_val)
        self.verticalLayout.addWidget(self.borderstyle_frame)
        # border-width
        self.borderwidth_frame = QtWidgets.QFrame(self.scrollAreaWidgetContents)
        self.borderwidth_frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.borderwidth_frame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.borderwidth_frame.setObjectName("border_frame")
        self.horizontalLayout_8 = QtWidgets.QHBoxLayout(self.borderwidth_frame)
        self.horizontalLayout_8.setObjectName("horizontalLayout_8")
        self.borderwidth_lbl = QtWidgets.QLabel(self.borderwidth_frame)
        self.borderwidth_lbl.setObjectName("border_lbl")
        self.horizontalLayout_8.addWidget(self.borderwidth_lbl)
        self.borderwidth_val = QtWidgets.QSpinBox(self.borderwidth_frame)
        self.borderwidth_val.setObjectName("border_val")
        self.horizontalLayout_8.addWidget(self.borderwidth_val)
        self.verticalLayout.addWidget(self.borderwidth_frame)
        # border color
        self.bordercolor_frame = QtWidgets.QFrame(self.scrollAreaWidgetContents)
        self.bordercolor_frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.bordercolor_frame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.bordercolor_frame.setObjectName("bordercolor_frame")
        self.horizontalLayout_9 = QtWidgets.QHBoxLayout(self.bordercolor_frame)
        self.horizontalLayout_9.setObjectName("horizontalLayout_5")
        self.bordercolor_lbl = QtWidgets.QLabel(self.bordercolor_frame)
        self.bordercolor_lbl.setObjectName("bordercolor_lbl")
        self.horizontalLayout_9.addWidget(self.bordercolor_lbl)
        self.bordercolor_val = QtWidgets.QLineEdit(self.bordercolor_frame)
        self.bordercolor_val.setPlaceholderText("HEX")
        self.bordercolor_val.setText("#000000")
        self.bordercolor_val.setObjectName("bordercolor_val")
        self.horizontalLayout_9.addWidget(self.bordercolor_val)
        self.bordercolor_visualizer = QtWidgets.QPushButton(self.bordercolor_frame)
        self.bordercolor_visualizer.setFixedSize(20, 20)
        self.bordercolor_visualizer.move(10, 0)
        self.bordercolor_visualizer.setAutoFillBackground(True)
        self.bordercolor_visualizer.setStyleSheet(
            f"background-color: {self.bordercolor_val.text()};"
        )
        self.horizontalLayout_9.addWidget(self.bordercolor_visualizer)
        self.verticalLayout.addWidget(self.bordercolor_frame)
        # border-radius
        self.border_radius_frame = QtWidgets.QFrame(self.scrollAreaWidgetContents)
        self.border_radius_frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.border_radius_frame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.border_radius_frame.setObjectName("border_radius_frame")
        self.horizontalLayout_6 = QtWidgets.QHBoxLayout(self.border_radius_frame)
        self.horizontalLayout_6.setObjectName("horizontalLayout_6")
        self.border_radius_lbl = QtWidgets.QLabel(self.border_radius_frame)
        self.border_radius_lbl.setObjectName("border_radius_lbl")
        self.horizontalLayout_6.addWidget(self.border_radius_lbl)
        self.border_radius_val = QtWidgets.QSpinBox(self.border_radius_frame)
        self.border_radius_val.setObjectName("border_radius_val")
        self.horizontalLayout_6.addWidget(self.border_radius_val)
        self.verticalLayout.addWidget(self.border_radius_frame)
        # background-color
        self.backgroundcolor_frame = QtWidgets.QFrame(self.scrollAreaWidgetContents)
        self.backgroundcolor_frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.backgroundcolor_frame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.backgroundcolor_frame.setObjectName("backgroundcolor_frame")
        self.horizontalLayout_10 = QtWidgets.QHBoxLayout(self.backgroundcolor_frame)
        self.horizontalLayout_10.setObjectName("horizontalLayout_5")
        self.backgroundcolor_lbl = QtWidgets.QLabel(self.backgroundcolor_frame)
        self.backgroundcolor_lbl.setObjectName("backgroundcolor_lbl")
        self.horizontalLayout_10.addWidget(self.backgroundcolor_lbl)
        self.backgroundcolor_val = QtWidgets.QLineEdit(self.backgroundcolor_frame)
        self.backgroundcolor_val.setPlaceholderText("HEX")
        self.backgroundcolor_val.setText("#000000")
        self.backgroundcolor_val.setObjectName("backgroundcolor_val")
        self.horizontalLayout_10.addWidget(self.backgroundcolor_val)
        self.backgroundcolor_visualizer = QtWidgets.QPushButton(
            self.backgroundcolor_frame
        )
        self.backgroundcolor_visualizer.setFixedSize(20, 20)
        self.backgroundcolor_visualizer.move(10, 0)
        self.backgroundcolor_visualizer.setAutoFillBackground(True)
        self.backgroundcolor_visualizer.setStyleSheet(
            f"background-color: {self.backgroundcolor_val.text()};"
        )
        self.horizontalLayout_10.addWidget(self.backgroundcolor_visualizer)
        self.verticalLayout.addWidget(self.backgroundcolor_frame)
        # text color
        self.textcolor_frame = QtWidgets.QFrame(self.scrollAreaWidgetContents)
        self.textcolor_frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.textcolor_frame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.textcolor_frame.setObjectName("textcolor_frame")
        self.horizontalLayout_11 = QtWidgets.QHBoxLayout(self.textcolor_frame)
        self.horizontalLayout_11.setObjectName("horizontalLayout_5")
        self.textcolor_lbl = QtWidgets.QLabel(self.textcolor_frame)
        self.textcolor_lbl.setObjectName("textcolor_lbl")
        self.horizontalLayout_11.addWidget(self.textcolor_lbl)
        self.textcolor_val = QtWidgets.QLineEdit(self.textcolor_frame)
        self.textcolor_val.setPlaceholderText("HEX")
        self.textcolor_val.setText("#000000")
        self.textcolor_val.setObjectName("textcolor_val")
        self.horizontalLayout_11.addWidget(self.textcolor_val)
        self.textcolor_visualizer = QtWidgets.QPushButton(self.textcolor_frame)
        self.textcolor_visualizer.setFixedSize(20, 20)
        self.textcolor_visualizer.move(10, 0)
        self.textcolor_visualizer.setAutoFillBackground(True)
        self.textcolor_visualizer.setStyleSheet(f"color: {self.textcolor_val.text()};")
        self.horizontalLayout_11.addWidget(self.textcolor_visualizer)
        self.verticalLayout.addWidget(self.textcolor_frame)
        # other
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
        self.apply_btn.setText(_translate("MainWindow", "Apply"))
        self.outlinewidth_lbl.setText(_translate("MainWindow", "Outline width"))
        self.outlinestyle_lbl.setText(_translate("MainWindow", "Outline style"))
        self.outlinecolor_lbl.setText(_translate("MainWindow", "Outline color"))
        self.borderstyle_lbl.setText(_translate("MainWindow", "Border style"))
        self.borderwidth_lbl.setText(_translate("Mainwindow", "Border width"))
        self.bordercolor_lbl.setText(_translate("MainWindow", "Border color"))
        self.border_radius_lbl.setText(_translate("MainWindow", "Border radius"))
        self.backgroundcolor_lbl.setText(_translate("MainWindow", "Background color"))
        self.textcolor_lbl.setText(_translate("MainWindow", "Text color"))
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
        self.borderstyle_val.currentTextChanged.connect(self.change_border_style)
        self.border_radius_val.textChanged.connect(self.change_border_radius)
        self.borderwidth_val.textChanged.connect(self.change_border_width)
        self.bordercolor_val.textChanged.connect(self.change_border_color)
        self.bordercolor_visualizer.clicked.connect(lambda: self.color_event("border"))
        self.backgroundcolor_val.textChanged.connect(self.change_background_color)
        self.backgroundcolor_visualizer.clicked.connect(
            lambda: self.color_event("background")
        )
        self.textcolor_val.textChanged.connect(self.change_text_color)
        self.textcolor_visualizer.clicked.connect(lambda: self.color_event("text"))
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
        border_style = list(filter(lambda x: "border:" in x, self.current_css))
        if len(border_style) != 0:
            self.borderstyle_val.setCurrentText(border_style[0].split()[1][:-1])
        else:
            self.borderstyle_val.setCurrentText("solid")
        border_width = list(filter(lambda x: "border-width" in x, self.current_css))
        if len(border_width) != 0:
            self.borderwidth_val.setValue(int(border_width[0].split()[1][:-3]))
        else:
            self.borderwidth_val.setValue(0)
        border_color = list(filter(lambda x: "border-color:" in x, self.current_css))
        if len(border_color) != 0:
            self.bordercolor_val.setText(border_color[0].split()[1][:-1])
        else:
            self.bordercolor_val.setText("#000000")
        border_radius = list(filter(lambda x: "border-radius:" in x, self.current_css))
        if len(border_radius) != 0:
            self.border_radius_val.setValue(int(border_radius[0].split()[1][:-3]))
        else:
            self.border_radius_val.setValue(0)
        background_color = list(
            filter(lambda x: "background-color:" in x, self.current_css)
        )
        if len(background_color) != 0:
            self.backgroundcolor_val.setText(background_color[0].split()[1][:-1])
        else:
            self.backgroundcolor_val.setText("#ffffff")
        text_color = list(filter(lambda x: "color:" in x, self.current_css))
        if len(text_color) != 0:
            self.textcolor_val.setText(text_color[0].split()[1][:-1])
        else:
            self.textcolor_val.setText("#000000")

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

    def change_border_style(self):
        tmp_index = None
        for index, i in enumerate(self.current_css):
            if "border:" in i:
                tmp_index = index
        if tmp_index is None:
            self.current_css.append(f"border: {self.borderstyle_val.currentText()};")
        else:
            self.current_css[
                tmp_index
            ] = f"border: {self.borderstyle_val.currentText()};"
        print(self.current_css)

    def change_border_width(self):
        tmp_index = None
        for index, i in enumerate(self.current_css):
            if "border-width" in i:
                tmp_index = index
        if tmp_index is None:
            self.current_css.append(f"border-width: {self.borderwidth_val.value()}px;")
        else:
            self.current_css[
                tmp_index
            ] = f"border-width: {self.borderwidth_val.value()}px;"
        print(self.current_css)

    def change_border_color(self):
        tmp_index = None
        for index, i in enumerate(self.current_css):
            if "border-color" in i:
                tmp_index = index
        if tmp_index is None:
            self.current_css.append(f"border-color: {self.bordercolor_val.text()};")
        else:
            self.current_css[
                tmp_index
            ] = f"border-color: {self.bordercolor_val.text()};"
        self.bordercolor_visualizer.setStyleSheet(
            f"background-color: {self.bordercolor_val.text()}"
        )
        print(self.current_css)

    def change_border_radius(self):
        tmp_index = None
        for index, i in enumerate(self.current_css):
            if "border-radius:" in i:
                tmp_index = index
        if tmp_index is None:
            self.current_css.append(
                f"border-radius: {self.border_radius_val.value()}px;"
            )
        else:
            self.current_css[
                tmp_index
            ] = f"border-radius: {self.border_radius_val.value()}px;"
        print(self.current_css)

    def change_background_color(self):
        tmp_index = None
        for index, i in enumerate(self.current_css):
            if "background-color" in i:
                tmp_index = index
        if tmp_index is None:
            self.current_css.append(
                f"background-color: {self.backgroundcolor_val.text()};"
            )
        else:
            self.current_css[
                tmp_index
            ] = f"background-color: {self.backgroundcolor_val.text()};"
        self.backgroundcolor_visualizer.setStyleSheet(
            f"background-color: {self.backgroundcolor_val.text()}"
        )
        print(self.current_css)

    def change_text_color(self):
        tmp_index = None
        for index, i in enumerate(self.current_css):
            if "color" in i:
                tmp_index = index
        if tmp_index is None:
            self.current_css.append(f"color: {self.textcolor_val.text()};")
        else:
            self.current_css[tmp_index] = f"color: {self.textcolor_val.text()};"
        self.textcolor_visualizer.setStyleSheet(
            f"background-color: {self.textcolor_val.text()}"
        )
        print(self.current_css)

    def color_event(self, obj):
        color = QColorDialog.getColor().name()
        if obj == "outline":
            self.outlinecolor_val.setText(color)
        if obj == "border":
            self.bordercolor_val.setText(color)
        if obj == "background":
            self.backgroundcolor_val.setText(color)
        if obj == "text":
            self.textcolor_val.setText(color)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    ex = MyWidget()
    ex.show()
    sys.exit(app.exec_())
