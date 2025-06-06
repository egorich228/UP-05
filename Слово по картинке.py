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
            self.mediaPlayer.pause()
            self.is_playing = False
        else:
            self.mediaPlayer.play()
            self.is_playing = True
        self._update_listeners()

    def _update_listeners(self):
        for listener in self.listeners:
            listener.update_music_button(self.is_playing)

class RecordsManager:
    @staticmethod
    def save_record(nickname, total_time):
        records = RecordsManager.load_records()
        records.append({"nickname": nickname, "time": total_time})
        records.sort(key=lambda x: x["time"])
        records = records[:10]
        with open('records.json', 'w', encoding='utf-8') as f:
            json.dump(records, f, ensure_ascii=False, indent=4)
        return records

    @staticmethod
    def load_records():
        if not os.path.exists('records.json'):
            return []
        with open('records.json', 'r', encoding='utf-8') as f:
            try:
                return json.load(f)
            except json.JSONDecodeError:
                return []

class LevelsManager:
    @staticmethod
    def load_levels():
        if not os.path.exists('levels.json'):
            return {}

        with open('levels.json', 'r', encoding='utf-8') as f:
            try:
                return json.load(f)
            except json.JSONDecodeError:
                return {}

class MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowState(QtCore.Qt.WindowFullScreen)
        self.setFixedSize(1920, 1080)
        self.stacked_widget = QtWidgets.QStackedWidget()
        self.setCentralWidget(self.stacked_widget)
        self.music_manager = MusicManager(r"C:\Users\egork\Desktop\Слово по картинке\sound\Мелодия для игры.mp3")
        self.main_menu = MainMenuWidget(self)
        self.records_window = RecordsWidget(self)
        self.rules_dialog = RulesDialogWidget(self)
        self.stacked_widget.addWidget(self.main_menu)
        self.stacked_widget.addWidget(self.records_window)
        self.stacked_widget.addWidget(self.rules_dialog)
        self.show_main_menu()

    def show_screen(self, widget, title):
        if widget == self.records_window:
            self.records_window.load_records()
        self.stacked_widget.setCurrentWidget(widget)
        self.setWindowTitle(title)

    def show_main_menu(self):
        self.show_screen(self.main_menu, "Меню")

    def show_records(self):
        self.show_screen(self.records_window, "Рекорды")

    def show_rules(self):
        self.show_screen(self.rules_dialog, "Правила игры")

    def start_level(self, level=1):
        if not hasattr(self, 'level_widget'):
            self.level_widget = LevelWidget(self, level)
            self.stacked_widget.addWidget(self.level_widget)
        else:
            self.level_widget.set_level(level)
        self.show_screen(self.level_widget, f"{level} уровень")

