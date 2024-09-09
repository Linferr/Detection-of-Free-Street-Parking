import threading
from ServerPredefined import haversine, createInsertRequest, post_to_mongodb

EDGE_DEVICE_ID = "666"

# This cache will remove stored value timeout seconds after the put operation
class timeCache:
    def __init__(self, timeout, second_level_cache):
        self.storage = []
        self.timeout = timeout
        self.second_level_cache = second_level_cache

    def put(self, data):
        self.storage.append(data)
        timer = threading.Timer(self.timeout, self.removePut, args=(data,))
        timer.start()

    def removePut(self, data):
        for item in self.storage:
            if item == data:
                self.second_level_cache.put(item)
                insert_api_url, headers, insert_body = createInsertRequest(EDGE_DEVICE_ID, item)
                response_text = post_to_mongodb(insert_api_url, headers, insert_body)
                print("Response from MongoDB:", response_text)
                    
                self.storage.remove(item)
                
                break
                    

# This is for the second-level cahce
class normalCache:
    def __init__(self):
        self.storage = []

    def put(self, data):
        self.storage.append(data)

    def remove(self, data):
        for item in self.storage:
            if item == data:
                    
                self.storage.remove(item)
                
                break
    
    def removeRedundantLocation(self, new_location):
        replaced_locations = []
        for old_location in self.storage:
            if haversine(old_location[0], old_location[1], new_location[0], new_location[1]) < 2:
                    
                self.storage.remove(old_location)
                replaced_locations.append(old_location)
            
        return replaced_locations            
            