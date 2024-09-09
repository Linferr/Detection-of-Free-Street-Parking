import requests
from datetime import datetime, timezone

def post_to_mongodb(api_url, headers, body):
    """
    Sends a POST request to a MongoDB Atlas API to insert a document into a specified collection.
    
    Parameters:
        api_url (str): The complete URL to the MongoDB Atlas REST API endpoint for data insertion.
        headers (dict): A dictionary containing the headers to be sent with the request, including authorization and content type.
        body (dict): A dictionary representing the JSON payload to be sent, specifying the database, collection, data source, and the document to insert.
        
    Returns:
        str: The API response as a string, which typically contains information about the success or failure of the operation.
    """
    response = requests.post(api_url, json=body, headers=headers)
    return response.text

def main():
    # URL for the MongoDB Atlas REST API endpoint specifically configured for inserting documents
    insert_api_url = "https://ap-southeast-1.aws.data.mongodb-api.com/app/data-eplbb/endpoint/data/v1/action/insertOne"

    # Authorization and content-type headers for the API request
    headers = {
        "api-key": "codqN8SQIUEuA4Q4ADCWmc3xnb7E4vr8otm2urWstPbl1LpONuputENzp7s5F9wv",  # Your MongoDB Atlas API key needs to be inserted here
        "Content-Type": "application/json"
    }

    # Constructing the JSON payload for the POST request to insert a new document into the collection
    insert_body = {
        "collection": "availableParking",
        "database": "demoDB",
        "dataSource": "Cluster0",
        "document": {
            "location": [-123.247120, 49.261005],  # GPS coordinates of the parking location
            "edgedevice": '7',  # Identifier for the edge device reporting the data
            "timestamp": datetime.now(timezone.utc).isoformat(),  # Current UTC time in ISO 8601 format
            "isValid": 1  # Document validity status: 0 for invalid, 1 for valid
        }
    }

    # Execute the POST request and capture the response from MongoDB Atlas
    response_text = post_to_mongodb(insert_api_url, headers, insert_body)
    print("Response from MongoDB:", response_text)

if __name__ == '__main__':
    main()
