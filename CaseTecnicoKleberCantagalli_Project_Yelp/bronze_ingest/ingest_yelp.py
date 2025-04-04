import requests
import json
import logging
from google.cloud import storage

logging.basicConfig(level=logging.INFO)

def fetch_yelp_data(api_key, location="Sao Paulo", category="restaurants", limit=50):
    try:
        url = "https://api.yelp.com/v3/businesses/search"
        headers = {"Authorization": f"Bearer {api_key}"}
        params = {"location": location, "categories": category, "limit": limit}
        response = requests.get(url, headers=headers, params=params)
        response.raise_for_status()
        logging.info("Dados do Yelp obtidos com sucesso.")
        return response.json()
    except Exception as e:
        logging.error(f"Erro ao buscar dados do Yelp: {e}")
        raise

def save_to_gcs(bucket_name, destination_blob_name, data):
    try:
        client = storage.Client()
        bucket = client.get_bucket(bucket_name)
        blob = bucket.blob(destination_blob_name)
        blob.upload_from_string(json.dumps(data), content_type="application/json")
        logging.info(f"Dados salvos no GCS: gs://{bucket_name}/{destination_blob_name}")
    except Exception as e:
        logging.error(f"Erro ao salvar no GCS: {e}")
        raise

def main():
    YELP_API_KEY = "YOUR_YELP_API_KEY"
    BUCKET_NAME = "medallion-pipeline-yelp"
    FILE_NAME = "bronze/yelp_restaurants.json"

    data = fetch_yelp_data(YELP_API_KEY)
    if "businesses" in data and data["businesses"]:
        save_to_gcs(BUCKET_NAME, FILE_NAME, data)
    else:
        logging.warning("Nenhum dado de restaurante retornado pela API do Yelp.")
