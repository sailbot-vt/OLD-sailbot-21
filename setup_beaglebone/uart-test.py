import Adafruit_BBIO.UART as UART
import serial

UART.setup("UART1")
UART.setup("UART2")

ser = serial.Serial(port = "/dev/ttyO1", baudrate=9600)
ser.close()
ser.open()
ser2 = serial.Serial(port = "/dev/ttyO2", baudrate=9600)
ser2.close()
ser2.open()

if ser.isOpen():
    print("ttyO1 is open")
    ser.write(b"Hello World!\n")

if ser2.isOpen():
    print("ttyO2 is open")

print(ser2.readline())
ser2.close()