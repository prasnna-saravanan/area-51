#!/bin/bash

# Start pgvector container for MindsDB KB storage
echo "Starting pgvector..."

docker run -d \
  --name mindsdb-pgvector \
  -e POSTGRES_PASSWORD=admin \
  -e POSTGRES_USER=postgres \
  -e POSTGRES_DB=postgres \
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

