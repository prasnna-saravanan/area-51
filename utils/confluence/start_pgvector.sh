#!/bin/bash

# Start pgvector container for MindsDB KB storage
echo "Starting pgvector..."

docker run -d \
  --name mindsdb \
  -e POSTGRES_PASSWORD=mindsdb \
  -e POSTGRES_USER=mindsdb \
  -e POSTGRES_DB=mindsdb \
  -p 5432:5432 \
  pgvector/pgvector:pg16

echo "Waiting for pgvector to be ready..."
sleep 5

echo "✓ pgvector is running on port 5432"
echo "Connection details:"
echo "  Host: localhost (or host.docker.internal if MindsDB is in Docker)"
echo "  Port: 5432"
echo "  Database: postgres"
echo "  User: postgres"
echo "  Password: admin"

