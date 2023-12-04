from SensorAutomate import SensorAutomate

sensors = [
    ["tankLevelSensor", 20, 100, "Level"],
    ["cisternTemperatureSensor", 16, 20, "Temperature"],
    ["const_tankLevelSensor", 100, 100, "Level"],
    ["dough_machineSpeedSensor", 55, 65, "Speed"],
    ["dough_machineTimeSensor", 0, 12, "Time"],
    ["dough_machineTemperatureSensor", 50, 60, "Temperature"],
    ["closetTemperatureSensor", 35, 40, "Temperature"],
    ["closetWetSensor", 70, 80, "Wet"],
    ["bakeTemperatureSensor", 120, 130, "Temperature"]
]


def initializationSensors():
    sensors_objects = []
    for sensor in sensors:
        sensors_objects.append(SensorAutomate(sensor[1], sensor[2], sensor[0], sensor[3]))
    return sensors_objects

