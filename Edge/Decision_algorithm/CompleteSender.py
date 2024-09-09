import torch
import threading
import time
import serial				
from SenderPredefined import predict																												
																																										       

if torch.cuda.is_available():
    print("CUDA is available. Using GPU for acceleration.")
else:
    print("CUDA not available. Using CPU.")

MODEL_PATH = r"F:\Courses\CPEN491\best.pt"
BAURATE = 115200
PORT = "COM3"
WINDOW_SIZE = [1280, 960] # For checking the processed video

# Currently, the system uses the video in the given video path. To use camera, simply set this to be 0.
VIDEO_PATH = r"F:\Courses\CPEN491\IMG_8006.MOV"
OUT_PATH = r'F:\Courses\CPEN491\Video\detect_video1.MOV'
VALID_LOCATION = '[11,12,1]' # location example
Reference_Frequency = 0.5
writing_lock = threading.Lock()


def sendReferenceLocation():
    while True:
        writing_lock.acquire()
        ser.write('[11,12,0]'.encode('utf-8'))
        writing_lock.release()
        time.sleep(Reference_Frequency)  # Sleep for 2 seconds

if __name__ == '__main__':
    ser = serial.Serial(PORT, BAURATE, timeout=1)
    
    # This is the second method for sending reference locations, which initiates another thread and send it periodically.
    # It has lower performance in current testing. However, it enhances flexibility.
    # # Another thread sending reference locations
    # thread = threading.Thread(target=sendReferenceLocation)
    # thread.daemon = True
    # thread.start()
    
    predict(VALID_LOCATION, ser, MODEL_PATH, WINDOW_SIZE, writing_lock, VIDEO_PATH, OUT_PATH)
    
    