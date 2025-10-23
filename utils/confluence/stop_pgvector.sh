#!/bin/bash

# Stop and remove pgvector container
echo "Stopping pgvector..."

docker stop mindsdb-pgvector
docker rm mindsdb-pgvector

echo "✓ pgvector stopped and removed"

