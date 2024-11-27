from PySide6.QtCore import QCoreApplication, QMetaObject, QRect, Qt, QSize, QThread, Signal, QCoreApplication, QTimer
from PySide6.QtGui import QFont, QIcon, QPixmap
from PySide6.QtWidgets import QApplication, QLabel, QPushButton, QSizePolicy, QWidget, QFrame

from server.client import *
from server.verify_server import get_local_ip


# Подключение к серверу
class ConnectionThread(QThread):
    connection_finished = Signal(bool)

    def run(self):
        try:
            # Здесь выполняем подключение к серверу
            client = Client()
            server_ip = get_local_ip()  # Если сервер верификации создаётся на локальной машине
            server_port = 12999
            client.connect_to_server(server_ip, server_port)

            key = "key_261171_192.168.1.68:12673_ABCD"    # Ключ, вводимый пользователем в графическом интерфейсе

            valid_key = client.send_message(key)
            if valid_key == "1":
                print("Подключение...")
                import time
                time.sleep(3)  # Имитация подключения к VPN серверу
                success = True
            else:
                print("Неверный ключ доступа!")
                success = False

            # time.sleep(3)
            # success = True
        except Exception as e:
            print(e)
            success = False

        # Отправляем результат подключения
        self.connection_finished.emit(success)


