# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'gui.ui'
##
## Created by: Qt User Interface Compiler version 5.14.2
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide2.QtCore import (QCoreApplication, QDate, QDateTime, QMetaObject,
    QObject, QPoint, QRect, QSize, QTime, QUrl, Qt)
from PySide2.QtGui import (QBrush, QColor, QConicalGradient, QCursor, QFont,
    QFontDatabase, QIcon, QKeySequence, QLinearGradient, QPalette, QPainter,
    QPixmap, QRadialGradient)
from PySide2.QtWidgets import *


class Ui_SnakeGame(object):
    def setupUi(self, SnakeGame):
        self.board_labels = []
        for i in range(10):
            labels_row = []
            for j in range(16):
                label = QLabel(SnakeGame)
                label.setObjectName(u"board_label_{}_{}".format(i, j))
                label.setGeometry(QRect(60 + j*30, 630 + i*30, 30, 30))
                labels_row.append(label)
            self.board_labels.append(labels_row)

        if not SnakeGame.objectName():
            SnakeGame.setObjectName(u"SnakeGame")
        SnakeGame.resize(780, 1000)
        self.btn_pause = QPushButton(SnakeGame)
        self.btn_pause.setObjectName(u"btn_pause")
        self.btn_pause.setGeometry(QRect(610, 40, 151, 31))
        self.btn_restart = QPushButton(SnakeGame)
        self.btn_restart.setObjectName(u"btn_restart")
        self.btn_restart.setGeometry(QRect(610, 80, 151, 31))
        self.btn_exit = QPushButton(SnakeGame)
        self.btn_exit.setObjectName(u"btn_exit")
        self.btn_exit.setGeometry(QRect(610, 120, 151, 31))
        self.board_gBox = QGroupBox(SnakeGame)
        self.board_gBox.setObjectName(u"board_gBox")
        self.board_gBox.setGeometry(QRect(10, 10, 581, 601))
        self.board_text = QTextEdit(self.board_gBox)
        self.board_text.setObjectName(u"board_text")
        self.board_text.setGeometry(QRect(10, 10, 561, 581))
        self.board_text.setReadOnly(True)
        self.p1_gBox = QGroupBox(SnakeGame)
        self.p1_gBox.setObjectName(u"p1_gBox")
        self.p1_gBox.setGeometry(QRect(610, 290, 151, 131))
        self.p1_c_gBox = QGroupBox(self.p1_gBox)
        self.p1_c_gBox.setObjectName(u"p1_c_gBox")
        self.p1_c_gBox.setGeometry(QRect(10, 20, 120, 51))
        self.p1_controls_textbox = QLineEdit(self.p1_c_gBox)
        self.p1_controls_textbox.setObjectName(u"p1_controls_textbox")
        self.p1_controls_textbox.setGeometry(QRect(10, 20, 101, 21))
        self.p1_controls_textbox.setAlignment(Qt.AlignCenter)
        self.p1_controls_textbox.setReadOnly(True)
        self._p_gBox = QGroupBox(self.p1_gBox)
        self._p_gBox.setObjectName(u"_p_gBox")
        self._p_gBox.setGeometry(QRect(10, 70, 120, 51))
        self.p1_points_textbox = QLineEdit(self._p_gBox)
        self.p1_points_textbox.setObjectName(u"p1_points_textbox")
        self.p1_points_textbox.setGeometry(QRect(10, 20, 101, 20))
        self.p1_points_textbox.setAlignment(Qt.AlignLeading|Qt.AlignLeft|Qt.AlignVCenter)
        self.p1_points_textbox.setReadOnly(True)
        self.p2_gBox = QGroupBox(SnakeGame)
        self.p2_gBox.setObjectName(u"p2_gBox")
        self.p2_gBox.setGeometry(QRect(610, 440, 151, 131))
        self.p2_c_gBox = QGroupBox(self.p2_gBox)
        self.p2_c_gBox.setObjectName(u"p2_c_gBox")
        self.p2_c_gBox.setGeometry(QRect(10, 20, 120, 51))
        self.p2_controls_textbox = QLineEdit(self.p2_c_gBox)
        self.p2_controls_textbox.setObjectName(u"p2_controls_textbox")
        self.p2_controls_textbox.setGeometry(QRect(10, 20, 101, 21))
        self.p2_controls_textbox.setAlignment(Qt.AlignCenter)
        self.p2_controls_textbox.setReadOnly(True)
        self.p2_p_gBox = QGroupBox(self.p2_gBox)
        self.p2_p_gBox.setObjectName(u"p2_p_gBox")
        self.p2_p_gBox.setGeometry(QRect(10, 70, 120, 51))
        self.p2_points_textbox = QLineEdit(self.p2_p_gBox)
        self.p2_points_textbox.setObjectName(u"p2_points_textbox")
        self.p2_points_textbox.setGeometry(QRect(10, 20, 101, 21))
        self.p2_points_textbox.setAlignment(Qt.AlignLeading|Qt.AlignLeft|Qt.AlignVCenter)
        self.p2_points_textbox.setReadOnly(True)
        self.game_state_gBox = QGroupBox(SnakeGame)
        self.game_state_gBox.setObjectName(u"game_state_gBox")
        self.game_state_gBox.setGeometry(QRect(610, 170, 151, 81))
        self.game_state_textbox = QTextEdit(self.game_state_gBox)
        self.game_state_textbox.setObjectName(u"game_state_textbox")
        self.game_state_textbox.setGeometry(QRect(10, 20, 131, 51))
        self.game_state_textbox.setReadOnly(True)
        self.line = QFrame(SnakeGame)
        self.line.setObjectName(u"line")
        self.line.setGeometry(QRect(600, 260, 171, 31))
        self.line.setFrameShape(QFrame.HLine)
        self.line.setFrameShadow(QFrame.Sunken)
        self.line_2 = QFrame(SnakeGame)
        self.line_2.setObjectName(u"line_2")
        self.line_2.setGeometry(QRect(583, 10, 41, 601))
        self.line_2.setFrameShape(QFrame.VLine)
        self.line_2.setFrameShadow(QFrame.Sunken)

        self.retranslateUi(SnakeGame)

        QMetaObject.connectSlotsByName(SnakeGame)
    # setupUi

    def retranslateUi(self, SnakeGame):
        SnakeGame.setWindowTitle(QCoreApplication.translate("SnakeGame", u"Hex Snake Game", None))
        self.btn_pause.setText(QCoreApplication.translate("SnakeGame", u"Unpause game", None))
        self.btn_restart.setText(QCoreApplication.translate("SnakeGame", u"Restart game", None))
        self.btn_exit.setText(QCoreApplication.translate("SnakeGame", u"Exit game", None))
        self.board_gBox.setTitle("")
        self.p1_gBox.setTitle(QCoreApplication.translate("SnakeGame", u"Player 1", None))
        self.p1_c_gBox.setTitle(QCoreApplication.translate("SnakeGame", u"Controls", None))
        self.p1_controls_textbox.setText(QCoreApplication.translate("SnakeGame", u"q, w, e, a, s, d", None))
        self._p_gBox.setTitle(QCoreApplication.translate("SnakeGame", u"Points", None))
        self.p1_points_textbox.setText(QCoreApplication.translate("SnakeGame", u"0", None))
        self.p2_gBox.setTitle(QCoreApplication.translate("SnakeGame", u"Player 2", None))
        self.p2_c_gBox.setTitle(QCoreApplication.translate("SnakeGame", u"Controls", None))
        self.p2_controls_textbox.setText(QCoreApplication.translate("SnakeGame", u"u, i, o, j, k, l", None))
        self.p2_p_gBox.setTitle(QCoreApplication.translate("SnakeGame", u"Points", None))
        self.p2_points_textbox.setText(QCoreApplication.translate("SnakeGame", u"0", None))
        self.game_state_gBox.setTitle(QCoreApplication.translate("SnakeGame", u"Game state", None))
    # retranslateUi

