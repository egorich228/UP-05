from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        self.MainWindow = MainWindow  # Сохраняем ссылку на главное окно
        MainWindow.setObjectName("Меню")
        MainWindow.resize(701, 738)
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

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

        # Связываем кнопку "Правила игры" с методом open_rules_dialog
        self.pushButton_2.clicked.connect(self.open_rules_dialog)

        # Связываем кнопку "Начать" с методом open_level_window
        self.pushButton.clicked.connect(self.open_level_window)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Меню"))
        self.label.setText(_translate("MainWindow", "Слово по картинке"))
        self.pushButton.setText(_translate("MainWindow", "Начать"))
        self.pushButton_2.setText(_translate("MainWindow", "Правила игры"))
        self.pushButton_3.setText(_translate("MainWindow", "♪"))
        self.pushButton_4.setText(_translate("MainWindow", "Рекорды"))
        self.pushButton_5.setText(_translate("MainWindow", "Выход"))
        self.pushButton_5.clicked.connect(MainWindow.close)

    def open_rules_dialog(self):
        # Создаем диалоговое окно
        self.Dialog = QtWidgets.QDialog()
        self.ui = Ui_Dialog()
        self.ui.setupUi(self.Dialog)
        # Связываем кнопку "Ок" с закрытием диалога
        self.ui.pushButton.clicked.connect(self.Dialog.close)
        self.Dialog.show()

    def open_level_window(self):
        # Создаем окно с уровнем
        self.LevelWindow = QtWidgets.QMainWindow()
        self.ui_level = Ui_LevelWindow(self)  # Передаем ссылку на главное меню
        self.ui_level.setupUi(self.LevelWindow)
        self.LevelWindow.show()
        self.MainWindow.hide()  # Скрываем главное меню


class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Правила игры")
        Dialog.resize(701, 738)
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
        self.label_2.setGeometry(QtCore.QRect(20, 110, 731, 511))
        font = QtGui.QFont()
        font.setFamily("Times New Roman")
        font.setPointSize(12)
        self.label_2.setFont(font)
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
        self.label_2.setText(_translate("Dialog", "<html><head/><body><p>На экране появляется изображение, которое связано с загаданным словом.</p><p>В нижней части экрана отображается набор букв, из которых игрок </p><p>должен составить слово. </p><p>Игроку следует внимательно посмотреть на изображение и попытаться</p><p>определить какое слово оно может представлять.</p><p>Слово может быть связано с объектом, действием или концепцией, </p><p>изображенной на картинке.</p><p>Для ввода слова игрок нажимает на буквы виртуальной клавиатуры, </p><p>чтобы сформировать нужное слово.</p><p>После того как игрок составил слово, он нажимает кнопку для проверки.</p><p>Если слово правильное, он переходит к следующему уровню.</p><p>Если слово неправильное, на экране появляется ошибка, и игрок может</p><p>попробовать снова.</p><p>Игра продолжается до тех пор, пока игрок не пройдет все уровни или не </p><p>решит завершить игру.</p><p>В конце игры игроку предлагается ввести свой ник, </p><p>после этого он может нажать в главном меню на кнопку рекорды,</p><p>чтобы ознакомиться со своими результатами и результатами других пользователей.</p></body></html>"))
        self.pushButton.setText(_translate("Dialog", "Ок"))


