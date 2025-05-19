# MongoDB Commands - Lab 165

## 1. Show all databases

**Command:**

```javascript
show dbs
```

**Expected Result:**

```
admin   0.000GB
config  0.000GB
local   0.000GB
my_data 0.002GB
```

## 2. Show collections in my_data database

**Command:**

```javascript
use my_data
show collections
```

**Expected Result:**

```
my_team
open_data
```

## 3. Count documents in open_data collection

**Command:**

```javascript
use my_data
db.open_data.countDocuments()
```

**Expected Result:**

```
16
```

## 4. Count documents in my_team collection

**Command:**

```javascript
use my_data
db.my_team.countDocuments()
```

**Expected Result:**

```
3
```

## 5. Additional verification commands

### Verify modified documents

```javascript
db.open_data.find({ custom_field: { $exists: true } }).count();
// Expected result: 3
```

### Verify added documents

```javascript
db.open_data.find({ created_at: { $exists: true } }).count();
// Expected result: 3
```

### Sample document structure

```javascript
db.open_data.findOne();
// Shows the structure of a document
```

### Check users (run as admin)

```javascript
use admin
db.getUsers()
// Should show myUserAdmin, userModify, userPlus
```
