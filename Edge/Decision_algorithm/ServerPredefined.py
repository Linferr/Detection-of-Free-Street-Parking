import math
import requests
from datetime import datetime, timezone

INSERT_API_URL = "https://ap-southeast-1.aws.data.mongodb-api.com/app/data-eplbb/endpoint/data/v1/action/insertOne"
INSERT_API_KEY = "codqN8SQIUEuA4Q4ADCWmc3xnb7E4vr8otm2urWstPbl1LpONuputENzp7s5F9wv"

REPLACE_API_URL = "https://ap-southeast-1.aws.data.mongodb-api.com/app/data-eplbb/endpoint/data/v1/action/replaceOne"
REPLACE_API_KEY = "codqN8SQIUEuA4Q4ADCWmc3xnb7E4vr8otm2urWstPbl1LpONuputENzp7s5F9wv"

def haversine(lat1, lon1, lat2, lon2):
    R = 6371000 
    phi1 = math.radians(lat1)
    phi2 = math.radians(lat2)
    delta_phi = math.radians(lat2 - lat1)
    delta_lambda = math.radians(lon2 - lon1)

    a = math.sin(delta_phi / 2) ** 2 + math.cos(phi1) * math.cos(phi2) * math.sin(delta_lambda / 2) ** 2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))

    distance = R * c
    return distance

def post_to_mongodb(api_url, headers, body):
    """
    Posts data to a MongoDB Atlas collection using a REST API.

    :param api_url: URL for the MongoDB Atlas REST API endpoint.
    :param headers: Dictionary containing request headers.
    :param body: Dictionary containing the request body.
    :return: Response from the API as a string.
    """
    response = requests.post(api_url, json=body, headers=headers)
    return response.text

def createInsertRequest(edgedevice, location_data):
    # MongoDB Atlas REST API URL for inserting data
    insert_api_url = INSERT_API_URL

    # Headers for the API request
    headers = {
        "api-key": INSERT_API_KEY,
        "Content-Type": "application/json"
    }

    # Body for the POST request to insert data
    insert_body = {
        "collection": "availableParking",
        "database": "demoDB",
        "dataSource": "Cluster0",
        "document": {
            "location": location_data,
            'edgedevice': edgedevice,
            "timestamp": datetime.now(timezone.utc).isoformat(), # Current UTC time in ISO 8601 format
            "isValid": 1 # Document validity status: 0 for invalid, 1 for valid
        }
    }
    
    return insert_api_url, headers, insert_body

def createReplaceRequest(edgedevice_id, new_location):
    # MongoDB Atlas REST API URL for replacing or inserting data
    
    replace_api_url = REPLACE_API_URL
    # Headers for the API request
    headers = {
        "api-key": REPLACE_API_KEY,  # Your MongoDB Atlas API key here
        "Content-Type": "application/json"
    }
    
    # Body for the POST request to replace or insert a new document
    replace_body = {
        "collection": "availableParking",
        "database": "demoDB",
        "dataSource": "Cluster0",
        "filter": {
            "edgedevice": edgedevice_id,
            "location": {
                "$near": {
                    "$geometry": {
                        "type": "Point",
                        "coordinates": new_location
                    },
                    "$maxDistance": 2  # 2 meters
                }
            }
        },
        "replacement": {
            "location": new_location,
            "edgedevice": edgedevice_id,
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "isValid": 0  # Document validity status: 0 for invalid, 1 for valid
        },
        # "upsert": True  # Insert a new document if no matching document is found
    }

    return replace_api_url, headers, replace_body

def checkRepeatedLocation(location_list, new_location):
    for each_location in location_list:
        if haversine(each_location[0], each_location[1], new_location[0], new_location[1]) < 6:
            return True
        
    return False

def isValid(location):
    if location[2] == 1:
        return True

    return False