class MainWindowUI:
    def setup_ui(self, main_window):
        if not main_window.objectName():
            main_window.setObjectName("MainWindow")
        main_window.setFixedSize(400, 600)
        main_window.setStyleSheet("background-color: rgb(37, 37, 37);")

        # Название VPN
        self.title_label = QLabel(main_window)
        self.title_label.setObjectName("title_label")
        self.title_label.setGeometry(QRect(0, 50, 400, 40))
        font_name_vpn = QFont()
        font_name_vpn.setFamilies(["Noto Sans"])
        font_name_vpn.setPointSize(20)
        self.title_label.setFont(font_name_vpn)
        self.title_label.setStyleSheet("color: white;")
        self.title_label.setAlignment(Qt.AlignCenter)

        # Кнопка включения

        # Добавление рамки для кнопки включения нужной для анимации
        self.circle_frame = QFrame(main_window)

        circle_button_size = 150
        circle_frame_size = circle_button_size + 20
        self.circle_frame.setGeometry(
            QRect(
                (main_window.width() - circle_frame_size) // 2,
                (main_window.height() - circle_frame_size) // 2,
                circle_frame_size,
                circle_frame_size,
            )
        )
        self.circle_frame.setStyleSheet(
            f"border-radius: {circle_frame_size / 2}px;")

        # Кнопка
        self.circle_button = QPushButton(self.circle_frame)
        self.circle_button.setObjectName("circle_button")
        self.circle_button.setGeometry(
            QRect(
                (circle_frame_size - circle_button_size) // 2,
                (circle_frame_size - circle_button_size) // 2,
                circle_button_size,
                circle_button_size,
            )
        )
        self.circle_button.setStyleSheet(
            "background-color: #636363;"
            f"border-radius: {circle_button_size / 2}px;"
            "border-width: 5px;"
            "border-color: #A1A1A1;"
            "border-style: solid;"
        )
        self.circle_button.setIcon(QIcon("./img/power.png"))
        self.circle_button.setIconSize(QSize(64, 64))
        self.circle_button.clicked.connect(self.change_connection_status)
        self.circle_button.setFocusPolicy(Qt.NoFocus)

        # Строка состояния подключения
        self.status_bar = QLabel(main_window)
        self.status_bar.setObjectName("status_bar")
        status_bar_width = 200
        status_bar_height = 50
        self.status_bar.setGeometry(QRect(
            (main_window.width() - status_bar_width) // 2,
            (main_window.height() - circle_button_size) // 2 +
            circle_button_size + 20,
            status_bar_width,
            status_bar_height))
        font_status_bar = QFont()
        font_status_bar.setFamilies(["Noto Sans"])
        font_status_bar.setPointSize(12)
        self.status_bar.setFont(font_status_bar)
        self.status_bar.setStyleSheet("color: white;")
        self.status_bar.setAlignment(Qt.AlignCenter)

        # Кнопка выбора сервера
        self.choise_server = QPushButton(main_window)
        self.choise_server.setObjectName("choise_server")
        server_button_size = 40
        self.choise_server.setGeometry(
            QRect(50, 50, server_button_size, server_button_size))
        self.choise_server.setStyleSheet(
            "border-radius: 20px;"
            "border: none;")
        icon_choised_server = QPixmap(
            "./img/countries/netherlands.png").scaled(server_button_size, server_button_size)
        self.choise_server.setIconSize(
            QSize(server_button_size, server_button_size))
        self.choise_server.setIcon(QIcon(icon_choised_server))

        # Кнопка настроек
        self.settings_button = QPushButton(main_window)
        self.settings_button.setObjectName("settings_button")
        settings_button_size = 40
        self.settings_button.setGeometry(
            QRect(main_window.width() - 100, 50, server_button_size, server_button_size))
        self.settings_button.setStyleSheet(
            "border-radius: 20px;"
            "border: none;")
        self.settings_button.setIconSize(
            QSize(settings_button_size, settings_button_size))
        self.settings_button.setIcon(QIcon("./img/settings.png"))

        self.animation_timer = QTimer()
        self.animation_timer.timeout.connect(self.animate_circle_frame)

        # Установку текстовых строк
        self.retranslate_ui(main_window)
        # Подключение слотов
        QMetaObject.connectSlotsByName(main_window)

    def retranslate_ui(self, main_window):
        main_window.setWindowTitle(
            QCoreApplication.translate("MainWindow", "ПМ VPN"))
        self.title_label.setText(QCoreApplication.translate(
            "MainWindow",

            "<span style=\"color: #009688;\">ПМ</span>      "
            "<span style=\"color: white;\">VPN</span>"
        ))
        self.status_bar.setText(QCoreApplication.translate(
            "MainWindow",
            "<p><img src=\"./img/cross.png\" style=\"margin-right: 5px;\" width=\"10\" height=\"10\"> Не подключен</p>"))

    current_status_connection = 0  # 0 - выключен, 1 - подключен

    # Изменение состояния подключения
    def change_connection_status(self):
        if self.current_status_connection == 0:
            self.status_bar.setText(QCoreApplication.translate(
                "MainWindow",
                "<p><img src=\"./img/alarm_clock.png\" style=\"margin-right: 5px;\" width=\"10\" height=\"10\"> Подключение</p>"))
            self.opacity_step = 0
            self.animation_timer.start(50)
            self.connection_thread = ConnectionThread()
            self.connection_thread.connection_finished.connect(
                self.connection_finished)
            self.connection_thread.start()
            self.current_status_connection = 1

        elif self.current_status_connection == 1:
            self.current_status_connection = 0
            self.status_bar.setText(QCoreApplication.translate(
                "MainWindow",
                "<p><img src=\"./img/cross.png\" style=\"margin-right: 5px;\" width=\"10\" height=\"10\"> Не подключен</p>"))
            self.circle_button.setStyleSheet(
                "background-color: #636363;"
                f"border-radius: {150 / 2}px;"
                "border-width: 5px;"
                "border-color: #A1A1A1;"
                "border-style: solid;"
            )
            self.circle_frame.setStyleSheet(f"border-radius: {170 / 2}px;")

    def connection_finished(self, success):
        if success:
            self.animation_timer.stop()
            self.status_bar.setText(QCoreApplication.translate(
                "MainWindow",
                "<p><img src=\"./img/check_mark.png\" style=\"margin-right: 5px;\" width=\"10\" height=\"10\"> Подключен</p>"))
            self.circle_button.setStyleSheet(
                "background-color: #009688;"
                f"border-radius: {150 / 2}px;")
            self.circle_frame.setStyleSheet(
                f"border-radius: {170 / 2}px;"
                "background-color: rgba(0, 150, 136, 0.2);")

    def animate_circle_frame(self):
        max_opacity = 0.7
        min_opacity = 0.2
        speed = 0.05

        self.opacity_step += speed
        opacity = min_opacity + (max_opacity - min_opacity) * \
            abs((self.opacity_step % 2) - 1)

        self.circle_frame.setStyleSheet(
            f"""
            background-color: rgba(0, 150, 136, {opacity});
            border-radius: {self.circle_frame.width() / 2}px;
            """
        )
