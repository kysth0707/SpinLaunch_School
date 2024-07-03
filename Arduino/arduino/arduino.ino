#include <SoftwareSerial.h>
#include <Servo.h>


SoftwareSerial BTSerial(4, 5);
Servo ballServo;

#define ServoPIN 7
#define IRSensorPIN 8

#define ReleaseAngle 30
#define HoldAngle 120

const bool MOTOR_RELEASE = false;
const bool MOTOR_HOLD = true;

bool motorState = false;
bool lastMotorState = false;

void setup() 
{
    //시리얼과 블루투스 시리얼 연결
    BTSerial.begin(9600);

    //모터 초기화 및 기본 테스트
    ballServo.attach(ServoPIN);
    delay(1000);
    ballServo.write(ReleaseAngle);
    delay(1000);
    ballServo.write(HoldAngle);
    delay(1000);
    ballServo.write(ReleaseAngle);
    motorState = MOTOR_RELEASE;

    //IR 센서 모드 설정
    pinMode(IRSensorPIN, INPUT);
}

void loop() 
{
    checkSerial();
    setMotor();
}

void checkSerial()
{
    char commandCode = BTSerial.read();
    switch (commandCode)
    {
        case 'lD':
            //set distance
            //code Here

        break;

        case 'S':
            //set distance
            //code Here

        break;

        case 'G':
            //get Data
            //code Here

        break;

        case 'H':
            //motor Hold
            motorState = MOTOR_HOLD;
        break;

        case 'R':
            //motor Release
            motorState = MOTOR_RELEASE;
        break;
    }
}

void setMotor()
{
    if(lastMotorState == motorState) { return; }
    if(motorState == MOTOR_HOLD)
    {
        ballServo.write(HoldAngle);
    }
    else
    {
        ballServo.write(ReleaseAngle);
    }
    lastMotorState = motorState;
}


/*
#include <SoftwareSerial.h> //블루투스 관련 라이브러리

SoftwareSerial BTSerial(4, 5); //RXD 4번핀, TXD 5번핀으로 이용
//R : Receive 수신, T : Transmit 송신

void setup() 
{
    //블루투스와 시리얼을 초기화
    Serial.begin(9600);
    BTSerial.begin(9600);
}

void loop() 
{
    //블루투스 -> 시리얼
    if(BTSerial.available())
        Serial.write(BTSerial.read());

    //시리얼 -> 블루투스
    if(Serial.available())
        BTSerial.write(Serial.read());
}
*/