class Ui_LevelWindow(object):
    def __init__(self, main_menu):
        self.main_menu = main_menu  # Сохраняем ссылку на главное меню

    def setupUi(self, LevelWindow):
        self.LevelWindow = LevelWindow  # Сохраняем ссылку на окно уровня
        LevelWindow.setObjectName("MainWindow")
        LevelWindow.resize(701, 738)
        self.centralwidget = QtWidgets.QWidget(LevelWindow)
        self.centralwidget.setObjectName("centralwidget")

        # Кнопка "Пауза" (остается на своем месте)
        self.pushButton = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton.setGeometry(QtCore.QRect(600, 20, 81, 81))
        font = QtGui.QFont()
        font.setFamily("Times New Roman")
        font.setPointSize(14)
        self.pushButton.setFont(font)
        self.pushButton.setObjectName("pushButton")
        self.pushButton.clicked.connect(self.toggleTimer)  # Подключаем обработчик нажатия

        # Таймер под кнопкой "Пауза"
        self.timerLabel = QtWidgets.QLabel(self.centralwidget)
        self.timerLabel.setGeometry(QtCore.QRect(600, 110, 81, 30))  # Позиция под кнопкой "Пауза"
        self.timerLabel.setAlignment(QtCore.Qt.AlignCenter)
        self.timerLabel.setStyleSheet("font-size: 16px; font-weight: bold;")
        self.timerLabel.setText("00:00:00")  # Начальное значение таймера

        # Кнопка "♪" (сдвигаем влево)
        self.pushButton_2 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_2.setGeometry(QtCore.QRect(20, 630, 81, 81))
        font = QtGui.QFont()
        font.setPointSize(20)
        self.pushButton_2.setFont(font)
        self.pushButton_2.setObjectName("pushButton_2")

        # Кнопка "Проверить" (между "♪" и "Меню")
        self.checkButton = QtWidgets.QPushButton(self.centralwidget)
        self.checkButton.setGeometry(QtCore.QRect(300, 630, 120, 81))  # Позиция и размер кнопки
        font = QtGui.QFont()
        font.setFamily("Times New Roman")
        font.setPointSize(14)
        self.checkButton.setFont(font)
        self.checkButton.setObjectName("checkButton")
        self.checkButton.setText("Проверить")  # Текст кнопки
        self.checkButton.clicked.connect(self.onCheckButtonClicked)  # Подключаем обработчик нажатия

        # Кнопка "Меню" (сдвигаем вправо)
        self.pushButton_3 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_3.setGeometry(QtCore.QRect(590, 630, 81, 81))
        font = QtGui.QFont()
        font.setFamily("Times New Roman")
        font.setPointSize(14)
        self.pushButton_3.setFont(font)
        self.pushButton_3.setObjectName("pushButton_3")
        self.pushButton_3.clicked.connect(self.return_to_main_menu)  # Возврат в главное меню

        # Поле для ввода слова (по центру над клавиатурой)
        self.wordInput = QtWidgets.QPlainTextEdit(self.centralwidget)  # Используем QPlainTextEdit
        self.wordInput.setGeometry(QtCore.QRect(70, 280, 560, 50))  # Позиция и размер поля ввода
        self.wordInput.setStyleSheet("font-size: 20px;")
        self.wordInput.setLineWrapMode(QtWidgets.QPlainTextEdit.NoWrap)  # Отключаем перенос строк
        self.wordInput.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)  # Отключаем вертикальную прокрутку
        self.wordInput.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOn)  # Включаем горизонтальную прокрутку
        self.wordInput.setReadOnly(True)  # Запрещаем ввод с клавиатуры

        # Создаем GridLayout для виртуальной клавиатуры
        self.keyboardLayout = QtWidgets.QGridLayout()
        self.keyboardLayout.setSpacing(5)  # Уменьшаем расстояние между кнопками
        self.keyboardLayout.setObjectName("keyboardLayout")

        # Список букв алфавита
        alphabet = 'АБВГДЕЁЖЗИЙКЛМНОПРСТУФХЦЧШЩЪЫЬЭЮЯ'

        # Добавляем кнопки с буквами в GridLayout
        row, col = 0, 0
        for letter in alphabet:
            button = QtWidgets.QPushButton(letter)
            button.setFixedSize(40, 40)  # Уменьшаем размер кнопок
            button.clicked.connect(lambda _, l=letter: self.onKeyboardButtonClicked(l))  # Подключаем обработчик нажатия
            self.keyboardLayout.addWidget(button, row, col)
            col += 1
            if col > 6:  # Ограничиваем количество кнопок в строке
                col = 0
                row += 1

        # Добавляем кнопку "Backspace" (⌫) для удаления последнего символа
        backspaceButton = QtWidgets.QPushButton("⌫")
        backspaceButton.setFixedSize(80, 40)  # Увеличиваем размер кнопки
        backspaceButton.clicked.connect(self.onBackspaceClicked)  # Подключаем обработчик нажатия
        self.keyboardLayout.addWidget(backspaceButton, row, col, 1, 2)  # Размещаем кнопку в сетке

        # Создаем контейнер для виртуальной клавиатуры
        self.keyboardWidget = QtWidgets.QWidget(self.centralwidget)
        self.keyboardWidget.setLayout(self.keyboardLayout)
        self.keyboardWidget.setGeometry(QtCore.QRect(20, 340, 660, 300))  # Позиция и размер клавиатуры

        # Добавляем QLabel для отображения картинки
        self.imageLabel = QtWidgets.QLabel(self.centralwidget)
        self.imageLabel.setGeometry(QtCore.QRect(40, 15, 560, 250))  # Позиция и размер картинки
        self.imageLabel.setAlignment(QtCore.Qt.AlignCenter)
        # Убираем фон и рамку
        self.imageLabel.setStyleSheet("background-color: transparent; border: none;")

        # Загружаем картинку из локального файла
        self.loadImageFromFile(r"C:\Users\egork\Desktop\зонт.jpg")  # Путь к изображению

        LevelWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(LevelWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 701, 26))
        self.menubar.setObjectName("menubar")
        LevelWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(LevelWindow)
        self.statusbar.setObjectName("statusbar")
        LevelWindow.setStatusBar(self.statusbar)

        # Таймер для обновления времени
        self.timer = QtCore.QTimer()
        self.timer.timeout.connect(self.updateTimer)
        self.timer.start(1000)  # Обновление каждую секунду
        self.seconds = 0  # Счетчик секунд
        self.timerRunning = True  # Состояние таймера (запущен/остановлен)

        self.retranslateUi(LevelWindow)
        QtCore.QMetaObject.connectSlotsByName(LevelWindow)

    def retranslateUi(self, LevelWindow):
        _translate = QtCore.QCoreApplication.translate
        LevelWindow.setWindowTitle(_translate("MainWindow", "1 уровень"))
        self.pushButton.setText(_translate("MainWindow", "Пауза"))
        self.pushButton_2.setText(_translate("MainWindow", "♪"))
        self.pushButton_3.setText(_translate("MainWindow", "Меню"))

    def updateTimer(self):
        """Обновление таймера каждую секунду."""
        if self.timerRunning:
            self.seconds += 1
            hours = self.seconds // 3600
            minutes = (self.seconds % 3600) // 60
            seconds = self.seconds % 60
            self.timerLabel.setText(f"{hours:02}:{minutes:02}:{seconds:02}")

    def toggleTimer(self):
        """Остановка/запуск таймера при нажатии на кнопку 'Пауза'."""
        if self.timerRunning:
            self.timer.stop()  # Останавливаем таймер
            self.timerRunning = False
            self.pushButton.setText("Старт")  # Меняем текст кнопки
        else:
            self.timer.start(1000)  # Запускаем таймер
            self.timerRunning = True
            self.pushButton.setText("Пауза")  # Меняем текст кнопки

    def onKeyboardButtonClicked(self, letter):
        """Обработчик нажатия на кнопки виртуальной клавиатуры."""
        current_text = self.wordInput.toPlainText()  # Получаем текущий текст
        new_text = current_text + letter  # Добавляем текст кнопки
        self.wordInput.setPlainText(new_text)  # Обновляем поле ввода

    def onBackspaceClicked(self):
        """Обработчик нажатия на кнопку 'Backspace'."""
        current_text = self.wordInput.toPlainText()  # Получаем текущий текст
        if current_text:  # Если текст не пустой
            new_text = current_text[:-1]  # Удаляем последний символ
            self.wordInput.setPlainText(new_text)  # Обновляем поле ввода

    def loadImageFromFile(self, imagePath):
        """Загрузка и отображение картинки из локального файла."""
        pixmap = QtGui.QPixmap(imagePath)
        if not pixmap.isNull():
            # Масштабируем картинку под размер QLabel
            pixmap = pixmap.scaled(self.imageLabel.width(), self.imageLabel.height(), QtCore.Qt.KeepAspectRatio)
            self.imageLabel.setPixmap(pixmap)
        else:
            print("Ошибка загрузки изображения.")

    def onCheckButtonClicked(self):
        """Обработчик нажатия на кнопку 'Проверить'."""
        user_input = self.wordInput.toPlainText().strip().lower()  # Получаем введенное слово и приводим к нижнему регистру
        if user_input == "дождь":
            QtWidgets.QMessageBox.information(None, "Результат", "Молодец! Ты угадал ответ!")
        else:
            QtWidgets.QMessageBox.warning(None, "Результат", "Не правильно, попробуй еще раз")

    def return_to_main_menu(self):
        """Возврат в главное меню."""
        self.main_menu.MainWindow.show()  # Показываем главное меню
        self.LevelWindow.close()  # Закрываем текущее окно уровня


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())