import requests

def find_nearby_locations(api_url, headers, body):
    """
    Queries a MongoDB Atlas collection for locations near a specified point.
    
    Parameters:
        api_url (str): The endpoint URL for the MongoDB Atlas REST API to perform location queries.
        headers (dict): Headers for the API request, including authorization and content type.
        body (dict): The request body with details about the collection, database, data source, and filter conditions for geospatial querying.
        
    Returns:
        str: The response text from the API, containing the locations found or an error message.
    """
    response = requests.post(api_url, json=body, headers=headers)
    return response.text

def main():
    # Define the endpoint URL for geospatial queries within the MongoDB Atlas API
    search_url = "https://ap-southeast-1.aws.data.mongodb-api.com/app/data-eplbb/endpoint/data/v1/action/find"

    # Headers for the API request including the required API key and content type specification
    headers = {
        "api-key": "codqN8SQIUEuA4Q4ADCWmc3xnb7E4vr8otm2urWstPbl1LpONuputENzp7s5F9wv",  # Placeholder for the actual API key
        "Content-Type": "application/json"
    }

    # Request body specifying the collection and geospatial filter criteria for finding nearby parking locations
    search_body = {
        "collection": "availableParking",
        "database": "demoDB",
        "dataSource": "Cluster0",
        "filter": {
            "location": {
                "$near": {
                    "$geometry": {"type": "Point", "coordinates": [-123.247120, 49.26013]},
                    "$minDistance": 0,
                    "$maxDistance": 3000  # Maximum search radius in meters
                }
            }
        }
    }

    # Execute the search query and capture the response
    response_text = find_nearby_locations(search_url, headers, search_body)
    if response_text.strip() == '{"documents":[]}':  # Check for empty
        print("No nearby parking locations found.")
    else:
        print("Nearby Parking Locations:", response_text)

if __name__ == '__main__':
    main()