class MainMenuWidget(QtWidgets.QWidget):
    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent
        self.setup_ui()

    def setup_ui(self):
        self.label = QtWidgets.QLabel(self)
        self.label.setGeometry(QtCore.QRect(660, 200, 600, 100))
        font = QtGui.QFont()
        font.setFamily("Times New Roman")
        font.setPointSize(45)
        self.label.setFont(font)
        self.startButton = QtWidgets.QPushButton(self)
        self.startButton.setGeometry(QtCore.QRect(760, 400, 400, 150))
        font = QtGui.QFont()
        font.setFamily("Times New Roman")
        font.setPointSize(36)
        font.setBold(True)
        font.setWeight(75)
        self.startButton.setFont(font)
        self.rulesButton = QtWidgets.QPushButton(self)
        self.rulesButton.setGeometry(QtCore.QRect(50, 50, 250, 80))
        font = QtGui.QFont()
        font.setFamily("Times New Roman")
        font.setPointSize(18)
        self.rulesButton.setFont(font)
        self.musicButton = QtWidgets.QPushButton(self)
        self.musicButton.setGeometry(QtCore.QRect(1750, 30, 120, 120))
        font = QtGui.QFont()
        font.setPointSize(36)
        self.musicButton.setFont(font)
        self.musicButton.setCheckable(True)
        self.musicButton.setStyleSheet("QPushButton {border: none;}")
        self.recordsButton = QtWidgets.QPushButton(self)
        self.recordsButton.setGeometry(QtCore.QRect(760, 600, 400, 120))
        font = QtGui.QFont()
        font.setFamily("Times New Roman")
        font.setPointSize(24)
        self.recordsButton.setFont(font)
        self.exitButton = QtWidgets.QPushButton(self)
        self.exitButton.setGeometry(QtCore.QRect(760, 750, 400, 120))
        font = QtGui.QFont()
        font.setFamily("Times New Roman")
        font.setPointSize(24)
        self.exitButton.setFont(font)
        self.parent.music_manager.add_listener(self)
        self.musicButton.setChecked(False)
        self.update_music_button(self.parent.music_manager.is_playing)
        self.retranslate_ui()
        self.rulesButton.clicked.connect(self.parent.show_rules)
        self.startButton.clicked.connect(lambda: self.parent.start_level(1))
        self.recordsButton.clicked.connect(self.parent.show_records)
        self.exitButton.clicked.connect(self.parent.close)
        self.musicButton.clicked.connect(self.parent.music_manager.toggle_music)

    def update_music_button(self, is_playing):
        self.musicButton.setChecked(is_playing)
        self.musicButton.setText("🔇" if is_playing else "♪")

    def retranslate_ui(self):
        self.label.setText("Слово по картинке")
        self.startButton.setText("Начать")
        self.rulesButton.setText("Правила игры")
        self.musicButton.setText("♪")
        self.recordsButton.setText("Рекорды")
        self.exitButton.setText("Выход")

class RecordsWidget(QtWidgets.QWidget):
    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent
        self.setup_ui()

    def setup_ui(self):
        self.setGeometry(0, 0, 1920, 1080)
        self.titleLabel = QtWidgets.QLabel(self)
        self.titleLabel.setGeometry(QtCore.QRect(0, 50, 1920, 100))
        font = QtGui.QFont()
        font.setPointSize(36)
        self.titleLabel.setFont(font)
        self.titleLabel.setAlignment(QtCore.Qt.AlignCenter)
        self.recordsTable = QtWidgets.QTableWidget(self)
        self.recordsTable.setGeometry(QtCore.QRect(100, 200, 1720, 700))
        self.recordsTable.setColumnCount(3)
        self.recordsTable.setHorizontalHeaderLabels(["Место", "Никнейм", "Общее время"])
        self.recordsTable.horizontalHeader().setSectionResizeMode(0, QtWidgets.QHeaderView.ResizeToContents)
        self.recordsTable.horizontalHeader().setSectionResizeMode(1, QtWidgets.QHeaderView.Stretch)
        self.recordsTable.horizontalHeader().setSectionResizeMode(2, QtWidgets.QHeaderView.ResizeToContents)
        self.recordsTable.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
        self.recordsTable.setSelectionMode(QtWidgets.QAbstractItemView.NoSelection)
        self.recordsTable.setStyleSheet("""
            QTableWidget {
                font-size: 24px;
            }
            QTableWidget::item {
                padding: 10px;
            }
        """)
        self.recordsTable.horizontalHeader().setStyleSheet("""
            QHeaderView::section {
                font-size: 24px;
                padding: 10px;
            }
        """)
        self.recordsTable.verticalHeader().setDefaultSectionSize(60)
        self.recordsTable.verticalHeader().setVisible(False)
        self.musicButton = QtWidgets.QPushButton(self)
        self.musicButton.setGeometry(QtCore.QRect(50, 950, 120, 120))
        font = QtGui.QFont()
        font.setPointSize(36)
        self.musicButton.setFont(font)
        self.musicButton.setCheckable(True)
        self.musicButton.setStyleSheet("QPushButton {border: none;}")
        self.menuButton = QtWidgets.QPushButton("Меню", self)
        self.menuButton.setGeometry(QtCore.QRect(1750, 950, 120, 120))
        font = QtGui.QFont()
        font.setFamily("Times New Roman")
        font.setPointSize(24)
        self.menuButton.setFont(font)
        self.parent.music_manager.add_listener(self)
        self.musicButton.setChecked(False)
        self.update_music_button(self.parent.music_manager.is_playing)
        self.retranslate_ui()
        self.musicButton.clicked.connect(self.parent.music_manager.toggle_music)
        self.menuButton.clicked.connect(self.parent.show_main_menu)

    def update_music_button(self, is_playing):
        self.musicButton.setChecked(is_playing)
        self.musicButton.setText("🔇" if is_playing else "♪")

    def load_records(self):
        records = RecordsManager.load_records()
        self.recordsTable.setRowCount(len(records))
        for i, record in enumerate(records):
            place_item = QtWidgets.QTableWidgetItem(str(i + 1))
            place_item.setTextAlignment(QtCore.Qt.AlignCenter)
            self.recordsTable.setItem(i, 0, place_item)
            nickname_item = QtWidgets.QTableWidgetItem(record["nickname"])
            nickname_item.setTextAlignment(QtCore.Qt.AlignCenter)
            nickname_item.setToolTip(record["nickname"])
            self.recordsTable.setItem(i, 1, nickname_item)
            time_str = self._format_time(record["time"])
            time_item = QtWidgets.QTableWidgetItem(time_str)
            time_item.setTextAlignment(QtCore.Qt.AlignCenter)
            self.recordsTable.setItem(i, 2, time_item)
        self.recordsTable.resizeColumnsToContents()
        self.recordsTable.horizontalHeader().setSectionResizeMode(1, QtWidgets.QHeaderView.Stretch)

    def _format_time(self, seconds):
        hours = seconds // 3600
        minutes = (seconds % 3600) // 60
        seconds = seconds % 60
        return f"{hours:02}:{minutes:02}:{seconds:02}"

    def retranslate_ui(self):
        self.titleLabel.setText("Таблица рекордов")

