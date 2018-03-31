export BUCKET_NAME=penguincount-197807-mlengine
export JOB_NAME="penguin_count_train_$(date +%Y%m%d_%H%M%S)"
export JOB_DIR=gs://$BUCKET_NAME/$JOB_NAME
export REGION=europe-west1

gcloud ml-engine jobs submit training $JOB_NAME \
  --job-dir gs://$BUCKET_NAME/$JOB_NAME \
  --runtime-version 1.0 \
  --module-name train.train \
  --package-path ./train \
  --region $REGION \
  --config=cloudml-gpu.yaml \
  -- \
  --data_dir gs://penguincount-197807-mlengine/data