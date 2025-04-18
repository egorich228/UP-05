from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtMultimedia import QMediaPlayer, QMediaContent, QMediaPlaylist
from PyQt5.QtCore import QUrl
import json
import os


class MusicManager:
    def __init__(self, music_file):
        self.music_file = music_file
        self.playlist = QMediaPlaylist()
        self.playlist.addMedia(QMediaContent(QUrl.fromLocalFile(self.music_file)))
        self.playlist.setPlaybackMode(QMediaPlaylist.Loop)

        self.mediaPlayer = QMediaPlayer()
        self.mediaPlayer.setPlaylist(self.playlist)
        self.mediaPlayer.setVolume(50)
        self.is_playing = False
        self.listeners = []

    def add_listener(self, listener):
        self.listeners.append(listener)

    def toggle_music(self):
        if self.is_playing:
            self.pause()
        else:
            self.play()
        self.update_listeners()

    def play(self):
        self.mediaPlayer.play()
        self.is_playing = True
        self.update_listeners()

    def pause(self):
        self.mediaPlayer.pause()
        self.is_playing = False
        self.update_listeners()

    def set_volume(self, volume):
        self.mediaPlayer.setVolume(volume)

    def update_listeners(self):
        for listener in self.listeners:
            listener.update_music_button(self.is_playing)


class RecordsManager:
    @staticmethod
    def save_record(nickname, total_time):
        """Сохраняет рекорд и возвращает обновленный список"""
        records = RecordsManager.load_records()
        records.append({"nickname": nickname, "time": total_time})
        records.sort(key=lambda x: x["time"])
        records = records[:10]

        with open('records.json', 'w', encoding='utf-8') as f:
            json.dump(records, f, ensure_ascii=False, indent=4)

        return records

    @staticmethod
    def load_records():
        """Загружает рекорды из файла"""
        if not os.path.exists('records.json'):
            return []

        with open('records.json', 'r', encoding='utf-8') as f:
            try:
                return json.load(f)
            except json.JSONDecodeError:
                return []


