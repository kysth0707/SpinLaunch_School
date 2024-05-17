import serial.tools.list_ports as serialPorts
def macFinder():
	dev = serialPorts.comports()
	port = []
	for com in dev:
		port.append((com.device, com.hwid))
	
	macAddress = '44441B04048F'

	for device in port:
		if macAddress in device[1]:
			result = str(device[0])
	
	return result