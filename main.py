from tkinter import *
from tkinter import ttk
from serial import Serial
from datetime import datetime
import protocol
import mac
import math

GRAVITY = 9.80655

RADIUS = 0.6 #단위 m
targetDistance = 50
maxDistance = 1000
velocity = 100

RPS = 12 #Rotation Per Second
FONT_DIGIT = ("DS-Digital Bold Italic", 40)

try:
	port = 9600
	com = mac.macFinder()
	ser = Serial(com, port, timeout=0.2)
except:
	print("시리얼 연결 실패")
	exit()

# ====== tkinter 버튼 관련 =======
def sendSetDistance():
	global DistanceString, targetDistance
	try:
		targetDistance = int(DistanceString.get())
	except:
		return
	if targetDistance < 0 or targetDistance > maxDistance:
		addLog(f"거리 설정 실패 / 0 ~ {int(maxDistance)} 사이에 {targetDistance}가 없음.")
		return
	
	# protocol.setDistance(ser, targetDistance)
	addLog(f"거리 설정 : {targetDistance} cm")

def sendMotorHold():
	protocol.motorHold(ser)
	addLog(f"모터 잡기")

def sendMotorReleased():
	protocol.motorReleased(ser)
	addLog(f"모터 풀기")

def sendShoot():
	protocol.shoot(ser)
	addLog(f"발사 | 거리 : {targetDistance} cm | 속력 : {2 * math.pi * RADIUS * RPS} m/s")

# ====== 위젯 관련 ======
def addStaticLabel(root, txt : str, width = None) -> None:
	"""
	정적 라벨 생성
	"""
	if width == None:
		lbl = Label(root, text=txt)
	else:
		lbl = Label(root, text=txt, width=width)
	lbl.pack()

def addSpace(root) -> None:
	"""
	엔터 공간 만들기
	"""
	addStaticLabel(root, " ")
	addStaticLabel(root, " ")

def addLog(txt : str):
	"""
	로그 기록
	"""
	logBox.insert(END, f"[{datetime.now().strftime('%H:%M:%S')}] {txt}\n")
	logBox.yview(END)

def setLabelDatas(RPSLabelString : StringVar,
				  RPMLabelString : StringVar,
				  SpeedLabelString : StringVar,
				  MaxSpeedLabelString : StringVar,
				  RPS : int):
	"""
	데이터 받은 거 시각화
	"""
	global velocity, maxDistance

	RPSLabelString.set(f"{str(RPS).zfill(4)} RPS")
	RPMLabelString.set(f"{str(RPS * 60).zfill(4)} RPM")
	velocity = 2 * math.pi * RADIUS * RPS
	SpeedLabelString.set(f"{int(velocity*100)/100} m/s")
	maxDistance = velocity*velocity/GRAVITY
	MaxSpeedLabelString.set(f"{int(maxDistance)} m")


root = Tk()
root.geometry("500x800")
root.title("SpinLaunch 관리 시스템")



# 현재 데이터를 보여주는 프레임 생성
labelFrameData=LabelFrame(root, text="Data")

# 초당 회전 수
addStaticLabel(labelFrameData, "RPS ( 초당 회전 수 [n] )", 60)
RPSLabelString = StringVar()
RPSLabel = Label(labelFrameData, textvariable=RPSLabelString, font = FONT_DIGIT)
RPSLabel.pack()
addSpace(labelFrameData)

# 분당 회전 수
addStaticLabel(labelFrameData, "RPM ( 분당 회전 수 [n] )", 60)
RPMLabelString = StringVar()
RPMLabel = Label(labelFrameData, textvariable=RPMLabelString, font = FONT_DIGIT)
RPMLabel.pack()
addSpace(labelFrameData)

# 현재 속력
addStaticLabel(labelFrameData, "Speed ( 속력 [m/s] )", 60)
SpeedLabelString = StringVar()
SpeedLabel = Label(labelFrameData, textvariable=SpeedLabelString, font = FONT_DIGIT)
SpeedLabel.pack()

# 가능한 최대 거리
addStaticLabel(labelFrameData, "Max Distance ( 최대 거리 [m] )")
MaxSpeedLabelString = StringVar()
MaxSpeedLabelString.set("0 m")
MaxSpeedLabel = Label(labelFrameData, textvariable=MaxSpeedLabelString)
MaxSpeedLabel.pack()

# 라벨들의 데이터 설정
setLabelDatas(RPSLabelString, RPMLabelString, SpeedLabelString, MaxSpeedLabelString, RPS)
labelFrameData.pack()



# 컨트롤을 담당하는 프레임 생성
labelFrameControler=LabelFrame(root, text="Controler")

# 거리 설정
addStaticLabel(labelFrameControler, "Distance ( 거리 [cm] )", 60)
DistanceString = StringVar()
DistanceString.set(str(targetDistance))
DistanceBox = ttk.Spinbox(labelFrameControler, from_=0, to=9999, textvariable=DistanceString)
DistanceBox.pack()
DistanceButton = Button(labelFrameControler, text="거리 설정하기", width=20, command=sendSetDistance)
DistanceButton.pack()
addSpace(labelFrameControler)

# 모터 홀드 버튼
MotorHoldButton = Button(labelFrameControler, text="모터 잡기 ( Hold )", width=20, command=sendMotorHold)
MotorHoldButton.pack()

# 모터 릴리즈 버튼
MotorReleasedButton = Button(labelFrameControler, text="모터 풀기 ( Released )", width=20, command=sendMotorReleased)
MotorReleasedButton.pack()
addSpace(labelFrameControler)

# 발사 버튼
addStaticLabel(labelFrameControler, "※ 주의! 반드시 발사 전, 사람들에게 위험을 알리세요.", 60)
addStaticLabel(labelFrameControler, "반드시 거리 설정 이후 발사를 진행해야합니다.", 60)
ShootButton = Button(labelFrameControler, text="발사", command=sendShoot, width=20)
ShootButton.pack()

labelFrameControler.pack()


# 로그 기록
addStaticLabel(root, "로그")
logBox = Text(root, height=7, width=70)
logBox.pack()
addLog("시스템 시작")

while True:
	root.update()

	SerialText = ser.readline().decode("UTF-8") #데이터 받기
	if SerialText != "":
		RPS = int(SerialText)