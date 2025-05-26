# Windows 11 Setup Guide

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
git clone https://github.com/link1183/lab-165.git
cd lab-165

# Option 2: Download and extract ZIP file
# Extract to your preferred location
```

### Step 2: Create Python Virtual Environment

```cmd
# Create virtual environment
python -m venv venv

# Activate virtual environment
venv\Scripts\activate

# Upgrade pip
pip install --upgrade pip

# Install dependencies
pip install -r requirements.txt
```

### Step 3: Create Project Directories

```cmd
# Create necessary directories
mkdir data exports backup
```

### Step 4: Start MongoDB Service

```cmd
# Start MongoDB service
net start MongoDB

# Verify MongoDB is running
mongosh --eval "db.adminCommand('ping')"
```

### Step 5: Import Data to MongoDB

```cmd
# Import the JSON data
mongoimport --db my_data --collection open_data --type json --file data\path_of_exile_ladder.json
```

### Step 6: Create MongoDB Users

Connect to MongoDB shell and create the required users:

```cmd
mongosh
```

Run these commands in the MongoDB shell:

```javascript
use admin

// Create admin user
db.createUser({
  user: "myUserAdmin",
  pwd: "SecurePassword123!",
  roles: [
    { role: "userAdminAnyDatabase", db: "admin" },
    { role: "readWriteAnyDatabase", db: "admin" }
  ]
})

// Create read/write user for my_data database
db.createUser({
  user: "userModify",
  pwd: "UserPassword456!",
  roles: [
    { role: "readWrite", db: "my_data" }
  ]
})

// Create backup user
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

### Step 7: Create Team Collection

Still in the MongoDB shell:

```javascript
use my_data

// Create my_team collection with team member data
db.my_team.insertMany([
  {
    name: "Adrien Gunther",
    role: "Database Administrator",
    email: "adrien.gunther@eduvaud.ch",
    specialization: "MongoDB Management",
    created_at: new Date()
  },
  {
    name: "Claire Prodolliet",
    role: "Application Developer",
    email: "claire.prodolliet@eduvaud.ch",
    specialization: "Flask Applications",
    created_at: new Date()
  },
  {
    name: "Thomas Burkhalter",
    role: "Data Analyst",
    email: "thomas.burkhalter@eduvaud.ch",
    specialization: "Data Visualization",
    created_at: new Date()
  }
])
```

### Step 8: Make Required Data Modifications

Modify 3 existing documents:

```javascript
// Modify first document
db.open_data.updateOne(
  { name: "Tzn_NecroIsFineNow" },
  { $set: { custom_field: "Modified Player 1", modified_at: new Date() } },
);

// Modify second document
db.open_data.updateOne(
  { name: "RaizNeverFirstQT" },
  { $set: { custom_field: "Modified Player 2", modified_at: new Date() } },
);

// Modify third document
db.open_data.updateOne(
  { name: "GucciStreamerAdvantage" },
  { $set: { custom_field: "Modified Player 3", modified_at: new Date() } },
);
```

Add 3 new documents:

```javascript
// Add 3 new custom players
db.open_data.insertMany([
  {
    rank: 100,
    dead: false,
    online: true,
    name: "CustomPlayer1",
    level: 85,
    class: "Templar",
    id: "aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa",
    experience: 3500000000,
    account: "NewAccount1",
    challenges: 30,
    twitch: "customplayer1",
    ladder: "Custom League",
    custom_field: "Added Player 1",
    created_at: new Date(),
  },
  {
    rank: 101,
    dead: false,
    online: false,
    name: "CustomPlayer2",
    level: 78,
    class: "Marauder",
    id: "bbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbb",
    experience: 3200000000,
    account: "NewAccount2",
    challenges: 25,
    twitch: null,
    ladder: "Custom League HC",
    custom_field: "Added Player 2",
    created_at: new Date(),
  },
  {
    rank: 102,
    dead: true,
    online: false,
    name: "CustomPlayer3",
    level: 66,
    class: "Duelist",
    id: "cccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc",
    experience: 2800000000,
    account: "NewAccount3",
    challenges: 20,
    twitch: "customgamer3",
    ladder: "Custom SSF",
    custom_field: "Added Player 3",
    created_at: new Date(),
  },
]);

// Exit MongoDB shell
exit;
```

### Step 9: Export Collections

```cmd
# Export open_data collection
mongoexport --db my_data --collection open_data --out exports\open_data_export.json --pretty

# Export my_team collection
mongoexport --db my_data --collection my_team --out exports\my_team_export.json --pretty
```

### Step 10: Create Database Backup

```cmd
# Create backup using userPlus credentials
mongodump --username userPlus --password BackupPassword789! --authenticationDatabase admin --out backup\
```

### Step 11: Run the Flask Application

```cmd
# Activate virtual environment (if not already active)
venv\Scripts\activate

# Run without authentication
python app.py

# OR run with authentication (in separate terminal)
set MONGO_USERNAME=myUserAdmin
set MONGO_PASSWORD=SecurePassword123!
python app.py
```

### Step 12: Access the Application

- Open your browser
- Navigate to: [http://localhost:5000](http://localhost:5000)
- Check health: [http://localhost:5000/health](http://localhost:5000/health)
- View statistics: [http://localhost:5000/api/stats](http://localhost:5000/api/stats)

## Verification Commands

Run these in MongoDB shell to verify your setup:

```javascript
use my_data

// Check document counts
db.open_data.countDocuments()  // Should be 103 (100 original + 3 added)
db.my_team.countDocuments()    // Should be 3

// Verify modified documents
db.open_data.find({ custom_field: { $exists: true } }).count()  // Should be 6

// Verify added documents
db.open_data.find({ created_at: { $exists: true } }).count()    // Should be 3

// Check users (as admin)
use admin
db.getUsers()  // Should show 3 users
```
