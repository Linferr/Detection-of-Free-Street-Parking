import requests
from datetime import datetime, timezone

def post_to_mongodb(api_url, headers, body):
    """
    Posts data to a MongoDB Atlas collection using a REST API.
    If a document with the same 'edgedevice' identifier and a nearby location exists,
    it replaces that document.

    :param api_url: URL for the MongoDB Atlas REST API endpoint.
    :param headers: Dictionary containing request headers.
    :param body: Dictionary containing the request body.
    :return: Response from the API as a string.
    """
    response = requests.post(api_url, json=body, headers=headers)
    return response.text

def main():
    # MongoDB Atlas REST API URL for replacing or inserting data
    replace_api_url = "https://ap-southeast-1.aws.data.mongodb-api.com/app/data-eplbb/endpoint/data/v1/action/replaceOne"

    # Headers for the API request
    headers = {
        "api-key": "codqN8SQIUEuA4Q4ADCWmc3xnb7E4vr8otm2urWstPbl1LpONuputENzp7s5F9wv",  # Your MongoDB Atlas API key here
        "Content-Type": "application/json"
    }

    # Define the new document's location
    new_location = [-123.2483458, 49.2609203]
    edgedevice_id = '6' # The id of the device # to do
    
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

    # Replace an existing document or insert a new one into the MongoDB collection
    response_text = post_to_mongodb(replace_api_url, headers, replace_body)
    print("Response from MongoDB:", response_text)

if __name__ == '__main__':
    main()