class RulesDialogWidget(QtWidgets.QWidget):
    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent
        self.setup_ui()

    def setup_ui(self):
        self.setGeometry(0, 0, 1920, 1080)
        self.label = QtWidgets.QLabel(self)
        self.label.setGeometry(QtCore.QRect(0, 100, 1920, 100))
        font = QtGui.QFont()
        font.setFamily("Times New Roman")
        font.setPointSize(48)
        font.setBold(True)
        font.setWeight(75)
        self.label.setFont(font)
        self.label.setAlignment(QtCore.Qt.AlignCenter)
        self.rulesText = QtWidgets.QLabel(self)
        self.rulesText.setGeometry(QtCore.QRect(200, 250, 1520, 600))
        font = QtGui.QFont()
        font.setFamily("Times New Roman")
        font.setPointSize(24)
        self.rulesText.setFont(font)
        self.rulesText.setAlignment(QtCore.Qt.AlignCenter)
        self.rulesText.setWordWrap(True)
        self.okButton = QtWidgets.QPushButton(self)
        self.okButton.setGeometry(QtCore.QRect(860, 800, 200, 100))
        font = QtGui.QFont()
        font.setPointSize(24)
        self.okButton.setFont(font)
        self.retranslate_ui()
        self.okButton.clicked.connect(self.parent.show_main_menu)

    def retranslate_ui(self):
        self.label.setText("Правила игры")
        rules_text = (
            "На экране появляется изображение, которое связано с загаданным словом. "
            "Игроку следует внимательно посмотреть на изображение и попытаться определить, "
            "какое слово оно может представлять. После того как игрок ввел слово с клавиатуры "
            "в специальное поле, он нажимает Enter. Если слово правильное, он может перейти "
            "к следующему уровню. Если слово неправильное, на экране появляется ошибка, и игрок "
            "может попробовать снова. В конце игры игроку предлагается ввести свой ник для "
            "сохранения в таблицу рекордов."
        )
        self.rulesText.setText(rules_text)
        self.okButton.setText("Ок")

