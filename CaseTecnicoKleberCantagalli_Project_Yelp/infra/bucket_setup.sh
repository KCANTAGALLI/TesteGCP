#!/bin/bash
BUCKET_NAME="medallion-pipeline-yelp"
gsutil mb -l us-central1 gs://$BUCKET_NAME
bq mk --dataset yelp_data
