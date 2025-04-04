import pandas as pd
import json
from google.cloud import storage

def transform_yelp_data(event, context):
    storage_client = storage.Client()
    bucket = storage_client.get_bucket("medallion-pipeline-yelp")
    blob = bucket.blob("bronze/yelp_restaurants.json")
    data = json.loads(blob.download_as_string())

    records = []
    for biz in data.get("businesses", []):
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
