import serial

SERIAL_PORT = 'COM5'
BAUD_RATE = 115200

ser = serial.Serial(SERIAL_PORT, BAUD_RATE)

while True:
    if ser.in_waiting > 0:
        line = ser.readline().decode('utf-8').rstrip()
        print(f"Read line: {line}")
        
        