class RecordsWindow(QtWidgets.QMainWindow):
    def __init__(self, parent=None, music_manager=None):
        super().__init__(parent)
        self.music_manager = music_manager
        if music_manager:
            music_manager.add_listener(self)
        self.setupUi()

    def setupUi(self):
        self.setObjectName("RecordsWindow")
        self.setFixedSize(701, 738)  # Фиксированный размер окна
        self.centralwidget = QtWidgets.QWidget(self)
        self.setCentralWidget(self.centralwidget)

        layout = QtWidgets.QVBoxLayout(self.centralwidget)
        layout.setContentsMargins(20, 20, 20, 20)

        # Заголовок
        self.titleLabel = QtWidgets.QLabel()
        font = QtGui.QFont()
        font.setPointSize(20)
        self.titleLabel.setFont(font)
        self.titleLabel.setAlignment(QtCore.Qt.AlignCenter)
        layout.addWidget(self.titleLabel)

        # Таблица рекордов
        self.recordsTable = QtWidgets.QTableWidget()
        self.recordsTable.setColumnCount(3)
        self.recordsTable.setHorizontalHeaderLabels(["Место", "Никнейм", "Общее время"])
        self.recordsTable.horizontalHeader().setSectionResizeMode(1, QtWidgets.QHeaderView.Stretch)
        self.recordsTable.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
        self.recordsTable.setSelectionMode(QtWidgets.QAbstractItemView.NoSelection)
        layout.addWidget(self.recordsTable)

        # Нижняя панель с кнопками
        bottom_layout = QtWidgets.QHBoxLayout()
        bottom_layout.setContentsMargins(0, 20, 0, 0)

        # Кнопка музыки (слева)
        self.musicButton = QtWidgets.QPushButton()
        self.musicButton.setFixedSize(81, 81)
        font = QtGui.QFont()
        font.setPointSize(24)
        self.musicButton.setFont(font)
        self.musicButton.setCheckable(True)
        self.musicButton.setStyleSheet("QPushButton {border: none;}")
        self.musicButton.clicked.connect(self.toggle_music)
        if self.music_manager:
            self.update_music_button(self.music_manager.is_playing)
        bottom_layout.addWidget(self.musicButton)

        # Пустое пространство посередине
        bottom_layout.addStretch()

        # Кнопка меню (справа)
        self.menuButton = QtWidgets.QPushButton("Меню")
        self.menuButton.setFixedSize(81, 81)
        font = QtGui.QFont()
        font.setFamily("Times New Roman")
        font.setPointSize(14)
        self.menuButton.setFont(font)
        self.menuButton.clicked.connect(self.close)
        bottom_layout.addWidget(self.menuButton)

        layout.addLayout(bottom_layout)

        self.retranslateUi()
        self.load_records()

    def toggle_music(self):
        if self.music_manager:
            self.music_manager.toggle_music()

    def update_music_button(self, is_playing):
        self.musicButton.setChecked(is_playing)
        self.musicButton.setText("🔇" if is_playing else "♪")

    def load_records(self):
        records = RecordsManager.load_records()
        self.recordsTable.setRowCount(len(records))

        for i, record in enumerate(records):
            self.recordsTable.setItem(i, 0, QtWidgets.QTableWidgetItem(str(i + 1)))
            self.recordsTable.item(i, 0).setTextAlignment(QtCore.Qt.AlignCenter)

            self.recordsTable.setItem(i, 1, QtWidgets.QTableWidgetItem(record["nickname"]))
            self.recordsTable.item(i, 1).setTextAlignment(QtCore.Qt.AlignCenter)

            time_str = self.format_time(record["time"])
            self.recordsTable.setItem(i, 2, QtWidgets.QTableWidgetItem(time_str))
            self.recordsTable.item(i, 2).setTextAlignment(QtCore.Qt.AlignCenter)

    def format_time(self, seconds):
        hours = seconds // 3600
        minutes = (seconds % 3600) // 60
        seconds = seconds % 60
        return f"{hours:02}:{minutes:02}:{seconds:02}"

    def retranslateUi(self):
        _translate = QtCore.QCoreApplication.translate
        self.setWindowTitle(_translate("RecordsWindow", "Рекорды"))
        self.titleLabel.setText(_translate("RecordsWindow", "Таблица рекордов"))


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        self.MainWindow = MainWindow
        MainWindow.setObjectName("Меню")
        MainWindow.setFixedSize(701, 738)  # Фиксированный размер окна
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")

        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(160, 150, 391, 81))
        font = QtGui.QFont()
        font.setFamily("Times New Roman")
        font.setPointSize(28)
        self.label.setFont(font)
        self.label.setObjectName("label")

        self.pushButton = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton.setGeometry(QtCore.QRect(220, 260, 281, 101))
        font = QtGui.QFont()
        font.setFamily("Times New Roman")
        font.setPointSize(20)
        font.setBold(True)
        font.setWeight(75)
        self.pushButton.setFont(font)
        self.pushButton.setObjectName("pushButton")

        self.pushButton_2 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_2.setGeometry(QtCore.QRect(30, 30, 151, 51))
        font = QtGui.QFont()
        font.setFamily("Times New Roman")
        font.setPointSize(12)
        self.pushButton_2.setFont(font)
        self.pushButton_2.setObjectName("pushButton_2")

        self.pushButton_3 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_3.setGeometry(QtCore.QRect(600, 10, 81, 81))
        font = QtGui.QFont()
        font.setPointSize(24)
        self.pushButton_3.setFont(font)
        self.pushButton_3.setObjectName("pushButton_3")
        self.pushButton_3.setCheckable(True)
        self.pushButton_3.setStyleSheet("QPushButton {border: none;}")

        self.pushButton_4 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_4.setGeometry(QtCore.QRect(220, 390, 281, 91))
        font = QtGui.QFont()
        font.setFamily("Times New Roman")
        font.setPointSize(16)
        self.pushButton_4.setFont(font)
        self.pushButton_4.setObjectName("pushButton_4")

        self.pushButton_5 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_5.setGeometry(QtCore.QRect(220, 510, 281, 91))
        font = QtGui.QFont()
        font.setFamily("Times New Roman")
        font.setPointSize(16)
        self.pushButton_5.setFont(font)
        self.pushButton_5.setObjectName("pushButton_5")

        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 701, 26))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.music_manager = MusicManager(r"C:\Users\egork\Desktop\Мелодия для игры.mp3")
        self.music_manager.add_listener(self)
        self.pushButton_3.setChecked(False)
        self.records_window = RecordsWindow(MainWindow, self.music_manager)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

        self.pushButton_2.clicked.connect(self.open_rules_dialog)
        self.pushButton.clicked.connect(self.open_level_window)
        self.pushButton_4.clicked.connect(self.open_records_window)
        self.pushButton_5.clicked.connect(MainWindow.close)
        self.pushButton_3.clicked.connect(self.toggle_music)

    def toggle_music(self):
        if self.music_manager:
            self.music_manager.toggle_music()

    def update_music_button(self, is_playing):
        self.pushButton_3.setChecked(is_playing)
        self.pushButton_3.setText("🔇" if is_playing else "♪")

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Меню"))
        self.label.setText(_translate("MainWindow", "Слово по картинке"))
        self.pushButton.setText(_translate("MainWindow", "Начать"))
        self.pushButton_2.setText(_translate("MainWindow", "Правила игры"))
        self.pushButton_3.setText("♪")
        self.pushButton_4.setText(_translate("MainWindow", "Рекорды"))
        self.pushButton_5.setText(_translate("MainWindow", "Выход"))

    def open_rules_dialog(self):
        self.Dialog = QtWidgets.QDialog()
        self.ui = Ui_Dialog()
        self.ui.setupUi(self.Dialog)
        self.ui.pushButton.clicked.connect(self.Dialog.close)
        self.Dialog.show()

    def open_level_window(self):
        self.LevelWindow = QtWidgets.QMainWindow()
        self.ui_level = Ui_LevelWindow(self, level=1, music_manager=self.music_manager)
        self.ui_level.setupUi(self.LevelWindow)
        self.LevelWindow.show()
        self.MainWindow.hide()

    def open_records_window(self):
        self.records_window.load_records()
        self.records_window.show()
        self.records_window.raise_()
        self.records_window.activateWindow()


