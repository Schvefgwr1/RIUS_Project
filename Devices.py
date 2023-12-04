from DeviceAutomate import DeviceAutomate
from Sensors import initializationSensors

devices = [
    ["servoOpenCloseTank", "tankLevelSensor", 100, 0, "Servo"],
    ["coolerOnOffCistern", "cisternTemperatureSensor", 1, 0, "Cooler"],
    ["servoOpenCloseConstTank", "const_tankLevelSensor", 100, 0, "Servo"],
    ["servoOpenCloseDoughMachine", "dough_machineTimeSensor", 100, 0, "Servo"],
    ["heaterOnOffDoughMachine", "dough_machineTemperatureSensor", 1, 0, "Heater"],
    ["heaterOnOffCloset", "closetTemperatureSensor", 1, 0, "Heater"],
    ["humidifierOnOffCloset", "closetWetSensor", 1, 0, "Humidifier"],
    ["heaterOnOffBake", "bakeTemperatureSensor", 1, 0, "Heater"]
]


def find_for_name(array, name):
    for obj in array:
        if obj.name == name:
            return obj
    return None


def initialisationDevices():
    devices_objects = []
    sensors_objects = initializationSensors()
    for device in devices:
        devices_objects.append(
            DeviceAutomate(
                device[0],
                find_for_name(sensors_objects, device[1]),
                device[2],
                device[3],
                device[4]
            )
        )
    return devices_objects
