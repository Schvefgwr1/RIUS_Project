from PLKMessagesDevices import setCommandToPLC, getStateFromPLC
from time import sleep


class DeviceAutomate:
    def __init__(self, name, sensor, reference_state_on, reference_state_off, dev_type):
        self.name = name
        self.sensor = sensor
        self.sensor.setDevice(self)
        self.state = "initial"
        self.reference_state_on = reference_state_on
        self.reference_state_off = reference_state_off
        self.message = ""
        self.type_d = dev_type
        self.parameter = -1

    def setCommand(self, command):
        if command in ["on", "off"]:
            self.state = command
        else:
            self.state = "error"
            return {
                "state": self.state,
            }
        try:
            setCommandToPLC(self.name, command)
        except Exception as e:
            self.state = "error"
            print(e)
            return {
                "state": self.state,
            }
        sleep(2)
        try:
            get_state = getStateFromPLC(self)
            self.parameter = get_state
        except Exception as e:
            self.state = "error"
            print(e)
            return {
                "state": self.state,
            }
        if ((command == "on" and get_state != self.reference_state_on)
                or (command == "off" and get_state != self.reference_state_off)):
            self.state = "error"
        return {
            "state": self.state,
        }

    def checkState(self):
        if self.state == "initial":
            self.message = "Initialisation in process"
        if self.state == "on":
            self.message = "Device is working"
        if self.state == "off":
            self.message = "Device is not working"
        if self.state == "error":
            self.message = "Error of device"
        return {
            "message": self.message,
            "state": self.state
        }

    def updateState(self):
        if self.state == "initial":
            try:
                getStateFromPLC(self)
                self.state = "off"
            except Exception as e:
                print(e)
                self.state = "error"
        else:
            if self.state == "off":
                if self.sensor.state == "bad":
                    self.setCommand("on")
            else:
                if self.state == "on":
                    if self.sensor.state == "good":
                        self.setCommand("off")
                else:
                    if self.state == "error":
                        sleep(2)
                        self.state = "initial"
        if self.sensor.state == "error" or self.sensor.state == "initial":
            if self.state == "on":
                self.setCommand("off")
        return {
            "state": self.state
        }
