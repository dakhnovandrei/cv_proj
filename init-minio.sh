#!/bin/bash

set -e


minio server /data --console-address ":9001" &
MINIO_PID=$!

until curl -s http://127.0.0.1:9000/minio/health/live; do
  echo "Waiting for MinIO..."
  sleep 2
done


mc alias set local http://127.0.0.1:9000 $MINIO_ROOT_USER $MINIO_ROOT_PASSWORD

mc mb --ignore-existing local/plant-disease-image
mc anonymous set public --recursive local/plant-disease-image

wait $MINIO_PID