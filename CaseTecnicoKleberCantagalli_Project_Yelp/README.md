# Yelp Medallion Pipeline - GCP - DEV: KLEEBR CANTAGALLI

Este projeto implementa um pipeline de dados usando arquitetura Medallion na Google Cloud Platform (GCP), utilizando dados da API Yelp Fusion, 
A Yelp Fusion API oferece dados ricos e em tempo real sobre restaurantes, incluindo nome, localização, avaliações, tipo de cozinha, 
horário de funcionamento....

## Componentes
- **GCS**: Armazena dados brutos (bronze) e transformados (silver)
- **Cloud Functions**: Realizam transformação e agregação dos dados
- **BigQuery**: Armazena insights finais (gold)
- **Orquestrador Python**: Dispara etapas do pipeline

## Etapas
1. `ingest_yelp.py` coleta dados da API e salva no GCS (bronze)
2. Cloud Function Silver transforma dados em CSV (silver)
3. Cloud Function Gold agrega os dados e envia para BigQuery (gold)

## Execução
```bash
python3 orchestrator/orchestrate_pipeline.py
```

Substitua `YOUR_YELP_API_KEY` e configure os endpoints corretamente.

## Deploy das Cloud Functions

### 1. Deploy da Silver (Transformação)
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

### 2. Deploy da Gold (Agregação)
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

## Permissões e Configurações Adicionais

1. **Ativar APIs necessárias:**
```bash
gcloud services enable storage.googleapis.com cloudfunctions.googleapis.com bigquery.googleapis.com
```

2. **Conceder permissões às Cloud Functions:**
```bash
gcloud projects add-iam-policy-binding [PROJECT_ID] \
  --member="serviceAccount:[PROJECT_ID]@appspot.gserviceaccount.com" \
  --role="roles/storage.objectAdmin"

gcloud projects add-iam-policy-binding [PROJECT_ID] \
  --member="serviceAccount:[PROJECT_ID]@appspot.gserviceaccount.com" \
  --role="roles/bigquery.dataEditor"
```
