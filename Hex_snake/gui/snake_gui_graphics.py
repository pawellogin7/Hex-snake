# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'gui_graphics.ui'
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
        if not SnakeGame.objectName():
            SnakeGame.setObjectName(u"SnakeGame")
        SnakeGame.resize(998, 772)
        self.board_gBox = QGroupBox(SnakeGame)
        self.board_gBox.setObjectName(u"board_gBox")
        self.board_gBox.setGeometry(QRect(10, 10, 731, 731))
        self.gView_board = QGraphicsView(self.board_gBox)
        self.gView_board.setObjectName(u"gView_board")
        self.gView_board.setGeometry(QRect(10, 10, 711, 711))
        self.p1_gBox = QGroupBox(SnakeGame)
        self.p1_gBox.setObjectName(u"p1_gBox")
        self.p1_gBox.setGeometry(QRect(770, 290, 101, 131))
        self.p1_c_gBox = QGroupBox(self.p1_gBox)
        self.p1_c_gBox.setObjectName(u"p1_c_gBox")
        self.p1_c_gBox.setGeometry(QRect(0, 20, 101, 51))
        self.p1_controls_textbox = QLineEdit(self.p1_c_gBox)
        self.p1_controls_textbox.setObjectName(u"p1_controls_textbox")
        self.p1_controls_textbox.setGeometry(QRect(10, 20, 81, 21))
        self.p1_controls_textbox.setAlignment(Qt.AlignCenter)
        self.p1_controls_textbox.setReadOnly(True)
        self._p_gBox = QGroupBox(self.p1_gBox)
        self._p_gBox.setObjectName(u"_p_gBox")
        self._p_gBox.setGeometry(QRect(0, 70, 101, 51))
        self.p1_points_textbox = QLineEdit(self._p_gBox)
        self.p1_points_textbox.setObjectName(u"p1_points_textbox")
        self.p1_points_textbox.setGeometry(QRect(10, 20, 81, 20))
        self.p1_points_textbox.setAlignment(Qt.AlignLeading|Qt.AlignLeft|Qt.AlignVCenter)
        self.p1_points_textbox.setReadOnly(True)
        self.p2_gBox = QGroupBox(SnakeGame)
        self.p2_gBox.setObjectName(u"p2_gBox")
        self.p2_gBox.setGeometry(QRect(870, 290, 101, 131))
        self.p2_c_gBox = QGroupBox(self.p2_gBox)
        self.p2_c_gBox.setObjectName(u"p2_c_gBox")
        self.p2_c_gBox.setGeometry(QRect(0, 20, 101, 51))
        self.p2_controls_textbox = QLineEdit(self.p2_c_gBox)
        self.p2_controls_textbox.setObjectName(u"p2_controls_textbox")
        self.p2_controls_textbox.setGeometry(QRect(10, 20, 81, 21))
        self.p2_controls_textbox.setAlignment(Qt.AlignCenter)
        self.p2_controls_textbox.setReadOnly(True)
        self.p2_p_gBox = QGroupBox(self.p2_gBox)
        self.p2_p_gBox.setObjectName(u"p2_p_gBox")
        self.p2_p_gBox.setGeometry(QRect(0, 70, 101, 51))
        self.p2_points_textbox = QLineEdit(self.p2_p_gBox)
        self.p2_points_textbox.setObjectName(u"p2_points_textbox")
        self.p2_points_textbox.setGeometry(QRect(10, 20, 81, 21))
        self.p2_points_textbox.setAlignment(Qt.AlignLeading|Qt.AlignLeft|Qt.AlignVCenter)
        self.p2_points_textbox.setReadOnly(True)
        self.game_state_gBox = QGroupBox(SnakeGame)
        self.game_state_gBox.setObjectName(u"game_state_gBox")
        self.game_state_gBox.setGeometry(QRect(770, 200, 201, 91))
        self.game_state_textbox = QTextEdit(self.game_state_gBox)
        self.game_state_textbox.setObjectName(u"game_state_textbox")
        self.game_state_textbox.setGeometry(QRect(10, 20, 181, 61))
        self.game_state_textbox.setReadOnly(True)
        self.line = QFrame(SnakeGame)
        self.line.setObjectName(u"line")
        self.line.setGeometry(QRect(760, 410, 221, 31))
        self.line.setFrameShape(QFrame.HLine)
        self.line.setFrameShadow(QFrame.Sunken)
        self.line_2 = QFrame(SnakeGame)
        self.line_2.setObjectName(u"line_2")
        self.line_2.setGeometry(QRect(740, 20, 41, 721))
        self.line_2.setFrameShape(QFrame.VLine)
        self.line_2.setFrameShadow(QFrame.Sunken)
        self.groupBox_3 = QGroupBox(SnakeGame)
        self.groupBox_3.setObjectName(u"groupBox_3")
        self.groupBox_3.setGeometry(QRect(770, 120, 191, 61))
        self.combo_game_type = QComboBox(self.groupBox_3)
        self.combo_game_type.addItem("")
        self.combo_game_type.addItem("")
        self.combo_game_type.addItem("")
        self.combo_game_type.addItem("")
        self.combo_game_type.setObjectName(u"combo_game_type")
        self.combo_game_type.setGeometry(QRect(10, 20, 171, 31))
        self.groupBox_4 = QGroupBox(SnakeGame)
        self.groupBox_4.setObjectName(u"groupBox_4")
        self.groupBox_4.setGeometry(QRect(770, 10, 201, 101))
        self.btn_pause = QPushButton(self.groupBox_4)
        self.btn_pause.setObjectName(u"btn_pause")
        self.btn_pause.setGeometry(QRect(10, 20, 91, 31))
        self.btn_restart = QPushButton(self.groupBox_4)
        self.btn_restart.setObjectName(u"btn_restart")
        self.btn_restart.setGeometry(QRect(110, 20, 81, 31))
        self.btn_exit = QPushButton(self.groupBox_4)
        self.btn_exit.setObjectName(u"btn_exit")
        self.btn_exit.setGeometry(QRect(10, 60, 181, 31))
        self.line_4 = QFrame(SnakeGame)
        self.line_4.setObjectName(u"line_4")
        self.line_4.setGeometry(QRect(760, 180, 221, 31))
        self.line_4.setFrameShape(QFrame.HLine)
        self.line_4.setFrameShadow(QFrame.Sunken)
        self.line_5 = QFrame(SnakeGame)
        self.line_5.setObjectName(u"line_5")
        self.line_5.setGeometry(QRect(760, 480, 221, 31))
        self.line_5.setFrameShape(QFrame.HLine)
        self.line_5.setFrameShadow(QFrame.Sunken)
        self.groupBox = QGroupBox(SnakeGame)
        self.groupBox.setObjectName(u"groupBox")
        self.groupBox.setGeometry(QRect(770, 500, 191, 241))
        self.conn_gBox = QGroupBox(self.groupBox)
        self.conn_gBox.setObjectName(u"conn_gBox")
        self.conn_gBox.setGeometry(QRect(10, 20, 171, 131))
        self.ip_gBox = QGroupBox(self.conn_gBox)
        self.ip_gBox.setObjectName(u"ip_gBox")
        self.ip_gBox.setGeometry(QRect(10, 20, 151, 51))
        self.ip_textbox = QLineEdit(self.ip_gBox)
        self.ip_textbox.setObjectName(u"ip_textbox")
        self.ip_textbox.setGeometry(QRect(10, 20, 131, 21))
        self.port_gBox = QGroupBox(self.conn_gBox)
        self.port_gBox.setObjectName(u"port_gBox")
        self.port_gBox.setGeometry(QRect(10, 70, 151, 51))
        self.port_textbox = QLineEdit(self.port_gBox)
        self.port_textbox.setObjectName(u"port_textbox")
        self.port_textbox.setGeometry(QRect(10, 20, 131, 21))
        self.combo_online = QComboBox(self.groupBox)
        self.combo_online.addItem("")
        self.combo_online.addItem("")
        self.combo_online.setObjectName(u"combo_online")
        self.combo_online.setGeometry(QRect(10, 210, 61, 22))
        self.btn_connect = QPushButton(self.groupBox)
        self.btn_connect.setObjectName(u"btn_connect")
        self.btn_connect.setGeometry(QRect(80, 210, 101, 23))
        self.groupBox_2 = QGroupBox(self.groupBox)
        self.groupBox_2.setObjectName(u"groupBox_2")
        self.groupBox_2.setGeometry(QRect(10, 150, 171, 51))
        self.conn_status_textbox = QLineEdit(self.groupBox_2)
        self.conn_status_textbox.setObjectName(u"conn_status_textbox")
        self.conn_status_textbox.setGeometry(QRect(10, 20, 151, 20))
        self.conn_status_textbox.setAlignment(Qt.AlignCenter)
        self.conn_status_textbox.setReadOnly(True)
        self.groupBox_5 = QGroupBox(SnakeGame)
        self.groupBox_5.setObjectName(u"groupBox_5")
        self.groupBox_5.setGeometry(QRect(770, 430, 201, 61))
        self.save_replay_btn = QPushButton(self.groupBox_5)
        self.save_replay_btn.setObjectName(u"save_replay_btn")
        self.save_replay_btn.setGeometry(QRect(10, 20, 91, 31))
        self.load_replay_btn = QPushButton(self.groupBox_5)
        self.load_replay_btn.setObjectName(u"load_replay_btn")
        self.load_replay_btn.setGeometry(QRect(110, 20, 81, 31))

        self.retranslateUi(SnakeGame)

        QMetaObject.connectSlotsByName(SnakeGame)
    # setupUi

    def retranslateUi(self, SnakeGame):
        SnakeGame.setWindowTitle(QCoreApplication.translate("SnakeGame", u"Hex Snake Game", None))
        self.board_gBox.setTitle("")
        self.p1_gBox.setTitle(QCoreApplication.translate("SnakeGame", u"Player 1", None))
        self.p1_c_gBox.setTitle(QCoreApplication.translate("SnakeGame", u"Controls", None))
        self.p1_controls_textbox.setText(QCoreApplication.translate("SnakeGame", u"q, w, e, a, s, d", None))
        self._p_gBox.setTitle(QCoreApplication.translate("SnakeGame", u"Points", None))
        self.p1_points_textbox.setText(QCoreApplication.translate("SnakeGame", u"0", None))
        self.p2_gBox.setTitle(QCoreApplication.translate("SnakeGame", u"Player 2", None))
        self.p2_c_gBox.setTitle(QCoreApplication.translate("SnakeGame", u"Controls (Local)", None))
        self.p2_controls_textbox.setText(QCoreApplication.translate("SnakeGame", u"u, i, o, j, k, l", None))
        self.p2_p_gBox.setTitle(QCoreApplication.translate("SnakeGame", u"Points", None))
        self.p2_points_textbox.setText(QCoreApplication.translate("SnakeGame", u"0", None))
        self.game_state_gBox.setTitle(QCoreApplication.translate("SnakeGame", u"Game state", None))
        self.groupBox_3.setTitle(QCoreApplication.translate("SnakeGame", u"Game type", None))
        self.combo_game_type.setItemText(0, QCoreApplication.translate("SnakeGame", u"Local multilplayer", None))
        self.combo_game_type.setItemText(1, QCoreApplication.translate("SnakeGame", u"Singleplayer with bot", None))
        self.combo_game_type.setItemText(2, QCoreApplication.translate("SnakeGame", u"Online multiplayer", None))
        self.combo_game_type.setItemText(3, QCoreApplication.translate("SnakeGame", u"Replay player", None))

        self.groupBox_4.setTitle(QCoreApplication.translate("SnakeGame", u"Game options", None))
        self.btn_pause.setText(QCoreApplication.translate("SnakeGame", u"Unpause game", None))
        self.btn_restart.setText(QCoreApplication.translate("SnakeGame", u"Restart game", None))
        self.btn_exit.setText(QCoreApplication.translate("SnakeGame", u"Exit game", None))
        self.groupBox.setTitle(QCoreApplication.translate("SnakeGame", u"TCP Multiplayer options", None))
        self.conn_gBox.setTitle(QCoreApplication.translate("SnakeGame", u"Connection parameters", None))
        self.ip_gBox.setTitle(QCoreApplication.translate("SnakeGame", u"IP", None))
        self.ip_textbox.setText(QCoreApplication.translate("SnakeGame", u"localhost", None))
        self.ip_textbox.setPlaceholderText(QCoreApplication.translate("SnakeGame", u"IP address", None))
        self.port_gBox.setTitle(QCoreApplication.translate("SnakeGame", u"Port", None))
        self.port_textbox.setText(QCoreApplication.translate("SnakeGame", u"6000", None))
        self.port_textbox.setPlaceholderText(QCoreApplication.translate("SnakeGame", u"port", None))
        self.combo_online.setItemText(0, QCoreApplication.translate("SnakeGame", u"Host", None))
        self.combo_online.setItemText(1, QCoreApplication.translate("SnakeGame", u"Join", None))

        self.btn_connect.setText(QCoreApplication.translate("SnakeGame", u"Start server", None))
        self.groupBox_2.setTitle(QCoreApplication.translate("SnakeGame", u"Connection status", None))
        self.conn_status_textbox.setText(QCoreApplication.translate("SnakeGame", u"Not connected", None))
        self.groupBox_5.setTitle(QCoreApplication.translate("SnakeGame", u"Replay options", None))
        self.save_replay_btn.setText(QCoreApplication.translate("SnakeGame", u"Save last replay", None))
        self.load_replay_btn.setText(QCoreApplication.translate("SnakeGame", u"Load replay", None))
    # retranslateUi
