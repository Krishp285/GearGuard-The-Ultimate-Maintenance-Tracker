# GearGuard - Quick Reference Guide

## 🚀 One-Command Start

```bash
# Activate environment
venv\Scripts\activate  # Windows
source venv/bin/activate  # Mac/Linux

# Run
python app.py

# Open browser to: http://localhost:5000
```

---

## 📂 File Structure

```
gearguard/
├── app.py              ← Start here
├── config.py           ← MySQL settings
├── models.py           ← Database models
├── requirements.txt    ← Dependencies
├── routes/
│   ├── __init__.py
│   ├── equipment.py    ← Equipment CRUD
│   ├── teams.py        ← Team management
│   ├── requests.py     ← Request handling
│   └── dashboard.py    ← Views & calendar
├── templates/          ← HTML files
├── static/
│   ├── css/style.css   ← Styling
│   └── js/kanban.js    ← Drag & drop
└── README.md           ← Full documentation
```

---

## 🔑 Key Commands

### Virtual Environment
```bash
# Create
python -m venv venv

# Activate
venv\Scripts\activate          # Windows CMD
venv\Scripts\Activate.ps1      # Windows PowerShell
source venv/bin/activate       # Mac/Linux

# Deactivate
deactivate
```

### Install Dependencies
```bash
pip install -r requirements.txt
```

### Database
```sql
-- Create
CREATE DATABASE gearguard;

-- Backup
mysqldump -u root -p gearguard > backup.sql

-- Restore
mysql -u root -p gearguard < backup.sql
```

### Run Application
```bash
python app.py
```

---

## 🎯 Workflow Quick Guide

### 1. Setup (One-Time)
```
Install Python → Install MySQL → Create venv → 
pip install → Create database → Edit config.py → Run app
```

### 2. Daily Use
```
Activate venv → python app.py → Open browser
```

### 3. Demo Sequence
```
Create Teams → Add Technicians → Create Equipment → 
Create Requests → Test Kanban Drag → View Calendar
```

---

## 🗄️ Database Tables

| Table | Purpose | Key Fields |
|-------|---------|------------|
| `maintenance_team` | Teams | id, team_name |
| `technician` | Technicians | id, name, team_id |
| `equipment` | Equipment | id, name, serial, team_id, is_scrapped |
| `maintenance_request` | Requests | id, subject, type, equipment_id, status |

---

## 🔄 Request Status Flow

```
New → In Progress → Repaired
                 ↓
               Scrap (Equipment becomes unusable)
```

---

## 🎨 Key Features

| Feature | Location | Shortcut |
|---------|----------|----------|
| Kanban Board | `/dashboard/kanban` | Home button |
| Calendar | `/dashboard/calendar` | Calendar link |
| Equipment List | `/equipment/` | Equipment link |
| Teams | `/teams/` | Teams link |
| Create Request | `/requests/create` | + New Request |
| Dashboard Stats | `/dashboard/` | Dashboard link |

---

## ⚡ Auto-Fill Magic

When creating a request and selecting equipment:
```
Equipment Selected
    ↓
Automatically Fills:
    • Maintenance Team
    • Suggested Technician
    ↓
Only shows technicians from that team!
```

---

## 🚨 Overdue Detection

Requests are marked overdue if:
- ✅ Has scheduled_date
- ✅ scheduled_date < today
- ✅ Status is "New" OR "In Progress"

Display: **Red border + "OVERDUE" badge**

---

## 🗑️ Scrap Logic

When request moved to "Scrap":
```
1. Equipment.is_scrapped = True
2. Equipment shows "Scrapped" badge
3. New requests blocked for that equipment
4. Visual indicators throughout system
```

---

## 🔌 API Endpoints

| Endpoint | Method | Purpose |
|----------|--------|---------|
| `/equipment/api/technicians/<team_id>` | GET | Get team's technicians |
| `/equipment/api/details/<equipment_id>` | GET | Get equipment info |
| `/requests/update_status` | POST | Update request status (Kanban) |

