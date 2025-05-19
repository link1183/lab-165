#!/bin/bash

echo "==============================================="
echo "MongoDB Replica Set Setup for Lab 165"
echo "==============================================="

# Create keyfile for replica set authentication
echo "Creating keyfile for replica set..."
openssl rand -base64 756 >mongo-keyfile
chmod 400 mongo-keyfile
echo "Keyfile created: mongo-keyfile"

# Create data directories for each replica set member
echo "Creating data directories..."
mkdir -p data/rs0-1 data/rs0-2 data/rs0-3
mkdir -p logs

# Start three MongoDB instances
echo "Starting MongoDB instances..."

# Primary (port 27017)
mongod --replSet rs0 \
  --port 27017 \
  --dbpath data/rs0-1 \
  --logpath logs/rs0-1.log \
  --keyFile mongo-keyfile \
  --bind_ip localhost \
  --fork

# Secondary 1 (port 27018)
mongod --replSet rs0 \
  --port 27018 \
  --dbpath data/rs0-2 \
  --logpath logs/rs0-2.log \
  --keyFile mongo-keyfile \
  --bind_ip localhost \
  --fork

# Secondary 2 (port 27019)
mongod --replSet rs0 \
  --port 27019 \
  --dbpath data/rs0-3 \
  --logpath logs/rs0-3.log \
  --keyFile mongo-keyfile \
  --bind_ip localhost \
  --fork

echo "Waiting for MongoDB instances to start..."
sleep 10

# Initialize replica set
echo "Initializing replica set..."
mongosh --port 27017 --eval '
rs.initiate({
  _id: "rs0",
  members: [
    { _id: 0, host: "localhost:27017", priority: 2 },
    { _id: 1, host: "localhost:27018", priority: 1 },
    { _id: 2, host: "localhost:27019", priority: 1 }
  ]
})
'

echo "Waiting for primary election..."
sleep 15

# Create admin user on primary
echo "Creating admin user..."
mongosh --port 27017 --eval '
use admin
db.createUser({
  user: "admin",
  pwd: "AdminPassword123!",
  roles: [
    { role: "root", db: "admin" }
  ]
})
'

# Wait for replication
echo "Waiting for replication to sync..."
sleep 10

# Check replica set status
echo "Checking replica set status..."
mongosh --port 27017 --username admin --password AdminPassword123! --authenticationDatabase admin --eval '
rs.status()
'

echo "==============================================="
echo "Replica Set Setup Complete!"
echo "==============================================="
echo "Connection string: mongodb://admin:AdminPassword123!@localhost:27017,localhost:27018,localhost:27019/my_data?replicaSet=rs0"
echo "Run the replica set application with: python app_replica.py"
echo "==============================================="
