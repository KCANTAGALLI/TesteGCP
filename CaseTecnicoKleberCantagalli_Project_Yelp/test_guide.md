# Guia de Testes das Cloud Functions

## Testando a Ingestão (Bronze)
1. Edite `ingest_yelp.py` e insira sua API Key do Yelp.
2. Execute localmente:
```bash
python3 bronze_ingest/ingest_yelp.py
```
3. Verifique no GCS:
```bash
gsutil ls gs://medallion-pipeline-yelp/bronze/
```

## Testando a Transformação (Silver)
1. Após o upload do JSON no bucket, a função será acionada automaticamente.
2. Verifique o output:
```bash
gsutil ls gs://medallion-pipeline-yelp/silver/
```

## Testando a Agregação (Gold)
1. Certifique-se de ter uma tabela `silver_table` no BigQuery com os dados tabulares da camada Silver.
2. Dispare manualmente via console ou use:
```bash
gcloud functions call gold_aggregate
```
3. Verifique os dados:
```bash
bq query --use_legacy_sql=false 'SELECT * FROM yelp_data.gold_insights LIMIT 10'
```
