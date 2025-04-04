# Passo a Passo: Deploy Real do Pipeline Yelp na GCP

## Pré-requisitos
- Projeto GCP criado com billing ativado
- Google Cloud SDK instalado
- Autenticação feita com `gcloud auth login`
- Projeto selecionado com `gcloud config set project [SEU_PROJECT_ID]`

---

##  1. Ativar APIs
```bash
gcloud services enable storage.googleapis.com \
  cloudfunctions.googleapis.com \
  bigquery.googleapis.com
```

---

##  2. Criar Bucket e Dataset
```bash
BUCKET_NAME=medallion-pipeline-yelp
gsutil mb -l us-central1 gs://$BUCKET_NAME

bq mk --dataset --location=US yelp_data
```

---

##  3. Conceder Permissões
```bash
PROJECT_ID=$(gcloud config get-value project)

gcloud projects add-iam-policy-binding $PROJECT_ID \
  --member="serviceAccount:$PROJECT_ID@appspot.gserviceaccount.com" \
  --role="roles/storage.objectAdmin"

gcloud projects add-iam-policy-binding $PROJECT_ID \
  --member="serviceAccount:$PROJECT_ID@appspot.gserviceaccount.com" \
  --role="roles/bigquery.dataEditor"
```

---

##  4. Deploy das Cloud Functions

### Silver - Transformação
```bash
gcloud functions deploy silver_transform \
  --runtime python310 \
  --trigger-resource $BUCKET_NAME \
  --trigger-event google.storage.object.finalize \
  --entry-point transform_yelp_data \
  --source silver_transform \
  --region us-central1 \
  --allow-unauthenticated
```

### Gold - Agregação
```bash
gcloud functions deploy gold_aggregate \
  --runtime python310 \
  --trigger-resource $BUCKET_NAME \
  --trigger-event google.storage.object.finalize \
  --entry-point aggregate_yelp_data \
  --source gold_aggregate \
  --region us-central1 \
  --allow-unauthenticated
```

---

##  5. Rodar Ingestão (Bronze)
- Edite `bronze_ingest/ingest_yelp.py` com sua API Key do Yelp.
- Execute localmente:
```bash
python3 bronze_ingest/ingest_yelp.py
```

---

##  6. Verificar Resultado
```bash
gsutil ls gs://$BUCKET_NAME/bronze/
gsutil ls gs://$BUCKET_NAME/silver/
bq query --use_legacy_sql=false 'SELECT * FROM yelp_data.gold_insights LIMIT 10'
```

