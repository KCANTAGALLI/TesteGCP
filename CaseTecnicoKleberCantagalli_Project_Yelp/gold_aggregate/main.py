from google.cloud import bigquery
import logging

logging.basicConfig(level=logging.INFO)

def aggregate_yelp_data(event, context):
    try:
        client = bigquery.Client()
        dataset_id = "yelp_data"
        table_id = "gold_insights"

        job_config = bigquery.QueryJobConfig(
            destination=f"{client.project}.{dataset_id}.{table_id}",
            write_disposition="WRITE_TRUNCATE"
        )

        sql = f"""
        SELECT
          city,
          categories,
          COUNT(*) AS total_restaurantes,
          AVG(rating) AS media_avaliacao,
          SUM(review_count) AS total_reviews
        FROM
          `{client.project}.{dataset_id}.silver_table`
        GROUP BY city, categories
        """

        query_job = client.query(sql, job_config=job_config)
        query_job.result()
        logging.info("Agregação da camada Gold concluída e salva no BigQuery.")

    except Exception as e:
        logging.error(f"Erro ao agregar dados na camada Gold: {e}")
        raise
