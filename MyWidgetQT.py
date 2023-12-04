import sys
from PySide6.QtWidgets import (QApplication, QMainWindow, QVBoxLayout, QWidget, QLineEdit, QPushButton, QComboBox,
                               QLabel, QHBoxLayout)
import pyqtgraph as pg
from PySide6.QtCore import QTimer
import numpy as np
from Database import getSensor, getDevice, updateEtalons


class DynamicGraphWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        # Инициализируем константные значения для двух дополнительных линий
        self.constant_value1 = 2.0
        self.constant_value2 = -1.5

        # Создаем виджет и устанавливаем его в качестве центрального виджета окна
        central_widget = QWidget(self)
        self.setCentralWidget(central_widget)

        # Создаем компоновщик для центрального виджета
        central_layout = QHBoxLayout(central_widget)

        # Создаем график
        self.plot_widget = pg.PlotWidget()

        # Создаем кривые для графика
        self.curve = self.plot_widget.plot(pen='b')
        self.line1 = self.plot_widget.plot(pen='r')
        self.line2 = self.plot_widget.plot(pen='g')

        # Устанавливаем заголовок и метки осей
        self.plot_widget.setTitle("График показаний датчика")
        self.plot_widget.setLabel('left', "Значение")
        self.plot_widget.setLabel('bottom', "Время")
        #self.plot_widget.setYRange(self.constant_value1 - 20, self.constant_value2 + 20, padding=0)

        # Добавляем график в левую половину окна
        central_layout.addWidget(self.plot_widget, stretch=1)

        # Создаем виджет для правой половины окна
        right_widget = QWidget(self)
        right_layout = QVBoxLayout(right_widget)

        # Создаем два поля для ввода значений
        self.value1_edit = QLineEdit(self)
        self.value2_edit = QLineEdit(self)

        # Создаем селектор для выбора вида графика
        self.plot_type_selector = QComboBox(self)
        self.plot_type_selector.addItems(["servoOpenCloseTank",
                                          "coolerOnOffCistern",
                                          "servoOpenCloseConstTank",
                                          "servoOpenCloseDoughMachine",
                                          "heaterOnOffDoughMachine",
                                          "heaterOnOffCloset",
                                          "humidifierOnOffCloset",
                                          "heaterOnOffBake",
                                          ]
                                         )
        self.plot_type_selector.currentIndexChanged.connect(self.update_device)

        # Создаем кнопку
        self.update_button = QPushButton("Обновить", self)
        self.update_button.clicked.connect(self.update_values)

        # Добавляем текстовые поля для отображения значений
        self.text_value1 = QLabel("Статус работы устройства ", self)
        self.text_value2 = QLabel("Параметр устройства: ", self)

        # Добавляем поля, селектор, текстовые поля и кнопку в правую половину окна
        right_layout.addWidget(self.value1_edit)
        right_layout.addWidget(self.value2_edit)
        right_layout.addWidget(self.plot_type_selector)
        right_layout.addWidget(self.update_button)
        right_layout.addWidget(self.text_value1)
        right_layout.addWidget(self.text_value2)

        # Добавляем правую часть окна в компоновщик
        central_layout.addWidget(right_widget, stretch=1)

        # Инициализируем таймер для динамического обновления
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_plot)
        self.timer.start(500)  # Обновление каждые 500 миллисекунд

        # Инициализируем данные для графика
        self.x_data = np.linspace(0, 10, 100)
        self.y_data = np.sin(self.x_data)

        self.Sensor = getSensor("servoOpenCloseTank")
        self.Device = getDevice("servoOpenCloseTank")

    def update_plot(self):
        try:
            plot_type = self.plot_type_selector.currentText()
            self.Sensor = getSensor(plot_type)
        except Exception as e:
            print(e)
            return

        # Обновляем данные графика
        self.x_data = np.roll(self.x_data, -1)
        self.x_data[-1] = self.x_data[-2] + (self.x_data[1] - self.x_data[0])

        self.y_data = np.roll(self.y_data, -1)
        self.y_data[-1] = self.Sensor.actual_parameter

        self.constant_value1 = self.Sensor.etalon_1
        self.constant_value2 = self.Sensor.etalon_2

        # Обновляем данные для всех трех линий
        self.curve.setData(self.x_data, self.y_data)
        self.line1.setData(self.x_data, np.full_like(self.x_data, self.constant_value1))
        self.line2.setData(self.x_data, np.full_like(self.x_data, self.constant_value2))

        # Обновляем значения текстовых полей
        self.text_value1.setText(f"Состояние устройства: {self.Device.device_state_work}")
        self.text_value2.setText(f"Параметр устройства: {self.Device.device_parameter}")

    def update_values(self):
        # Обновляем значения кривой и константных линий на основе введенных данных
        try:
            value1 = float(self.value1_edit.text())
            value2 = float(self.value2_edit.text())
        except ValueError:
            return
        try:
            updateEtalons(self.Sensor.sensor_id, value1, value2)
        except Exception as e:
            print(e)
            return

    def update_device(self):
        try:
            plot_type = self.plot_type_selector.currentText()
            self.Device = getDevice(plot_type)
            self.Sensor = getSensor(self.Device.device_name)
        except Exception as e:
            print(e)
            return


def main():
    app = QApplication(sys.argv)
    window = DynamicGraphWindow()
    window.update_device()
    window.show()
    sys.exit(app.exec())


if __name__ == '__main__':
    main()
