# MongoDB Lab 165

## Project Overview

This project is a Flask application that displays random documents from a MongoDB collection containing Path of Exile ladder data.

## Practical Information

**Module**: [i165 - Utiliser des bases de données NoSQL](https://moodle.epsic.ch/course/view.php?id=1627)

**Team members:**

- Adrien Gunther
- Claire Prodolliet
- Thomas Burkhalter

## Quick Start

### Using Docker (Recommended)

Download the ZIP or clone from [Github repository](https://github.com/link1183/lab-165).

```bash
cd lab-165

# Run standalone application
docker compose up --build

# Access: http://localhost:5000

# Run with replica set (bonus feature)
docker compose --profile replica up --build
# Replica access: http://localhost:5001
# Normal access: http://localhost:5000
```

### Manual Windows Setup

For manual installation on Windows 11, see detailed instructions in `docs/windows-setup.md`.

Requirements:

- Python 3.12+
- MongoDB Community Edition
- Virtual environment setup
- Manual database configuration

## User Credentials

| User        | Role   | Access Level              | Password           |
| ----------- | ------ | ------------------------- | ------------------ |
| myUserAdmin | Admin  | Full database access      | SecurePassword123! |
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

**Source**: [Path of Exile Ladder Data](https://www.kaggle.com/datasets/gagazet/path-of-exile-league-statistic?resource=download)

**Content**: Player rankings, levels, classes, experience, challenges, Twitch channels, and game modes

**Size**: 100 original documents + 3 modifications + 3 additions = 103 total

**Collections**:

- `open_data`: Player ladder information (103 documents)
- `my_team`: Team member information (3 documents)

**Data Processing**:
The original CSV data was converted to JSON using:

```sh
npm install -g csvtojson
npx csvtojson data/path_of_exile_ladder.csv | jq '.' > data/path_of_exile_ladder.json
```

Note :
The original downloaded file contains about 10000 documents. We reduced this size to the 100 documents present in this project.

## Implementation Requirements

### 1. Data Import and Modification

**Import JSON data**: 100 Path of Exile ladder entries

**Modify 3 documents**: Added custom fields to existing players:

- `Tzn_NecroIsFineNow` → "Modified Player 1"
- `RaizNeverFirstQT` → "Modified Player 2"
- `GucciStreamerAdvantage` → "Modified Player 3"

**Add 3 new documents**: Custom players with different classes and leagues

### 2. User Authentication

**Three user types created**:

- **myUserAdmin**: Full administrative access
- **userModify**: Read/write access to my_data only
- **userPlus**: Backup and restore operations

### 3. Data Export and Backup

**Collections exported**: JSON exports in `/exports` directory

**Database backup**: Complete mongodump backup in `/backup` directory

**Verification commands**: Documented in `docs/mongosh_commands.md`

## Project Structure

```
lab-165/
├── app.py                     # Main Flask application
├── app-replica.py             # Replica set Flask application
├── Dockerfile                 # Docker container configuration
├── docker-compose.yml         # Docker services configuration
├── requirements.txt           # Python dependencies
├── data/
│   └── path_of_exile_ladder.json
├── docs/
│   ├── mongosh_commands.md    # MongoDB commands reference
│   ├── user_passwords.md      # User credentials documentation
│   └── windows-setup.md       # Manual Windows installation
├── exports/
│   ├── open_data_export.json  # Collection export
│   └── my_team_export.json    # Team collection export
├── backup/                    # MongoDB backup files
└── templates/
    └── index.html             # Web interface template
```

## MongoDB Commands Reference

Key verification commands (run in `mongosh`):

```javascript
// Check databases
show dbs

// Check collections
use my_data
show collections

// Count documents
db.open_data.countDocuments()  // Should be 103
db.my_team.countDocuments()    // Should be 3

// Verify modifications
db.open_data.find({ custom_field: { $exists: true } }).count()  // Should be 6
db.open_data.find({ created_at: { $exists: true } }).count()    // Should be 3
```

Complete command reference available in `docs/mongosh_commands.md`.

## Documentation

- **Setup Guide**: `docs/windows-setup.md`
- **Commands Reference**: `docs/mongosh_commands.md`
- **User Credentials**: `docs/user_passwords.md`
- **API Documentation**: Available at `/health` and `/api/stats` endpoints
