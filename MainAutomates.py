from Devices import initialisationDevices
from Database import setDevice, setDevicesType, setSensor, setSensorsType, setProcess, getSensor


def main():

    devices = initialisationDevices()

    setDevicesType("Servo")
    setDevicesType("Cooler")
    setDevicesType("Heater")
    setDevicesType("Humidifier")

    setSensorsType("Level")
    setSensorsType("Temperature")
    setSensorsType("Speed")
    setSensorsType("Time")
    setSensorsType("Wet")

    for device in devices:
        setDevice(
            device.name,
            0,
            device.message,
            device.type_d
        )
        setSensor(
            device.sensor.name,
            device.sensor.type_s,
            device.sensor.control1,
            device.sensor.control2,
            device.sensor.parameter,
            device.name
        )

    k = 0

    while True:
        k += 1
        message = []
        for device in devices:
            db_sensor = getSensor(device.name)
            if db_sensor:
                device.sensor.control1 = db_sensor.etalon_1
                device.sensor.control2 = db_sensor.etalon_2
            device.sensor.updateState()
            device.sensor.checkState()
            device.updateState()
            device.checkState()
            if device.state == "off" or device.state == "initial" or device.state == "error":
                device_st_l = 0
            else:
                device_st_l = 1
            if device.sensor.state == "init" or device.sensor.state == "error":
                sensor_st_l = 0
            else:
                sensor_st_l = 1
            message.append({
                "device.name": device.name,
                "device.state": device.state,
                "device.message": device.message,
                "sensor.message": device.sensor.message,
                "sensor.state": device.sensor.state
            })
            setProcess(
                device.name + str(k),
                device.message + " " + device.sensor.message,

                device.parameter,
                device.name,
                device_st_l,

                device.sensor.name,
                device.sensor.parameter,
                sensor_st_l
            )
        print(message, "\n\n\n")


if __name__ == '__main__':
    main()