class LevelWidget(QtWidgets.QWidget):
    def __init__(self, parent, level=1):
        super().__init__(parent)
        self.parent = parent
        self.level = level
        self.total_time = 0
        self.level_data = LevelsManager.load_levels()
        self.setup_ui()

    def setup_ui(self):
        self.setGeometry(0, 0, 1920, 1080)
        self.pauseButton = QtWidgets.QPushButton("Пауза", self)
        self.pauseButton.setGeometry(QtCore.QRect(50, 50, 120, 120))
        font = QtGui.QFont()
        font.setFamily("Times New Roman")
        font.setPointSize(24)
        self.pauseButton.setFont(font)
        self.timerLabel = QtWidgets.QLabel("00:00:00", self)
        self.timerLabel.setGeometry(QtCore.QRect(800, 50, 1900, 120))
        self.timerLabel.setAlignment(QtCore.Qt.AlignCenter)
        self.timerLabel.setStyleSheet("font-size: 36px; font-weight: bold;")
        self.imageLabel = QtWidgets.QLabel(self)
        self.imageLabel.setGeometry(QtCore.QRect(460, 200, 1000, 600))
        self.imageLabel.setAlignment(QtCore.Qt.AlignCenter)
        self.imageLabel.setStyleSheet("background-color: transparent; border: none;")
        self.wordInput = QtWidgets.QLineEdit(self)
        self.wordInput.setGeometry(QtCore.QRect(560, 850, 800, 80))
        self.wordInput.setStyleSheet("font-size: 36px;")
        self.wordInput.setAlignment(QtCore.Qt.AlignCenter)
        self.wordInput.returnPressed.connect(self.check_answer)
        self.musicButton = QtWidgets.QPushButton(self)
        self.musicButton.setGeometry(QtCore.QRect(50, 950, 120, 120))
        font = QtGui.QFont()
        font.setPointSize(36)
        self.musicButton.setFont(font)
        self.musicButton.setCheckable(True)
        self.musicButton.setStyleSheet("QPushButton {border: none;}")
        self.menuButton = QtWidgets.QPushButton("Меню", self)
        self.menuButton.setGeometry(QtCore.QRect(1750, 950, 120, 120))
        font = QtGui.QFont()
        font.setFamily("Times New Roman")
        font.setPointSize(24)
        self.menuButton.setFont(font)
        self.parent.music_manager.add_listener(self)
        self.musicButton.setChecked(False)
        self.update_music_button(self.parent.music_manager.is_playing)
        self.timer = QtCore.QTimer()
        self.timer.timeout.connect(self.update_timer)
        self.timer.start(1000)
        self.seconds = 0
        self.timerRunning = True
        self.load_level_content()
        self.pauseButton.clicked.connect(self.toggle_timer)
        self.musicButton.clicked.connect(self.parent.music_manager.toggle_music)
        self.menuButton.clicked.connect(self.confirm_return_to_menu)

    def set_level(self, level):
        self.level = level
        self.seconds = 0
        self.timerLabel.setText("00:00:00")
        self.timerRunning = True
        self.timer.start(1000)
        self.wordInput.clear()
        self.load_level_content()
        self.parent.setWindowTitle(f"{level} уровень")

    def update_music_button(self, is_playing):
        self.musicButton.setChecked(is_playing)
        self.musicButton.setText("🔇" if is_playing else "♪")

    def load_level_content(self):
        if str(self.level) in self.level_data:
            level_info = self.level_data[str(self.level)]
            pixmap = QtGui.QPixmap(level_info["image_path"])
            if not pixmap.isNull():
                pixmap = pixmap.scaled(1000, 600, QtCore.Qt.KeepAspectRatio)
                self.imageLabel.setPixmap(pixmap)
            self.current_correct_word = level_info["correct_word"]

    def update_timer(self):
        if self.timerRunning:
            self.seconds += 1
            hours = self.seconds // 3600
            minutes = (self.seconds % 3600) // 60
            seconds = self.seconds % 60
            self.timerLabel.setText(f"{hours:02}:{minutes:02}:{seconds:02}")

    def toggle_timer(self):
        if self.timerRunning:
            self.timer.stop()
            self.timerRunning = False
            self.pauseButton.setText("Старт")
            self.wordInput.setReadOnly(True)
        else:
            self.timer.start(1000)
            self.timerRunning = True
            self.pauseButton.setText("Пауза")
            self.wordInput.setReadOnly(False)

    def check_answer(self):
        if not self.timerRunning:
            return
        user_input = self.wordInput.text().strip().lower()
        if user_input == self.current_correct_word.lower():
            self.total_time += self.seconds
            self.timer.stop()
            if self.level == 10:
                self._handle_game_completion()
            else:
                self._handle_level_completion()
        else:
            self._show_message_box("Результат", "Неправильно, попробуй еще раз")

    def _handle_level_completion(self):
        if self._show_confirmation_dialog("Победа!", "Молодец! Ты выиграл! Перейти к следующему уровню?"):
            self.set_level(self.level + 1)
        else:
            self.timer.start(1000)
            self.timerRunning = True

    def _handle_game_completion(self):
        nickname = self._get_nickname()
        if nickname:
            RecordsManager.save_record(nickname, self.total_time)
            if hasattr(self.parent, 'records_window'):
                self.parent.records_window.load_records()
            self.parent.show_main_menu()

    def _get_nickname(self):
        nickname = ""
        while not nickname:
            nickname = self._show_input_dialog("Игра пройдена!", "Поздравляем! Вы прошли игру! Введите ваш никнейм:")
            if not nickname:
                self._show_message_box("Внимание", "Пожалуйста, введите никнейм")
        return nickname

    def _show_message_box(self, title, text):
        msg = QtWidgets.QMessageBox()
        msg.setWindowTitle(title)
        msg.setText(text)
        msg.setStyleSheet(self._get_message_box_style())
        msg.setWindowFlags(msg.windowFlags() & ~QtCore.Qt.WindowContextHelpButtonHint)
        msg.exec_()

    def _show_confirmation_dialog(self, title, text):
        msg = QtWidgets.QMessageBox()
        msg.setWindowTitle(title)
        msg.setText(text)
        msg.setStyleSheet(self._get_message_box_style())
        msg.setStandardButtons(QtWidgets.QMessageBox.Ok | QtWidgets.QMessageBox.Cancel)
        msg.button(QtWidgets.QMessageBox.Ok).setText("Да")
        msg.button(QtWidgets.QMessageBox.Cancel).setText("Нет")
        msg.setWindowFlags(msg.windowFlags() & ~QtCore.Qt.WindowContextHelpButtonHint)
        return msg.exec_() == QtWidgets.QMessageBox.Ok

    def _show_input_dialog(self, title, label):
        dialog = QtWidgets.QInputDialog(self)
        dialog.setWindowTitle(title)
        dialog.setLabelText(label)
        dialog.setStyleSheet(self._get_message_box_style())
        dialog.setWindowFlags(dialog.windowFlags() & ~QtCore.Qt.WindowContextHelpButtonHint)
        dialog.setOption(QtWidgets.QInputDialog.NoButtons)
        button_box = QtWidgets.QDialogButtonBox(QtWidgets.QDialogButtonBox.Ok)
        button_box.accepted.connect(dialog.accept)
        layout = dialog.layout()
        layout.addWidget(button_box)
        if dialog.exec_():
            return dialog.textValue().strip()
        return ""

    def _get_message_box_style(self):
        return """
            QMessageBox, QInputDialog {
                font-size: 24px;
            }
            QMessageBox QLabel, QInputDialog QLabel {
                font-size: 24px;
            }
            QMessageBox QPushButton, QInputDialog QPushButton {
                font-size: 24px;
                min-width: 100px;
                min-height: 50px;
            }
            QInputDialog QLineEdit {
                font-size: 24px;
                min-height: 50px;
            }
        """

    def confirm_return_to_menu(self):
        if self.level in range(1, 11):
            if self._show_confirmation_dialog('Подтверждение',
                'Вы точно хотите перейти в меню? Игровой процесс не сохранится'):
                self.parent.show_main_menu()
        else:
            self.parent.show_main_menu()

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    window = MainWindow()
    window.showFullScreen()
    sys.exit(app.exec_())