class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.setFixedSize(701, 738)  # Фиксированный размер окна
        Dialog.setWindowFlags(Dialog.windowFlags() & ~QtCore.Qt.WindowContextHelpButtonHint)  # Удаляем иконку помощи
        self.label = QtWidgets.QLabel(Dialog)
        self.label.setGeometry(QtCore.QRect(210, -30, 281, 161))
        font = QtGui.QFont()
        font.setFamily("Times New Roman")
        font.setPointSize(24)
        font.setBold(True)
        font.setWeight(75)
        self.label.setFont(font)
        self.label.setObjectName("label")

        self.label_2 = QtWidgets.QLabel(Dialog)
        self.label_2.setGeometry(QtCore.QRect(50, 100, 600, 500))
        font = QtGui.QFont()
        font.setFamily("Times New Roman")
        font.setPointSize(12)
        self.label_2.setFont(font)
        self.label_2.setAlignment(QtCore.Qt.AlignCenter)
        self.label_2.setWordWrap(True)
        self.label_2.setObjectName("label_2")

        self.pushButton = QtWidgets.QPushButton(Dialog)
        self.pushButton.setGeometry(QtCore.QRect(290, 640, 141, 71))
        font = QtGui.QFont()
        font.setPointSize(14)
        self.pushButton.setFont(font)
        self.pushButton.setObjectName("pushButton")

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Правила игры"))
        self.label.setText(_translate("Dialog", "Правила игры"))
        self.label_2.setText(_translate("Dialog",
                                        "<html><head/><body><p>На экране появляется изображение, которое связано с загаданным словом.</p>"
                                        "<p>В нижней части экрана отображается набор букв, из которых игрок должен составить слово.</p>"
                                        "<p>Игроку следует внимательно посмотреть на изображение и попытаться определить какое слово оно может представлять.</p>"
                                        "<p>После того как игрок составил слово, он нажимает кнопку для проверки.</p>"
                                        "<p>Если слово правильное, он переходит к следующему уровню.</p>"
                                        "<p>Если слово неправильное, на экране появляется ошибка, и игрок может попробовать снова.</p>"
                                        "<p>В конце игры игроку предлагается ввести свой ник для таблицы рекордов.</p>"
                                        "</body></html>"))
        self.pushButton.setText(_translate("Dialog", "Ок"))


