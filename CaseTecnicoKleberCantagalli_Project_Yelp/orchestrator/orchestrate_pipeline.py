import requests

def main():
    silver_url = "https://REGION-PROJECT.cloudfunctions.net/silver_transform"
    gold_url = "https://REGION-PROJECT.cloudfunctions.net/gold_aggregate"

    from bronze_ingest import main as bronze_main
    bronze_main()

    requests.post(silver_url)
    requests.post(gold_url)
