from serial import Serial

def setDistance(ser : Serial, centimeter : int) -> None:
	"""
	거리 설정
	"""
	if centimeter < 0 or centimeter > 9999:
		return
	
	ser.write(f"D{str(centimeter).zfill(4)}".encode())

def shoot(ser : Serial) -> None:
	"""
	발사
	"""
	ser.write("S".encode())

def getData(ser : Serial) -> None:
	"""
	데이터 호출
	"""
	ser.write("G".encode())

def motorHold(ser : Serial) -> None:
	"""
	모터 홀드 (공 잡은 상태)
	"""
	ser.write("H".encode())

def motorReleased(ser : Serial) -> None:
	"""
	모터 품 (공 날린 상태)
	"""
	ser.write("R".encode())