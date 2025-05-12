#!/bin/bash

# This script runs inside the MongoDB container to import CSV data

echo "Waiting for MongoDB to be ready..."
until mongosh --eval "db.adminCommand('ping')" >/dev/null 2>&1; do
  sleep 2
done

echo "MongoDB is ready. Importing data..."

# Import the CSV file
mongoimport --db my_data --collection open_data --type csv --headerline --file /docker-entrypoint-initdb.d/path_of_exile_ladder.csv

echo "Data import completed successfully!"