---

## 🎬 5-Minute Demo Script

**Minute 1:** Create Teams & Technicians
- Create "Electrical Team"
- Add 2 technicians

**Minute 2:** Create Equipment
- Add "CNC Machine"
- Assign to Electrical Team
- Set default technician

**Minute 3:** Corrective Request
- Create breakdown request
- Show auto-fill working
- Drag through Kanban columns

**Minute 4:** Preventive Maintenance
- Create preventive request
- Set future date
- Show on calendar

**Minute 5:** Scrap Demo
- Drag request to Scrap
- Show equipment marked scrapped
- Try creating new request (blocked!)

---

## 🐛 Quick Troubleshooting

| Problem | Quick Fix |
|---------|-----------|
| Can't connect to MySQL | Check MySQL service is running |
| Import errors | Activate venv, reinstall requirements |
| Port in use | Change port in app.py |
| Tables not created | Run `db.create_all()` in Python shell |
| Wrong password | Update config.py |

---

## 📊 Sample Test Data

### Teams
- Electrical Team
- Mechanical Team
- IT Support

### Technicians (2 per team)
- Electrical: John Smith, Sarah Johnson
- Mechanical: Mike Brown, Emily Davis  
- IT: David Wilson, Lisa Anderson

### Equipment (5 items)
- CNC Machine (Mechanical)
- Transformer (Electrical)
- Industrial Printer (IT)
- Conveyor Belt (Mechanical)
- Server Rack (IT)

### Requests
- 2 Corrective (breakdowns)
- 2 Preventive (future dates)
- 1 Overdue preventive

---

## 🎓 Key Concepts

**Corrective Maintenance:**
- Breakdown/emergency repair
- No scheduled date required
- Created when equipment fails

**Preventive Maintenance:**
- Scheduled maintenance
- Date required
- Shows on calendar
- Planned in advance

**Auto-Fill:**
- Equipment → Team & Technician
- Saves time
- Prevents errors

**Drag & Drop:**
- Visual workflow
- Real-time updates
- Intuitive interface

---

## 🔐 Config.py Settings

```python
# MySQL Connection
MYSQL_USER = 'root'
MYSQL_PASSWORD = 'your_password'
MYSQL_HOST = 'localhost'
MYSQL_PORT = '3306'
MYSQL_DB = 'gearguard'

# Flask
SECRET_KEY = 'change-in-production'
DEBUG = True
```

---

## 📱 Navigation Menu

```
⚙️ GearGuard
├── Kanban Board    (Primary view)
├── Calendar        (Preventive maintenance)
├── Equipment       (Manage equipment)
├── Teams           (Manage teams)
├── Dashboard       (Statistics)
└── + New Request   (Create request)
```

---

## ✅ Testing Checklist

- [ ] Teams created
- [ ] Technicians added
- [ ] Equipment added
- [ ] Corrective request created
- [ ] Auto-fill works
- [ ] Kanban drag & drop works
- [ ] Preventive request on calendar
- [ ] Scrap logic works
- [ ] Dashboard shows stats
- [ ] Overdue requests highlighted

---

## 💡 Pro Tips

1. **Always create teams first** before equipment
2. **Assign default technicians** for faster request creation
3. **Use descriptive subjects** for easy identification
4. **Set realistic scheduled dates** for preventive maintenance
5. **Check dashboard daily** for overdue requests
6. **Filter equipment list** by department for large setups
7. **Drag from right to left** feels natural (New → Scrap)

---

## 🚀 Performance Tips

- Equipment list: Use filters for > 50 items
- Requests: Archive old repaired requests monthly
- Calendar: Focus on current month
- Dashboard: Check at start of day

---

## 📞 Quick Help

**Issue:** Something not working?
**First:** Check terminal for error messages
**Second:** Verify MySQL is running
**Third:** Check config.py settings
**Fourth:** Restart application

---

**Quick Reference Version:** 1.0  
**For Full Details:** See README.md