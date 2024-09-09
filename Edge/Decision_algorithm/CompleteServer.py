import json
import serial
import re
import threading
import sys

sys.path.insert(0, r"F:\Courses\CPEN491\Decision_algorithm")
from ServerPredefined import haversine, post_to_mongodb, createInsertRequest, createReplaceRequest, checkRepeatedLocation, isValid
from Cache import timeCache, normalCache, EDGE_DEVICE_ID

# This buffer will store the unprocessed location strings
string_buffer = ""

buffer_lock = threading.Lock()
# SERIAL_PORT = '/dev/ttyUSB0'
SERIAL_PORT = 'COM5'
BAUD_RATE = 115200

second_level_cache = normalCache()
first_level_cache = timeCache(2, second_level_cache)

def process_data():
    global string_buffer
    while True:
        buffer_lock.acquire()
        
        # Split the string buffer into locations
        if '[' in string_buffer and ']' in string_buffer:
            start_index = string_buffer.index('[')
            end_index = string_buffer.index(']', start_index) + 1
            data_to_process = string_buffer[start_index:end_index]
            string_buffer = string_buffer[end_index:]
            
            print(f"Processing: {data_to_process}")
            
            # Convert the string to an int list
            location_data_v = json.loads(data_to_process)
            location_data = [location_data_v[0],location_data_v[1]]
            
            # Check if this location is within 6 meters of another one, also check whether it is a valid location or a ref location
            if isValid(location_data_v):
                if not checkRepeatedLocation(first_level_cache.storage, location_data):
                    first_level_cache.put(location_data)
            
            elif not isValid(location_data_v):
                # Go to second_level_cache and delete the valid location
                # If the car indead detects that there is an available parking space, that valid location will be stored after this deletion
                replaced_locations = second_level_cache.removeRedundantLocation(location_data)
                print(f"replaced_location: {replaced_locations}")
                
                # This strategy cannot filter out all the redundant locations when a car stops for a long time. However, it still significantly reduce the burden of the cloud.
                # To make the strategy resolve this issue, simply invalidate all the locations in replaced_locations. However, this will harm the efficiency.
                if len(replaced_locations) > 0:
                    # Send invalid to the cloud
                    replace_api_url, headers, replace_body = createReplaceRequest(EDGE_DEVICE_ID, replaced_locations[0])
                    response_text = post_to_mongodb(replace_api_url, headers, replace_body)
                    print("Response from MongoDB:", response_text)
                    
        buffer_lock.release()

# This function helps the system to read the buffer information. This is because the reading buffer won't perfectly match the length of a message.
# For example, the first line can be "[11,12,1][11" and the second can be ",12,1]"
def read_serial():
    global string_buffer
    serial_port = SERIAL_PORT
    baud_rate = BAUD_RATE
    ser = serial.Serial(serial_port, baud_rate)

    # Get valid location data from uncontinuous messages from the sender
    try:
        while True:
            if ser.in_waiting > 0:
                line = ser.readline().decode('utf-8').rstrip()
                matches_valid = re.findall(r'"([^"]*)"', line)
                
                buffer_lock.acquire()
                for match_valid in matches_valid:
                    string_buffer += match_valid
                
                
                buffer_lock.release()
    except KeyboardInterrupt:
        print("Serial reading terminated")
    finally:
        ser.close()

# Start the thread for processing data
data_processor = threading.Thread(target=process_data, daemon=True)
data_processor.start()

# Start reading from serial
read_serial()
