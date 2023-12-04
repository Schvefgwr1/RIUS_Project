from random import randint


def PLKSensors(sensor, device):
    sensors = [
        ["tankLevelSensor", 20, 100],
        ["cisternTemperatureSensor", 16, 20],
        ["const_tankLevelSensor", 100, 100],
        ["dough_machineSpeedSensor", 55, 65],
        ["dough_machineTimeSensor", 0, 12],
        ["dough_machineTemperatureSensor", 50, 60],
        ["closetTemperatureSensor", 35, 40],
        ["closetWetSensor", 70, 80],
        ["bakeTemperatureSensor", 120, 130]
    ]

    if sensor.parameter is None or device.state == "initial":
        sen = ""
        for sens in sensors:
            if sens[0] == sensor.name:
                sen = sens
        return randint(sen[1], sen[2])

    match sensor.name:
        case "tankLevelSensor":
            match device.state:
                case "on":
                    return sensor.parameter - 1
                case "off":
                    return sensor.parameter + 1
        case "cisternTemperatureSensor":
            match device.state:
                case "on":
                    return sensor.parameter - 1
                case "off":
                    return sensor.parameter + 1
        case "const_tankLevelSensor":
            match device.state:
                case "on":
                    return sensor.parameter - 1
                case "off":
                    return sensor.parameter + 1
        case "dough_machineSpeedSensor":
            return sensor.parameter
        case "dough_machineTimeSensor":
            match device.state:
                case "on":
                    return 0
                case "off":
                    return sensor.parameter + 1
        case "dough_machineTemperatureSensor":
            match device.state:
                case "on":
                    return sensor.parameter + 1
                case "off":
                    return sensor.parameter - 1
        case "closetTemperatureSensor":
            match device.state:
                case "on":
                    return sensor.parameter + 1
                case "off":
                    return sensor.parameter - 1
        case "closetWetSensor":
            match device.state:
                case "on":
                    return sensor.parameter + 1
                case "off":
                    return sensor.parameter - 1
        case "bakeTemperatureSensor":
            match device.state:
                case "on":
                    return sensor.parameter + 1
                case "off":
                    return sensor.parameter - 1
