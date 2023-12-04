from PLKMessagesSensors import PLKSensors
from time import sleep


class SensorAutomate:
    def __init__(self, control1, control2, name, sen_type):
        self.parameter = 0
        self.name = name
        self.control1 = control1
        self.control2 = control2
        self.state = "init"
        self.message = ""
        self.device = None
        self.type_s = sen_type

    def setDevice(self, device):
        self.device = device

    def updateState(self):
        try:
            self.parameter = PLKSensors(self, self.device)
            if self.control1 <= self.parameter <= self.control2:
                self.state = "good"
            else:
                self.state = "bad"
        except Exception as e:
            self.state = "error"
            print(e)
        return {
            "state": self.state,
            "parameter": self.parameter
        }

    def checkState(self):
        if self.state == "init":
            if self.updateState()["state"] != "error":
                self.message = "Initialisation was successful"
            else:
                self.message = "Initialisation was unsuccessful"
        if self.state == "good":
            self.message = "Parameter in target values"
        if self.state == "bad":
            self.message = "Parameter not in target values"
        if self.state == "error":
            self.message = "Error of sensor"
            sleep(2)
            self.state = "init"
        return {
            "message": self.message,
            "state": self.state
        }
