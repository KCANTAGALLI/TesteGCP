import requests
import json
from google.cloud import storage

def fetch_yelp_data(api_key, location="Sao Paulo", category="restaurants", limit=50):
    url = "https://api.yelp.com/v3/businesses/search"
    headers = {"Authorization": f"Bearer {api_key}"}
    params = {"location": location, "categories": category, "limit": limit}
    response = requests.get(url, headers=headers, params=params)
    return response.json()

def save_to_gcs(bucket_name, destination_blob_name, data):
    client = storage.Client()
    bucket = client.get_bucket(bucket_name)
    blob = bucket.blob(destination_blob_name)
    blob.upload_from_string(json.dumps(data), content_type="application/json")

def main():
    YELP_API_KEY = "YOUR_YELP_API_KEY"
    BUCKET_NAME = "medallion-pipeline-yelp"
    FILE_NAME = "bronze/yelp_restaurants.json"

    data = fetch_yelp_data(YELP_API_KEY)
    save_to_gcs(BUCKET_NAME, FILE_NAME, data)