class Ui_LevelWindow(object):
    def __init__(self, main_menu, level=1, music_manager=None):
        self.main_menu = main_menu
        self.level = level
        self.music_manager = music_manager
        if music_manager:
            music_manager.add_listener(self)
        self.level_data = {
            1: {"image_path": r"C:\Users\egork\Desktop\ливень.jpg", "correct_word": "ливень"},
            2: {"image_path": r"C:\Users\egork\Desktop\купюра.jpg", "correct_word": "деньги"},
            3: {"image_path": r"C:\Users\egork\Desktop\клевер.jpg", "correct_word": "удача"}
        }
        self.total_time = 0

    def setupUi(self, LevelWindow):
        self.LevelWindow = LevelWindow
        LevelWindow.setObjectName("LevelWindow")
        LevelWindow.setFixedSize(701, 738)  # Фиксированный размер окна
        self.centralwidget = QtWidgets.QWidget(LevelWindow)
        self.centralwidget.setObjectName("centralwidget")

        self.pushButton = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton.setGeometry(QtCore.QRect(600, 20, 81, 81))
        font = QtGui.QFont()
        font.setFamily("Times New Roman")
        font.setPointSize(14)
        self.pushButton.setFont(font)
        self.pushButton.setObjectName("pushButton")
        self.pushButton.clicked.connect(self.toggleTimer)

        self.timerLabel = QtWidgets.QLabel(self.centralwidget)
        self.timerLabel.setGeometry(QtCore.QRect(600, 110, 81, 30))
        self.timerLabel.setAlignment(QtCore.Qt.AlignCenter)
        self.timerLabel.setStyleSheet("font-size: 16px; font-weight: bold;")
        self.timerLabel.setText("00:00:00")

        self.pushButton_2 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_2.setGeometry(QtCore.QRect(20, 630, 81, 81))
        font = QtGui.QFont()
        font.setPointSize(20)
        self.pushButton_2.setFont(font)
        self.pushButton_2.setObjectName("pushButton_2")
        self.pushButton_2.setCheckable(True)
        self.pushButton_2.setStyleSheet("QPushButton {border: none;}")
        self.pushButton_2.clicked.connect(self.toggle_music)
        if self.music_manager:
            self.update_music_button(self.music_manager.is_playing)

        self.checkButton = QtWidgets.QPushButton(self.centralwidget)
        self.checkButton.setGeometry(QtCore.QRect(300, 630, 120, 81))
        font = QtGui.QFont()
        font.setFamily("Times New Roman")
        font.setPointSize(14)
        self.checkButton.setFont(font)
        self.checkButton.setObjectName("checkButton")
        self.checkButton.setText("Проверить")
        self.checkButton.clicked.connect(self.onCheckButtonClicked)

        self.pushButton_3 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_3.setGeometry(QtCore.QRect(590, 630, 81, 81))
        font = QtGui.QFont()
        font.setFamily("Times New Roman")
        font.setPointSize(14)
        self.pushButton_3.setFont(font)
        self.pushButton_3.setObjectName("pushButton_3")
        self.pushButton_3.clicked.connect(self.confirm_return_to_menu)

        self.wordInput = QtWidgets.QPlainTextEdit(self.centralwidget)
        self.wordInput.setGeometry(QtCore.QRect(70, 280, 560, 50))
        self.wordInput.setStyleSheet("font-size: 20px;")
        self.wordInput.setLineWrapMode(QtWidgets.QPlainTextEdit.NoWrap)
        self.wordInput.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.wordInput.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOn)
        self.wordInput.setReadOnly(True)

        self.keyboardLayout = QtWidgets.QGridLayout()
        self.keyboardLayout.setSpacing(5)
        alphabet = 'АБВГДЕЁЖЗИЙКЛМНОПРСТУФХЦЧШЩЪЫЬЭЮЯ'

        row, col = 0, 0
        for letter in alphabet:
            button = QtWidgets.QPushButton(letter)
            button.setFixedSize(40, 40)
            button.clicked.connect(lambda _, l=letter: self.onKeyboardButtonClicked(l))
            self.keyboardLayout.addWidget(button, row, col)
            col += 1
            if col > 6:
                col = 0
                row += 1

        backspaceButton = QtWidgets.QPushButton("⌫")
        backspaceButton.setFixedSize(80, 40)
        backspaceButton.clicked.connect(self.onBackspaceClicked)
        self.keyboardLayout.addWidget(backspaceButton, row, col, 1, 2)

        self.keyboardWidget = QtWidgets.QWidget(self.centralwidget)
        self.keyboardWidget.setLayout(self.keyboardLayout)
        self.keyboardWidget.setGeometry(QtCore.QRect(20, 340, 660, 300))

        self.imageLabel = QtWidgets.QLabel(self.centralwidget)
        self.imageLabel.setGeometry(QtCore.QRect(40, 15, 560, 250))
        self.imageLabel.setAlignment(QtCore.Qt.AlignCenter)
        self.imageLabel.setStyleSheet("background-color: transparent; border: none;")

        LevelWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(LevelWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 701, 26))
        self.menubar.setObjectName("menubar")
        LevelWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(LevelWindow)
        self.statusbar.setObjectName("statusbar")
        LevelWindow.setStatusBar(self.statusbar)

        self.timer = QtCore.QTimer()
        self.timer.timeout.connect(self.updateTimer)
        self.timer.start(1000)
        self.seconds = 0
        self.timerRunning = True

        self.loadImageForCurrentLevel()
        self.retranslateUi(LevelWindow)
        QtCore.QMetaObject.connectSlotsByName(LevelWindow)

    def confirm_return_to_menu(self):
        if self.level in [1, 2, 3]:
            msg_box = QtWidgets.QMessageBox()
            msg_box.setWindowTitle('Подтверждение')
            msg_box.setText('Вы точно хотите перейти в меню? Игровой процесс не сохранится')
            msg_box.setStandardButtons(QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No)
            msg_box.button(QtWidgets.QMessageBox.Yes).setText('Да')
            msg_box.button(QtWidgets.QMessageBox.No).setText('Нет')
            msg_box.setDefaultButton(QtWidgets.QMessageBox.No)
            msg_box.setWindowFlags(
                msg_box.windowFlags() & ~QtCore.Qt.WindowContextHelpButtonHint)  # Удаляем иконку помощи

            reply = msg_box.exec_()
            if reply == QtWidgets.QMessageBox.Yes:
                self.return_to_main_menu()
        else:
            self.return_to_main_menu()

    def toggle_music(self):
        if self.music_manager:
            self.music_manager.toggle_music()

    def update_music_button(self, is_playing):
        self.pushButton_2.setChecked(is_playing)
        self.pushButton_2.setText("🔇" if is_playing else "♪")

    def retranslateUi(self, LevelWindow):
        _translate = QtCore.QCoreApplication.translate
        LevelWindow.setWindowTitle(_translate("LevelWindow", f"{self.level} уровень"))
        self.pushButton.setText(_translate("LevelWindow", "Пауза"))
        self.pushButton_2.setText("🔇" if self.pushButton_2.isChecked() else "♪")
        self.pushButton_3.setText(_translate("LevelWindow", "Меню"))

    def loadImageForCurrentLevel(self):
        if self.level in self.level_data:
            level_info = self.level_data[self.level]
            self.loadImageFromFile(level_info["image_path"])
            self.current_correct_word = level_info["correct_word"]
        else:
            print(f"Нет данных для уровня {self.level}")

    def updateTimer(self):
        if self.timerRunning:
            self.seconds += 1
            hours = self.seconds // 3600
            minutes = (self.seconds % 3600) // 60
            seconds = self.seconds % 60
            self.timerLabel.setText(f"{hours:02}:{minutes:02}:{seconds:02}")

    def toggleTimer(self):
        if self.timerRunning:
            self.timer.stop()
            self.timerRunning = False
            self.pushButton.setText("Старт")
            self.set_input_enabled(False)  # Блокируем ввод при паузе
        else:
            self.timer.start(1000)
            self.timerRunning = True
            self.pushButton.setText("Пауза")
            self.set_input_enabled(True)  # Разблокируем ввод при возобновлении

    def set_input_enabled(self, enabled):
        """Включает или отключает элементы ввода"""
        self.wordInput.setReadOnly(not enabled)
        self.checkButton.setEnabled(enabled)

        # Блокируем или разблокируем все кнопки клавиатуры
        for i in range(self.keyboardLayout.count()):
            widget = self.keyboardLayout.itemAt(i).widget()
            if widget:
                widget.setEnabled(enabled)

    def onKeyboardButtonClicked(self, letter):
        if not self.timerRunning:  # Если игра на паузе, игнорируем ввод
            return

        scroll_position = self.wordInput.horizontalScrollBar().value()
        current_text = self.wordInput.toPlainText()
        new_text = current_text + letter
        self.wordInput.setPlainText(new_text)
        self.wordInput.horizontalScrollBar().setValue(scroll_position)

    def onBackspaceClicked(self):
        if not self.timerRunning:  # Если игра на паузе, игнорируем ввод
            return

        scroll_position = self.wordInput.horizontalScrollBar().value()
        current_text = self.wordInput.toPlainText()
        if current_text:
            new_text = current_text[:-1]
            self.wordInput.setPlainText(new_text)
        self.wordInput.horizontalScrollBar().setValue(scroll_position)

    def loadImageFromFile(self, imagePath):
        pixmap = QtGui.QPixmap(imagePath)
        if not pixmap.isNull():
            pixmap = pixmap.scaled(self.imageLabel.width(), self.imageLabel.height(), QtCore.Qt.KeepAspectRatio)
            self.imageLabel.setPixmap(pixmap)
        else:
            print("Ошибка загрузки изображения.")

    def onCheckButtonClicked(self):
        if not self.timerRunning:  # Если игра на паузе, игнорируем проверку
            return

        user_input = self.wordInput.toPlainText().strip().lower()
        if user_input == self.current_correct_word.lower():
            if self.level == 3:
                self.total_time += self.seconds
                self.showGameCompletedDialog()
            else:
                self.total_time += self.seconds
                self.timer.stop()
                self.showVictoryDialog()
        else:
            msg = QtWidgets.QMessageBox()
            msg.setWindowTitle("Результат")
            msg.setText("Неправильно, попробуй еще раз")
            msg.setWindowFlags(msg.windowFlags() & ~QtCore.Qt.WindowContextHelpButtonHint)  # Удаляем иконку помощи
            msg.exec_()

    def showVictoryDialog(self):
        self.victoryDialog = QtWidgets.QDialog()
        self.victoryDialog.setWindowTitle("Победа!")
        self.victoryDialog.setFixedSize(300, 150)  # Фиксированный размер окна
        self.victoryDialog.setWindowFlags(
            self.victoryDialog.windowFlags() & ~QtCore.Qt.WindowContextHelpButtonHint)  # Удаляем иконку помощи

        layout = QtWidgets.QVBoxLayout()

        label = QtWidgets.QLabel("Молодец! Ты выиграл!")
        label.setAlignment(QtCore.Qt.AlignCenter)
        layout.addWidget(label)

        nextLevelButton = QtWidgets.QPushButton("Следующий уровень")
        nextLevelButton.clicked.connect(self.goToNextLevel)
        layout.addWidget(nextLevelButton)

        self.victoryDialog.setLayout(layout)
        self.victoryDialog.exec_()

    def showGameCompletedDialog(self):
        self.timer.stop()
        self.showNicknameDialog()

    def showNicknameDialog(self):
        dialog = QtWidgets.QDialog(self.LevelWindow)
        dialog.setWindowTitle("Игра пройдена!")
        dialog.setFixedSize(400, 150)  # Фиксированный размер окна
        dialog.setWindowFlags(dialog.windowFlags() & ~QtCore.Qt.WindowContextHelpButtonHint)  # Удаляем иконку помощи

        layout = QtWidgets.QVBoxLayout(dialog)

        label = QtWidgets.QLabel("Поздравляем! Вы прошли игру! Введите ваш никнейм:")
        label.setAlignment(QtCore.Qt.AlignCenter)
        layout.addWidget(label)

        nickname_input = QtWidgets.QLineEdit()
        nickname_input.setPlaceholderText("Ваш никнейм")
        layout.addWidget(nickname_input)

        btn_confirm = QtWidgets.QPushButton("Сохранить результат")
        btn_confirm.clicked.connect(lambda: self.save_record_and_close(dialog, nickname_input.text()))
        layout.addWidget(btn_confirm)

        dialog.exec_()

    def save_record_and_close(self, dialog, nickname):
        if nickname.strip():
            RecordsManager.save_record(nickname.strip(), self.total_time)
            if hasattr(self.main_menu, 'records_window'):
                self.main_menu.records_window.load_records()
            dialog.close()
            self.return_to_main_menu()
        else:
            self.show_empty_nickname_warning()

    def show_empty_nickname_warning(self):
        warning = QtWidgets.QDialog(self.LevelWindow)
        warning.setWindowTitle("Внимание")
        warning.setFixedSize(300, 150)
        warning.setWindowFlags(warning.windowFlags() & ~QtCore.Qt.WindowContextHelpButtonHint)  # Удаляем иконку помощи

        layout = QtWidgets.QVBoxLayout(warning)

        label = QtWidgets.QLabel("Пожалуйста, введите никнейм")
        label.setAlignment(QtCore.Qt.AlignCenter)
        layout.addWidget(label)

        ok_button = QtWidgets.QPushButton("Ок")
        ok_button.clicked.connect(warning.close)
        layout.addWidget(ok_button)

        warning.exec_()

    def goToNextLevel(self):
        self.victoryDialog.close()
        self.LevelWindow.close()
        self.nextLevelWindow = QtWidgets.QMainWindow()
        self.ui_next_level = Ui_LevelWindow(self.main_menu, self.level + 1, self.music_manager)
        self.ui_next_level.total_time = self.total_time
        self.ui_next_level.setupUi(self.nextLevelWindow)
        self.nextLevelWindow.show()

    def return_to_main_menu(self):
        self.LevelWindow.close()
        self.main_menu.MainWindow.show()


if __name__ == "__main__":
    import sys

    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())