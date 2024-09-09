import serial		
import time

PORT = "COM3"
BAURATE = 115200

ser = serial.Serial(PORT, BAURATE, timeout=1)

while True:
    ser.write("data".encode('utf-8'))
    print("data is sent")
    time.sleep(0.5)