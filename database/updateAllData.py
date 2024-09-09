import requests
from datetime import datetime, timedelta, timezone

def update_documents(api_url, headers):
    """
    Updates documents to set 'isValid' to 0 where it is not already 1.
    or where the 'timestamp' is more than one day old.

    Parameters:
        api_url (str): URL for the MongoDB API endpoint.
        headers (dict): Request headers including API key and content type.
    """
    update_url = api_url + "/updateMany"  # An Data API endpoint

    # Calculate the cutoff datetime for one day ago
    one_day_ago = datetime.now(timezone.utc) - timedelta(days=1)
    one_day_ago_iso = one_day_ago.isoformat()

    # Update body for setting 'isValid' to 0 where it is not 1
    update_body = {
        "collection": "availableParking",
        "database": "demoDB",
        "dataSource": "Cluster0",
        "filter": {
            "$or": [
                {"isValid": {"$ne": 1}},
                {"timestamp": {"$lt": one_day_ago_iso}}
            ]
        },  # Matches documents where 'isValid' is not 1 or timestamp is older than one day
        "update": {"$set": {"isValid": 0}}  # Sets 'isValid' to 0
    }
    
    response = requests.post(update_url, json=update_body, headers=headers)
    print("Update Response:", response.text)

def delete_documents(api_url, headers):
    """
    Deletes documents where 'isValid' is set to 0.
    
    Parameters:
        api_url (str): URL for the MongoDB API endpoint.
        headers (dict): Request headers including API key and content type.
    """
    delete_url = api_url + "/deleteMany"  # An Data API endpoint

    # Delete body for removing documents with 'isValid' set to 0
    delete_body = {
        "collection": "availableParking",
        "database": "demoDB",
        "dataSource": "Cluster0",
        "filter": {"isValid": 0}  # Matches documents where 'isValid' is 0
    }
    
    response = requests.post(delete_url, json=delete_body, headers=headers)
    print("Delete Response:", response.text)

def main():
    api_url = "https://ap-southeast-1.aws.data.mongodb-api.com/app/data-eplbb/endpoint/data/v1/action"
    headers = {
        "api-key": "codqN8SQIUEuA4Q4ADCWmc3xnb7E4vr8otm2urWstPbl1LpONuputENzp7s5F9wv",  # Your MongoDB Atlas API key needs to be inserted here
        "Content-Type": "application/json"
    }

    # Update documents to invalidate them first
    update_documents(api_url, headers)

    # Then delete those invalidated documents
    delete_documents(api_url, headers)

if __name__ == '__main__':
    main()
