# MongoDB User Passwords for Lab 165

## User Credentials

### myUserAdmin
- **Username**: myUserAdmin
- **Password**: SecurePassword123!
- **Roles**: userAdminAnyDatabase, readWriteAnyDatabase
- **Database**: admin
- **Purpose**: Full administrative access

### userModify
- **Username**: userModify
- **Password**: UserPassword456!
- **Roles**: readWrite
- **Database**: my_data
- **Purpose**: Read/write access to my_data database only

### userPlus
- **Username**: userPlus
- **Password**: BackupPassword789!
- **Roles**: backup, restore, readWriteAnyDatabase
- **Database**: admin
- **Purpose**: Backup and restore operations

## Important Security Notes
- These passwords are for educational purposes only
- Change all passwords in production environments
- Store passwords securely (e.g., using environment variables)
- Never commit passwords to version control
- Use stronger passwords in real applications
