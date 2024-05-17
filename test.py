from serial import Serial
import time
import mac

try:
	port = 9600
	com = mac.macFinder()
	# com = "COM8"
	ser = Serial(com, port, timeout=0.2)
except:
	print("시리얼 연결 실패")
	exit()

lastTime = 0
while True:
	if time.time() - lastTime > 1:
		ser.write("a".encode())
		lastTime = time.time()

	SerialText = ser.readline().decode("UTF-8")

	if SerialText != "":
		print(SerialText)