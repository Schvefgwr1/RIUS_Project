from orm import Table, get_table
import datetime
import MySQLdb


def initialisation_database():
    try:
        Table.connect(config_dict={
            'host': 'localhost',
            'port': 3306,
            'user': 'root',
            'password': '12353890',
            'database': 'hleb'
        })
    except Exception as e:
        return e

    try:
        Devices = get_table('devices')
        DevicesStates = get_table('devices_states')
        DevicesTypes = get_table('devices_types')
        ProcessesDevicesKeys = get_table('processes_devices_keys')
        ProductionProcessDesc = get_table('production_process_desc')
        Sensors = get_table('sensors')
        SensorsStates = get_table('sensors_states')
        SensorsTypes = get_table('sensors_types')

        return {
            "Devices": Devices,
            "DevicesStates": DevicesStates,
            "DevicesTypes": DevicesTypes,
            "ProcessesDevicesKeys": ProcessesDevicesKeys,
            "ProductionProcessDesc": ProductionProcessDesc,
            "Sensors": Sensors,
            "SensorsStates": SensorsStates,
            "SensorsTypes": SensorsTypes
        }
    except Exception as e:
        return e


tables = initialisation_database()


def setSensorsType(type_sensor):
    try:
        return tables.get("SensorsTypes").create(type_name=type_sensor).save()
    except Exception as e:
        return e


def setDevicesType(type_device):
    try:
        return tables.get("DevicesTypes").create(type_name=type_device).save()
    except Exception as e:
        return e


def setDevice(device_name,
              device_state,
              device_parameter,
              device_type
              ):
    try:
        type_id = tables.get("DevicesTypes").where(type_name=device_type)[0].type_id
        return tables.get("Devices").create(
            device_name=device_name,
            device_state_work=device_state,
            device_parameter=device_parameter,
            type_id=type_id
        ).save()
    except Exception as e:
        return e


def setSensor(sensor_name,
              type_name,
              etalon_1,
              etalon_2,
              actual_parameter,
              device_name
              ):
    try:
        type_id = tables.get("SensorsTypes").where(type_name=type_name)[0].type_id
        device_id = tables.get("Devices").where(device_name=device_name)[0].device_id
        return tables.get("Sensors").create(
            sensor_name=sensor_name,
            type_id=type_id,
            etalon_1=etalon_1,
            etalon_2=etalon_2,
            actual_parameter=actual_parameter,
            device_id=device_id
        ).save()
    except Exception as e:
        return e


def setDeviceState(
        state_param,
        state_work,
        state_time,
        device_name
):
    try:
        device = tables.get("Devices").where(device_name=device_name)[0]
        connect = MySQLdb.connect('localhost', 'root', '12353890', 'hleb')
        cursor = connect.cursor()
        cursor.execute("UPDATE devices "
                       f"SET device_parameter={state_param}, "
                       f"device_state_work={state_work} "
                       f"WHERE device_id={device.device_id};")
        connect.commit()
        connect.close()

        return tables.get("DevicesStates").create(
            state_param=state_param,
            state_work=state_work,
            state_time=state_time,
            device_id=device.device_id
        ).save()
    except Exception as e:
        return e


def setSensorState(
        state_param,
        state_work,
        state_time,
        sensor_name
):
    try:
        sensor = tables.get("Sensors").where(sensor_name=sensor_name)[0]
        connect = MySQLdb.connect('localhost', 'root', '12353890', 'hleb')
        cursor = connect.cursor()
        cursor.execute("UPDATE sensors "
                       f"SET actual_parameter={state_param} "
                       f"WHERE sensor_id={sensor.sensor_id};")
        connect.commit()
        connect.close()

        return tables.get("SensorsStates").create(
            state_param=state_param,
            state_work=state_work,
            state_time=state_time,
            sensor_id=sensor.sensor_id
        ).save()
    except Exception as e:
        return e


def setProcessDescription(
        process_name,
        process_desc,
        start_time,
        stop_time,
        device_name
):
    try:
        device_id = tables.get("Devices").where(device_name=device_name)[0].device_id
        tables.get("ProductionProcessDesc").create(
            process_name=process_name,
            process_desc=process_desc,
            start_time=start_time,
            stop_time=stop_time
        ).save()
        process_id = tables.get("ProductionProcessDesc").where(
            process_name=process_name,
            start_time=start_time
        )[0].desc_id
        tables.get("ProcessesDevicesKeys").create(
            process_id=process_id,
            device_id=device_id
        ).save()
        return True
    except Exception as e:
        return e


def setProcess(
        process_name,
        process_desc,

        device_actual_param,
        device_name,
        device_state_work,

        sensor_name,
        sensor_actual_parameter,
        sensor_state_work,
):
    try:
        start_time = datetime.datetime.now()

        setSensorState(
            sensor_actual_parameter,
            sensor_state_work,
            start_time,
            sensor_name
        )

        setDeviceState(
            device_actual_param,
            device_state_work,
            start_time,
            device_name
        )

        stop_time = datetime.datetime.now()

        setProcessDescription(
            process_name,
            process_desc,
            start_time,
            stop_time,
            device_name
        )
        return True
    except Exception as e:
        return e


def getSensor(device_name):
    try:
        device_id = tables.get("Devices").where(device_name=device_name)[0].device_id
        return tables.get("Sensors").where(device_id=device_id)[0]
    except Exception as e:
        return e


def getDevice(device_name):
    try:
        return tables.get("Devices").where(device_name=device_name)[0]
    except Exception as e:
        return e


def updateEtalons(sensor_id, etalon1, etalon2):
    try:
        connect = MySQLdb.connect('localhost', 'root', '12353890', 'hleb')
        cursor = connect.cursor()
        cursor.execute("UPDATE sensors "
                       f"SET etalon_1={etalon1}, "
                       f"etalon_2={etalon2} "
                       f"WHERE sensor_id={sensor_id};")
        connect.commit()
        connect.close()
    except Exception as e:
        return e
