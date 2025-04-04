# Guia de Deploy Real na GCP

## Pré-requisitos
- Projeto criado no Google Cloud
- SDK do Google Cloud instalado e autenticado
- Billing habilitado
- APIs ativadas:
```bash
gcloud services enable storage.googleapis.com cloudfunctions.googleapis.com bigquery.googleapis.com
```

## 1. Criação dos recursos
```bash
# Criar bucket
gsutil mb -l us-central1 gs://medallion-pipeline-yelp

# Criar dataset no BigQuery
bq mk --dataset yelp_data
```

## 2. Deploy da Cloud Function Silver
```bash
gcloud functions deploy silver_transform \
  --runtime python310 \
  --trigger-resource medallion-pipeline-yelp \
  --trigger-event google.storage.object.finalize \
  --entry-point transform_yelp_data \
  --source silver_transform \
  --region us-central1 \
  --allow-unauthenticated
```

## 3. Deploy da Cloud Function Gold
```bash
gcloud functions deploy gold_aggregate \
  --runtime python310 \
  --trigger-resource medallion-pipeline-yelp \
  --trigger-event google.storage.object.finalize \
  --entry-point aggregate_yelp_data \
  --source gold_aggregate \
  --region us-central1 \
  --allow-unauthenticated
```

## 4. Permissões
```bash
gcloud projects add-iam-policy-binding [PROJECT_ID] \
  --member="serviceAccount:[PROJECT_ID]@appspot.gserviceaccount.com" \
  --role="roles/storage.objectAdmin"

gcloud projects add-iam-policy-binding [PROJECT_ID] \
  --member="serviceAccount:[PROJECT_ID]@appspot.gserviceaccount.com" \
  --role="roles/bigquery.dataEditor"
```
