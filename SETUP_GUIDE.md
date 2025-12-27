# GearGuard - Complete Setup Guide

## Quick Start (5 Minutes)

### 1. Install Python 3.8+
- Download from [python.org](https://www.python.org/downloads/)
- During installation, **check "Add Python to PATH"**

### 2. Install MySQL 8.0+
- Download from [mysql.com](https://dev.mysql.com/downloads/mysql/)
- Remember your root password

### 3. Setup Project
```bash
# Extract the project folder
cd gearguard

# Create virtual environment
python -m venv venv

# Activate it
# Windows:
venv\Scripts\activate
# Mac/Linux:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

### 4. Create Database
```sql
mysql -u root -p
CREATE DATABASE gearguard;
EXIT;
```

### 5. Configure (Edit config.py)
```python
MYSQL_USER = 'root'
MYSQL_PASSWORD = 'your_mysql_password'
```

### 6. Run Application
```bash
python app.py
```

### 7. Open Browser
```
http://localhost:5000
```

---

## Detailed Setup Instructions

### Step 1: Python Installation

#### Windows
1. Download Python 3.8+ from python.org
2. Run installer
3. **IMPORTANT:** Check "Add Python to PATH"
4. Click "Install Now"
5. Verify installation:
```bash
python --version
pip --version
```

#### macOS
```bash
# Install Homebrew first (if not installed)
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"

# Install Python
brew install python@3.9
```

#### Linux (Ubuntu/Debian)
```bash
sudo apt update
sudo apt install python3.9 python3-pip python3-venv
```

### Step 2: MySQL Installation

#### Windows
1. Download MySQL Installer from mysql.com
2. Choose "Developer Default"
3. Set root password (remember this!)
4. Complete installation
5. Verify:
```bash
mysql --version
```

#### macOS
```bash
brew install mysql
brew services start mysql
mysql_secure_installation
```

#### Linux (Ubuntu/Debian)
```bash
sudo apt update
sudo apt install mysql-server
sudo systemctl start mysql
sudo mysql_secure_installation
```

### Step 3: Project Setup

#### Create Project Directory
```bash
# Navigate to where you want the project
cd /path/to/your/workspace

# Extract the GearGuard files or clone from git
# You should have this structure:
gearguard/
├── app.py
├── config.py
├── models.py
├── requirements.txt
├── routes/
├── templates/
└── static/
```

#### Create Virtual Environment
```bash
cd gearguard

# Create virtual environment
python -m venv venv

# If above fails, try:
python3 -m venv venv
```

#### Activate Virtual Environment

**Windows Command Prompt:**
```bash
venv\Scripts\activate.bat
```

**Windows PowerShell:**
```bash
venv\Scripts\Activate.ps1
# If you get an error, run:
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

**macOS/Linux:**
```bash
source venv/bin/activate
```

You should see `(venv)` at the start of your command prompt.

#### Install Dependencies
```bash
pip install -r requirements.txt
```

Expected output:
```
Successfully installed Flask-2.3.2 Flask-SQLAlchemy-3.0.5 PyMySQL-1.1.0 cryptography-41.0.3
```

### Step 4: Database Configuration

#### Create Database
```bash
# Login to MySQL
mysql -u root -p
# Enter your MySQL root password
```

```sql
-- Create the database
CREATE DATABASE gearguard CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;

-- Verify it was created
SHOW DATABASES;

-- Exit MySQL
EXIT;
```

#### (Optional) Create Dedicated User
```sql
mysql -u root -p

CREATE USER 'gearguard_user'@'localhost' IDENTIFIED BY 'secure_password_here';
GRANT ALL PRIVILEGES ON gearguard.* TO 'gearguard_user'@'localhost';
FLUSH PRIVILEGES;
EXIT;
```

### Step 5: Configure Application

#### Edit config.py
Open `config.py` in a text editor and update:

```python
class Config:
    # Update these values
    MYSQL_USER = 'root'  # or 'gearguard_user'
    MYSQL_PASSWORD = 'your_actual_password'  # Your MySQL password
    MYSQL_HOST = 'localhost'
    MYSQL_PORT = '3306'
    MYSQL_DB = 'gearguard'
```

#### Or Use Environment Variables
Create a file named `.env` (optional):
```bash
MYSQL_USER=root
MYSQL_PASSWORD=your_password
MYSQL_HOST=localhost
MYSQL_PORT=3306
MYSQL_DB=gearguard
```

### Step 6: Initialize Application

#### Run the Application
```bash
python app.py
```

Expected output:
```
 * Serving Flask app 'app'
 * Debug mode: on
WARNING: This is a development server. Do not use it in a production deployment.
 * Running on http://0.0.0.0:5000
```

#### Verify Database Tables Were Created
In another terminal:
```bash
mysql -u root -p gearguard

SHOW TABLES;
```

You should see:
```
+-------------------------+
| Tables_in_gearguard     |
+-------------------------+
| equipment               |
| maintenance_request     |
| maintenance_team        |
| technician              |
+-------------------------+
```

### Step 7: Access Application

1. Open your web browser
2. Navigate to: `http://localhost:5000`
3. You should see the GearGuard home page

---

## Common Issues & Solutions

### Issue 1: "pip is not recognized"
**Solution:**
```bash
python -m pip install -r requirements.txt
```

### Issue 2: "Access Denied for user 'root'@'localhost'"
**Solution:** Check your MySQL password in config.py

### Issue 3: "No module named 'flask'"
**Solution:** Make sure virtual environment is activated
```bash
# Activate venv first
venv\Scripts\activate  # Windows
source venv/bin/activate  # Mac/Linux

# Then install
pip install -r requirements.txt
```

### Issue 4: "Port 5000 is already in use"
**Solution:** Change port in app.py:
```python
if __name__ == '__main__':
    app = create_app()
    app.run(debug=True, host='0.0.0.0', port=5001)
```

### Issue 5: "Can't connect to MySQL server"
**Solution:**
```bash
# Check if MySQL is running
# Windows:
net start MySQL80

# Linux:
sudo systemctl start mysql

# macOS:
brew services start mysql
```

### Issue 6: Tables not created
**Solution:** Manually create tables:
```bash
python
>>> from app import create_app
>>> from models import db
>>> app = create_app()
>>> with app.app_context():
...     db.create_all()
>>> exit()
```

---

## Testing the Application

### 1. Create a Team
1. Click "Teams" in navigation
2. Click "+ Add Team"
3. Enter "Electrical Team"
4. Click "Save Team"
5. Add technicians: John Smith, Sarah Johnson

### 2. Create Equipment
1. Click "Equipment"
2. Click "+ Add Equipment"
3. Fill in:
   - Name: CNC Machine
   - Serial: CNC-001
   - Location: Factory Floor A
   - Team: Electrical Team
   - Default Tech: John Smith
4. Click "Save Equipment"

### 3. Create a Request
1. Click "+ New Request"
2. Fill in:
   - Subject: Machine making unusual noise
   - Type: Corrective
   - Equipment: CNC Machine (should auto-fill team!)
3. Click "Create Request"

### 4. Test Kanban
1. Navigate to Kanban Board
2. You should see your request in "New" column
3. Try dragging it to "In Progress"
4. Notification should appear

### 5. Test Calendar
1. Click "Calendar"
2. Click "+" on any date
3. Create a Preventive request
4. It should appear on that date

---

## Production Deployment

### Security Checklist
- [ ] Change SECRET_KEY in config.py
- [ ] Use environment variables for passwords
- [ ] Enable HTTPS
- [ ] Add user authentication
- [ ] Implement rate limiting
- [ ] Set DEBUG = False
- [ ] Use production WSGI server (Gunicorn)

### Deploy with Gunicorn
```bash
pip install gunicorn
gunicorn -w 4 -b 0.0.0.0:8000 app:app
```

### Deploy with Docker
```dockerfile
# Create Dockerfile
FROM python:3.9
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
CMD ["gunicorn", "-w", "4", "-b", "0.0.0.0:8000", "app:app"]
```

---

## Backup & Restore

### Backup Database
```bash
mysqldump -u root -p gearguard > gearguard_backup.sql
```

### Restore Database
```bash
mysql -u root -p gearguard < gearguard_backup.sql
```

---

## Uninstall

### Remove Virtual Environment
```bash
deactivate
rm -rf venv  # Mac/Linux
rmdir /s venv  # Windows
```

### Drop Database
```sql
mysql -u root -p
DROP DATABASE gearguard;
EXIT;
```

---

## Getting Help

If you encounter issues:

1. Check this guide's "Common Issues" section
2. Verify all prerequisites are installed correctly
3. Ensure MySQL service is running
4. Check config.py credentials
5. Look at terminal error messages carefully

---

## Next Steps

Once setup is complete:
1. Read the main README.md for features
2. Create sample data (teams, equipment, requests)
3. Test all workflows
4. Prepare your demo

---

**Setup Guide Version:** 1.0  
**Last Updated:** December 2024