# Windows 11 Setup Guide for MongoDB Lab 165

## Prerequisites

### 1. Install Python 3.12+

- Download from [python.org](https://www.python.org/downloads/)
- During installation, check "Add Python to PATH"
- Verify installation: `python --version`

### 2. Install MongoDB Community Edition

- Download from [MongoDB Download Center](https://www.mongodb.com/try/download/community)
- Follow installation wizard
- Install as Windows Service
- Verify installation: `mongod --version`

### 3. Install Git (Optional)

- Download from [git-scm.com](https://git-scm.com/download/win)
- Useful for cloning the repository

## Installation Steps

### Step 1: Download Project Files

```cmd
# Option 1: Clone with Git
git clone <repository-url>
cd lab-165

# Option 2: Download and extract ZIP file
# Extract to C:\lab-165 or your preferred location
```

### Step 2: Automatic Setup

```cmd
# Run the setup script
setup-windows.bat
```

### Step 3: Manual Setup (if automatic fails)

```cmd
# Create virtual environment
python -m venv venv

# Activate virtual environment
venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Create directories
mkdir data exports backup
```

### Step 4: Start MongoDB

```cmd
# Start MongoDB service
net start MongoDB

# Verify MongoDB is running
mongosh --eval "db.adminCommand('ping')"
```

### Step 5: Import Data

```cmd
# Import the CSV data
mongoimport --db my_data --collection open_data --type csv --headerline --file data\path_of_exile_ladder.csv

# Create required modifications (run these in mongosh)
```

### Step 6: Set Up Users

Connect to mongosh and run:

```javascript
use admin

// Create users
db.createUser({
  user: "myUserAdmin",
  pwd: "SecurePassword123!",
  roles: [
    { role: "userAdminAnyDatabase", db: "admin" },
    { role: "readWriteAnyDatabase", db: "admin" }
  ]
})

db.createUser({
  user: "userModify",
  pwd: "UserPassword456!",
  roles: [
    { role: "readWrite", db: "my_data" }
  ]
})

db.createUser({
  user: "userPlus",
  pwd: "BackupPassword789!",
  roles: [
    { role: "backup", db: "admin" },
    { role: "restore", db: "admin" },
    { role: "readWriteAnyDatabase", db: "admin" }
  ]
})
```

### Step 7: Make Required Modifications

```javascript
use my_data

// Modify 3 documents
db.open_data.updateOne(
  { "name": "Tzn_NecroIsFineNow" },
  { $set: { "custom_field": "Modified Player 1", "modified_at": new Date() } }
)

db.open_data.updateOne(
  { "name": "RaizNeverFirstQT" },
  { $set: { "custom_field": "Modified Player 2", "modified_at": new Date() } }
)

db.open_data.updateOne(
  { "name": "GucciStreamerAdvantage" },
  { $set: { "custom_field": "Modified Player 3", "modified_at": new Date() } }
)

// Add 3 new documents
db.open_data.insertMany([
  {
    "rank": 100,
    "dead": false,
    "online": true,
    "name": "CustomPlayer1",
    "level": 85,
    "class": "Templar",
    "id": "aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa",
    "experience": 3500000000,
    "account": "NewAccount1",
    "challenges": 30,
    "twitch": "customplayer1",
    "ladder": "Custom League",
    "custom_field": "Added Player 1",
    "created_at": new Date()
  },
  {
    "rank": 101,
    "dead": false,
    "online": false,
    "name": "CustomPlayer2",
    "level": 78,
    "class": "Marauder",
    "id": "bbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbb",
    "experience": 3200000000,
    "account": "NewAccount2",
    "challenges": 25,
    "twitch": null,
    "ladder": "Custom League HC",
    "custom_field": "Added Player 2",
    "created_at": new Date()
  },
  {
    "rank": 102,
    "dead": true,
    "online": false,
    "name": "CustomPlayer3",
    "level": 66,
    "class": "Duelist",
    "id": "cccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc",
    "experience": 2800000000,
    "account": "NewAccount3",
    "challenges": 20,
    "twitch": "customgamer3",
    "ladder": "Custom SSF",
    "custom_field": "Added Player 3",
    "created_at": new Date()
  }
])
```

### Step 8: Export Collections

```cmd
# Export collections
mongoexport --db my_data --collection open_data --out exports\open_data_export.json --pretty
mongoexport --db my_data --collection my_team --out exports\my_team_export.json --pretty
```

### Step 9: Create Backup

```cmd
# Create backup
mongodump --username userPlus --password BackupPassword789! --authenticationDatabase admin --out backup\
```

### Step 10: Run the Application

```cmd
# Without authentication
python app.py

# With authentication
set MONGO_USERNAME=myUserAdmin
set MONGO_PASSWORD=SecurePassword123!
python app.py
```

### Step 11: Access the Application

- Open your browser
- Navigate to: [http://localhost:5000](http://localhost:5000)
- Check health: [http://localhost:5000/health](http://localhost:5000/health)

## Troubleshooting

### Common Issues

**1. Python not found**

- Ensure Python is installed and added to PATH
- Try using `py` instead of `python`

**2. MongoDB service won't start**

```cmd
# Check Windows Services
services.msc
# Look for "MongoDB Server" and start it manually
```

**3. Virtual environment activation fails**

```cmd
# Try different activation method
venv\Scripts\activate.bat
# Or use PowerShell
venv\Scripts\Activate.ps1
```

**4. mongoimport command not found**

- MongoDB bin directory should be in PATH
- Try full path: `"C:\Program Files\MongoDB\Server\5.0\bin\mongoimport"`

**5. Permission errors**

- Run Command Prompt as Administrator
- Check MongoDB data directory permissions
