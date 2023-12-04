def setCommandToPLC(name_device, command):
    print(name_device, command)
    return 14


def getStateFromPLC(device):
    match device.state:
        case "on":
            return device.reference_state_on
        case "off":
            return device.reference_state_off
        case "error":
            return Exception
