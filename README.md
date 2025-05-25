# MongoDB Lab 165 - Practical Evaluation

## Project Overview

This project is a flask app that shows a random document of the MMO RPG "Path of Exile". We only took the first 100 lines of the original files.

## Practical informations

**Module**: [i165 - Utiliser des bases de données NoSQL](https://moodle.epsic.ch/course/view.php?id=1627)

**Team members:**

- Adrien Gunther
- Claire Prodolliet
- Thomas Burkhalter

## 🚀 Quick Start

### Using Docker (Recommended)

Download the ZIP or take it directly from [Github repository](https://github.com/link1183/lab-165).
You can run the app in standalone mode or enable replicas set.

```bash
cd lab-165

# Run standalone application
docker compose up --build

# Access: http://localhost:5000

# Run with replica set (bonus)
docker-compose --profile replica up --build
# Replica access: http://localhost:5001
# Normal access: http://localhost:5000
```

## Features checklist

1. **MongoDB Standalone Server [30%]**

- [x] Imported Path of Exile ladder data (13 original + 3 added = 16 documents)
- [x] Modified 3 existing documents with custom fields
- [x] Added 3 new documents with complete structure
- [x] Created my_team collection (3 members)
- [x] Exported collections to JSON format

2. **Mongosh Commands [10%]**

- [x] Database listing commands (`show dbs`)
- [x] Collection operations (`show collections`)
- [x] Document counting for both collections
- [x] All commands documented with expected results

3. **User Authentication [30%]**

- [x] **myUserAdmin**: Full administrative privileges
- [x] **userModify**: Limited read/write to my_data only
- [x] **userPlus**: Backup and restore operations
- [x] Complete server backup with authenticated users

4. **Flask Application [30%]**

- [x] Random document display
- [x] Health check endpoint (`/health`)
- [x] Statistics API endpoint (`/api/stats`)
- [x] Docker deployment support

### Bonus Features

5. **Replica Set Implementation [+20%]**

- [x] 3-server replica set configuration
- [x] Modified application for replica set (`app-replica.py`)
- [x] Docker Compose with profiles

## User Credentials

| User        | Role   | Access Level              | Password           |
| ----------- | ------ | ------------------------- | ------------------ |
| myUserAdmin | Admin  | Full database access      | <À changer>        |
| userModify  | User   | my_data read/write only   | UserPassword456!   |
| userPlus    | Backup | Backup/restore operations | BackupPassword789! |

_See `docs/user_passwords.md` for secure credential storage_

## Application Endpoints

### Main Application (port 5000)

- `/` - Random player display with statistics
- `/health` - Application health and database stats
- `/api/stats` - Player and class distribution

### Replica Set Application (port 5001 - Bonus)

- `/` - Random player with replica set information
- `/replica-status` - Detailed replica set status
- `/health` - Health check with replica set details

## Data Description

**Source**: Path of Exile Ladder Data  
**Content**: Player rankings, levels, classes, experience, challenges, Twitch channels, and game modes  
**Size**: 100 documents  
**Collections**:

- `open_data`: Player ladder information
- `my_team`: Team member information (3 documents)

## 🚀 Deployment Options

### 1. Docker Deployment (Recommended)

```bash
# Standard deployment
docker-compose up --build

# With replica set
docker-compose --profile replica up --build

# With MongoDB Express (database UI)
docker-compose --profile tools up --build
```

### 2. Windows 11 Local Setup

1. Run `setup-windows.bat`
2. Follow prompts for automatic installation
3. Manual steps in `docs/windows-setup.md`

### 3. Manual Configuration

1. Install MongoDB and Python
2. Create users with authentication
3. Import data and make modifications
4. Export collections and create backup
5. Run Flask application

## 📝 Key Implementation Steps

### 1. Data Import and Modification

```bash
# Import CSV data
mongoimport --db my_data --collection open_data --type csv --headerline --file data/path_of_exile_ladder.csv

# Modify 3 documents (add custom fields)
# Add 3 new documents
# Create my_team collection
```

### 2. User Authentication

```javascript
// Create three users with different privileges
db.createUser({user: "myUserAdmin", pwd: "SecurePassword123!", roles: [...]})
db.createUser({user: "userModify", pwd: "UserPassword456!", roles: [...]})
db.createUser({user: "userPlus", pwd: "BackupPassword789!", roles: [...]})
```

### 3. Application Development

- Flask application with MongoDB integration
- Bootstrap UI with Path of Exile styling
- Health monitoring and statistics
- Docker containerization

### 4. Backup and Export

```bash
# Export collections
mongoexport --db my_data --collection open_data --out exports/open_data_export.json
mongoexport --db my_data --collection my_team --out exports/my_team_export.json

# Create backup
mongodump --username userPlus --password BackupPassword789! --out backup/
```

## 📚 Documentation

All documentation is located in the `/docs` directory:

- `mongosh_commands.md` - Complete command reference with results
- `user_passwords.md` - Secure credential documentation
- `windows-setup.md` - Detailed Windows installation guide
