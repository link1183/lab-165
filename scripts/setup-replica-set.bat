@echo off
echo ===============================================
echo MongoDB Replica Set Setup for Lab 165 (Windows)
echo ===============================================

REM Create keyfile for replica set
echo Creating keyfile...
python -c "import secrets; import base64; print(base64.b64encode(secrets.token_bytes(756)).decode())" > mongo-keyfile
echo Keyfile created: mongo-keyfile

REM Create directories
echo Creating directories...
if not exist data\rs0-1 mkdir data\rs0-1
if not exist data\rs0-2 mkdir data\rs0-2
if not exist data\rs0-3 mkdir data\rs0-3
if not exist logs mkdir logs

REM Start MongoDB instances
echo Starting MongoDB instances...

start /b mongod --replSet rs0 --port 27017 --dbpath data\rs0-1 --logpath logs\rs0-1.log --keyFile mongo-keyfile --bind_ip localhost
start /b mongod --replSet rs0 --port 27018 --dbpath data\rs0-2 --logpath logs\rs0-2.log --keyFile mongo-keyfile --bind_ip localhost
start /b mongod --replSet rs0 --port 27019 --dbpath data\rs0-3 --logpath logs\rs0-3.log --keyFile mongo-keyfile --bind_ip localhost

echo Waiting for instances to start...
timeout /t 15 /nobreak > nul

REM Initialize replica set
echo Initializing replica set...
mongosh --port 27017 --eval "rs.initiate({_id:'rs0',members:[{_id:0,host:'localhost:27017',priority:2},{_id:1,host:'localhost:27018',priority:1},{_id:2,host:'localhost:27019',priority:1}]})"

echo Waiting for primary election...
timeout /t 15 /nobreak > nul

REM Create admin user
echo Creating admin user...
mongosh --port 27017 --eval "use admin; db.createUser({user:'admin',pwd:'AdminPassword123!',roles:[{role:'root',db:'admin'}]})"

echo.
echo ===============================================
echo Replica Set Setup Complete!
echo ===============================================
echo To test:
echo 1. Run: python app_replica.py
echo 2. Visit: http://localhost:5000
echo 3. Check: http://localhost:5000/replica-status
echo ===============================================
pause
