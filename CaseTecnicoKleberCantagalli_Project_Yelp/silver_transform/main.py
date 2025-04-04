import pandas as pd
import json
import logging
from google.cloud import storage

logging.basicConfig(level=logging.INFO)

def transform_yelp_data(event, context):
    try:
        storage_client = storage.Client()
        bucket = storage_client.get_bucket("medallion-pipeline-yelp")
        blob = bucket.blob("bronze/yelp_restaurants.json")
        data = json.loads(blob.download_as_string())
        logging.info("Dados brutos carregados do GCS.")

        records = []
        for biz in data.get("businesses", []):
            if not biz.get("id") or not biz.get("name"):
                continue
            records.append({
                "id": biz.get("id"),
                "name": biz.get("name"),
                "rating": biz.get("rating"),
                "review_count": biz.get("review_count"),
                "city": biz.get("location", {}).get("city"),
                "categories": ", ".join([c["title"] for c in biz.get("categories", [])]),
            })

        df = pd.DataFrame(records)
        df.to_csv("/tmp/yelp_silver.csv", index=False)
        blob_silver = bucket.blob("silver/yelp_silver.csv")
        blob_silver.upload_from_filename("/tmp/yelp_silver.csv")
        logging.info("Dados transformados salvos na camada Silver no GCS.")

    except Exception as e:
        logging.error(f"Erro durante a transformação da camada Silver: {e}")
        raise
