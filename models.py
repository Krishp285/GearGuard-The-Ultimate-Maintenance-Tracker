from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash

db = SQLAlchemy()

class MaintenanceTeam(db.Model):
    __tablename__ = 'maintenance_team'
    
    id = db.Column(db.Integer, primary_key=True)
    team_name = db.Column(db.String(100), nullable=False, unique=True)
    
    # Relationships
    technicians = db.relationship('Technician', backref='team', lazy=True, cascade='all, delete-orphan')
    equipment = db.relationship('Equipment', backref='maintenance_team', lazy=True)
    requests = db.relationship('MaintenanceRequest', backref='maintenance_team', lazy=True)
    

class Technician(db.Model):
    __tablename__ = 'technician'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    team_id = db.Column(db.Integer, db.ForeignKey('maintenance_team.id'), nullable=False)
    
    # Relationships
    default_equipment = db.relationship('Equipment', backref='default_technician', lazy=True)
    assigned_requests = db.relationship('MaintenanceRequest', backref='assigned_technician', lazy=True)

class Equipment(db.Model):
    __tablename__ = 'equipment'
    
    id = db.Column(db.Integer, primary_key=True)
    equipment_name = db.Column(db.String(200), nullable=False)
    serial_number = db.Column(db.String(100), nullable=False, unique=True)
    department = db.Column(db.String(100), nullable=True)
    assigned_employee = db.Column(db.String(100), nullable=True)
    purchase_date = db.Column(db.Date, nullable=True)
    warranty_expiry = db.Column(db.Date, nullable=True)
    location = db.Column(db.String(200), nullable=False)
    maintenance_team_id = db.Column(db.Integer, db.ForeignKey('maintenance_team.id'), nullable=False)
    default_technician_id = db.Column(db.Integer, db.ForeignKey('technician.id'), nullable=True)
    is_scrapped = db.Column(db.Boolean, default=False, nullable=False)
    
    # Relationships
    requests = db.relationship('MaintenanceRequest', backref='equipment', lazy=True)
    
    def open_requests_count(self):
        """Count open requests (New or In Progress)"""
        return MaintenanceRequest.query.filter(
            MaintenanceRequest.equipment_id == self.id,
            MaintenanceRequest.status.in_(['New', 'In Progress'])
        ).count()

class MaintenanceRequest(db.Model):
    __tablename__ = 'maintenance_request'
    
    id = db.Column(db.Integer, primary_key=True)
    subject = db.Column(db.String(200), nullable=False)
    request_type = db.Column(db.String(20), nullable=False)  # Corrective, Preventive
    equipment_id = db.Column(db.Integer, db.ForeignKey('equipment.id'), nullable=False)
    maintenance_team_id = db.Column(db.Integer, db.ForeignKey('maintenance_team.id'), nullable=False)
    assigned_technician_id = db.Column(db.Integer, db.ForeignKey('technician.id'), nullable=True)
    scheduled_date = db.Column(db.Date, nullable=True)
    duration_hours = db.Column(db.Float, nullable=True)
    status = db.Column(db.String(20), default='New', nullable=False)  # New, In Progress, Repaired, Scrap
    priority = db.Column(db.String(10), nullable=False, default='Medium')

    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    
    def is_overdue(self):
        """Check if request is overdue"""
        if self.scheduled_date and self.status in ['New', 'In Progress']:
            return self.scheduled_date < datetime.utcnow().date()
        return False
    

class User(db.Model):
    __tablename__ = 'user'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)

    role = db.Column(db.String(20), nullable=False)  # Admin / Technician
    technician_id = db.Column(db.Integer, db.ForeignKey('technician.id'), nullable=True)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)