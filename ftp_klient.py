import sys
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QLineEdit, QPushButton, QRadioButton, QVBoxLayout, QHBoxLayout, QLineEdit, QListWidget
from ftplib import FTP
from PyQt5.QtCore import *

login = ""
password = ""
ip_address = ""
ftp = FTP()

class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        # Создаем виджеты для поля ввода IP-адреса, поля ввода логина и пароля,
        # radiobutton для выбора анонимного входа и кнопки
        self.ip_label = QLabel("IP-адрес FTP сервера:", self)
        self.ip_textbox = QLineEdit(self)
        self.login_label = QLabel("Логин:", self)
        self.login_textbox = QLineEdit(self)
        self.port_ftp = QLabel("Порт:", self)
        self.port_ftp_textbox = QLineEdit(self)
        self.password_label = QLabel("Пароль:", self)
        self.password_textbox = QLineEdit(self)
        self.password_textbox.setEchoMode(QLineEdit.Password)
        self.anonymous_radio = QRadioButton("Анонимный вход",self)
        self.button = QPushButton("Подключиться", self)
        self.directory_list = QListWidget()
        self.download_button = QPushButton("Download")
        self.change_dir_button = QPushButton("Перейти по каталогу")
        self.back_button = QPushButton("Назад")
        self.directory_label = QLabel("Directory: ")

        #ТАК НАДОООООО ====================================================================================
        self.probnik = QLabel("                                                                   ", self)
        #==================================================================================================
        self.port_ftp_textbox.setText("21")
        self.ip_textbox.setText("ftp.byfly.by")

        # Устанавливаем расположение виджетов на окне
        vbox = QVBoxLayout()
        hbox1 = QHBoxLayout()
        hbox1.addWidget(self.ip_label)
        hbox1.addWidget(self.ip_textbox)
        hbox1.addWidget(self.port_ftp)
        hbox1.addWidget(self.port_ftp_textbox)
        hbox2 = QHBoxLayout()
        hbox2.addWidget(self.login_label)
        hbox2.addWidget(self.login_textbox)
        hbox2.addWidget(self.password_label)
        hbox2.addWidget(self.password_textbox)
        hbox3 = QVBoxLayout()
        hbox3.addWidget(self.anonymous_radio)
        hbox4 = QVBoxLayout()
        hbox4.addWidget(self.button)
        hbox4.addWidget(self.directory_label)
        hbox5 = QVBoxLayout()
        hbox5.addWidget(self.directory_list)
        hbox6 = QHBoxLayout()
        hbox6.addWidget(self.change_dir_button)
        hbox6.addWidget(self.back_button)
        hbox7 = QHBoxLayout()
        hbox7.addWidget(self.download_button)

        vbox.addLayout(hbox1)
        vbox.addLayout(hbox2)
        vbox.addLayout(hbox3)
        vbox.addLayout(hbox4)
        vbox.addLayout(hbox5)
        vbox.addLayout(hbox6)
        vbox.addLayout(hbox7)
        self.setLayout(vbox)

        # Подключаем обработчик клика к кнопке
        self.button.clicked.connect(self.connect_to_ftp) 
        self.anonymous_radio.clicked.connect(self.anonim)
        self.change_dir_button.clicked.connect(self.change_directory)
        self.back_button.clicked.connect(self.go_back)
        self.download_button.clicked.connect(self.download_file)

        # Настраиваем окно (разрешение пользователь не сможет поменять)
        #self.setFixedSize(440, 270)
        self.setWindowTitle('FTP-клиент')
        
        # Добавляем текст с просьбой ввести логин
        login_text = "Введите ваш логин:"
        self.login_label.setText(login_text)

        # Добавляем текст о анонимном входе
        anonymous_text = "Анонимный вход"
        self.anonymous_radio.setText(anonymous_text)

        # Отображаем окно
        self.show()

    #Создаём пробный ftp доступ  
    def connect_to_ftp(self):
        try:
            # Получаем IP-адрес, логин и пароль из полей ввода и значение radiobutton
            ip_address = self.ip_textbox.text()
            ftp_port = self.port_ftp_textbox.text()
            login = self.login_textbox.text()
            password = self.password_textbox.text()
            anonymous = self.anonymous_radio.isChecked()
            # Если вход выполняется анонимно, используем логин anonymous и пустой пароль
            if anonymous:
                login = "anonymous"
                password = ""
                print("anonymous- " + login , password)
                ftp.connect(ip_address, int(ftp_port), login, password)
            else:
                #Просмотр выходных данных (без анонима)
                print("no_anonymous " + login , password)
            if login == "" and password == "":
                print("no")
                ftp.connect(ip_address, int(ftp_port))
            else:
                print("4125")
                ftp.connect(ip_address, int(ftp_port), login, password)
            #Привязка данных
            proverka_na_230 = ftp.login().split(" ") 
            #Проверка
            print(proverka_na_230)
            # Отправка пользователю сообщение с успешным входом
            if "230" in proverka_na_230 :
                self.probnik.setText("Вход выполнен успешно!")
            else:
                self.probnik.setText("Вход невыполнен")
            # Получаем список файлов в корневом каталоге
            filenames = ftp.nlst()
            self.directory_list.clear()
            for file in filenames:
                self.directory_list.addItem(file)
            text = self.ip_textbox.text()
            self.directory_label.setText("Directory: => " + str(text))
        except:
            self.probnik.setText("Неправильные данные")
         
    def change_directory(self):
        # Получаем имя выбранной папки
        dir_name = self.directory_list.currentItem().text()

        # Меняем текущую директорию на выбранную
        ftp.cwd(dir_name)

        # Получаем список файлов в новой директории
        files = ftp.nlst()
        self.directory_list.clear()
        for file in files:
            self.directory_list.addItem(file)

    def go_back(self):
        # получаем предыдущую директорию
        ftp.cwd('..')
        files = ftp.nlst()
        self.directory_list.clear()
        for file in files:
            self.directory_list.addItem(file)

    def download_file(self):
        # Получаем имя выбранного файла
        filename = self.directory_list.currentItem().text()

        # Скачиваем файл
        with open(filename, "wb") as f:
            ftp.retrbinary("RETR " + filename, f.write)

        #блокировка при активном анониме
    def anonim(self):
        anonymous = self.anonymous_radio.isChecked()
        if anonymous:
            # Блокируем поля логина и пароля
            self.login_textbox.setDisabled(True)
            self.password_textbox.setDisabled(True)
        else:
            # Разблокируем поля логина и пароля
            self.login_textbox.setEnabled(True)
            self.password_textbox.setEnabled(True)

        
       
   
app = QApplication(sys.argv)
window = MainWindow()
window.show()
sys.exit(app.exec_())
