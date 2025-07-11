# RIUS_Project - Система автоматизации производственных процессов

## 📋 Описание проекта

RIUS_Project представляет собой комплексную систему автоматизации для управления производственными процессами с возможностью мониторинга, управления и визуализации данных в реальном времени. Система предназначена для автоматизации пекарного или пищевого производства.

## 🚀 Основные возможности

- **Автоматическое управление устройствами** - система автоматически включает/выключает оборудование на основе показаний сенсоров
- **Мониторинг в реальном времени** - отслеживание состояния всех устройств и сенсоров
- **Графическая визуализация** - современный GUI с графиками для мониторинга показаний
- **Логирование процессов** - полная история всех операций в базе данных
- **Настройка эталонных значений** - возможность калибровки сенсоров
- **Обработка ошибок** - система автоматически реагирует на сбои оборудования

## 🏗️ Архитектура проекта

### Основные модули:

#### 📊 **Database.py**
- Работа с MySQL базой данных
- Хранение состояний устройств и сенсоров
- Логирование всех производственных процессов
- Управление типами устройств и сенсоров

#### 🖥️ **MyWidgetQT.py**
- GUI приложение на PySide6
- Динамические графики показаний сенсоров
- Интерфейс для настройки эталонных значений
- Мониторинг состояния устройств в реальном времени

#### ⚙️ **MainAutomates.py**
- Основной цикл автоматизации
- Инициализация системы
- Управление всеми устройствами и сенсорами
- Постоянный мониторинг состояния

#### 🔧 **DeviceAutomate.py**
- Класс для автоматизации устройств
- Управление состояниями (включено/выключено/ошибка)
- Интеграция с ПЛК
- Автоматическое реагирование на показания сенсоров

#### 📡 **SensorAutomate.py**
- Класс для автоматизации сенсоров
- Проверка значений в допустимых пределах
- Обработка ошибок считывания
- Связь с устройствами

### Конфигурационные модули:

#### **Devices.py**
Конфигурация устройств:
- `servoOpenCloseTank` - сервопривод бака
- `coolerOnOffCistern` - охладитель цистерны
- `heaterOnOffDoughMachine` - нагреватель тестомесильной машины
- `humidifierOnOffCloset` - увлажнитель шкафа
- И другие устройства производственной линии

#### **Sensors.py**
Конфигурация сенсоров:
- Датчики уровня (`Level`)
- Датчики температуры (`Temperature`)
- Датчики скорости (`Speed`)
- Датчики времени (`Time`)
- Датчики влажности (`Wet`)

### Модули связи с ПЛК:

#### **PLKMessagesDevices.py**
- Отправка команд на ПЛК
- Получение состояния устройств

#### **PLKMessagesSensors.py**
- Симуляция данных сенсоров
- Имитация реального поведения производственного оборудования

### Структура базы данных
Система автоматически создаст следующие таблицы:
- `devices` - устройства
- `devices_states` - состояния устройств
- `devices_types` - типы устройств
- `sensors` - сенсоры
- `sensors_states` - состояния сенсоров
- `sensors_types` - типы сенсоров
- `production_process_desc` - описание производственных процессов
- `processes_devices_keys` - связь процессов с устройствами

## 📊 Использование GUI

### Главное окно
- **Левая панель**: График показаний выбранного сенсора в реальном времени
- **Правая панель**: Элементы управления и мониторинга

### Функции GUI
1. **Выбор устройства**: Выпадающий список для переключения между устройствами
2. **Настройка эталонов**: Поля для ввода минимального и максимального значений
3. **Мониторинг состояния**: Отображение текущего состояния устройства и параметров
4. **Обновление в реальном времени**: Автоматическое обновление каждые 500мс

## 🔄 Логика работы системы

### Автоматическое управление
1. Система читает показания сенсоров
2. Сравнивает с эталонными значениями
3. Принимает решение о включении/выключении устройства
4. Отправляет команду на ПЛК
5. Логирует все действия в базу данных

### Состояния устройств
- `initial` - инициализация
- `on` - включено
- `off` - выключено
- `error` - ошибка

### Состояния сенсоров
- `init` - инициализация
- `good` - значения в норме
- `bad` - значения вне диапазона
- `error` - ошибка считывания

## 🔧 Конфигурация

### Настройка устройств
Каждое устройство определяется параметрами:
- Имя устройства
- Связанный сенсор
- Значение при включении
- Значение при выключении
- Тип устройства

### Настройка сенсоров
Каждый сенсор определяется параметрами:
- Минимальное эталонное значение
- Максимальное эталонное значение
- Имя сенсора
- Тип сенсора

## 🚨 Обработка ошибок

Система включает комплексную обработку ошибок:
- Автоматическое переключение в безопасный режим при сбоях
- Логирование всех ошибок
- Попытки автоматического восстановления
- Уведомления о критических ошибках

## 📈 Мониторинг и логирование

### Данные в базе
- История всех изменений состояний
- Временные метки всех операций
- Параметры производственных процессов
- Связь между устройствами и процессами

### Визуализация
- Графики в реальном времени
- Эталонные линии для контроля
- Цветовая индикация состояний
- Динамическое обновление данных
