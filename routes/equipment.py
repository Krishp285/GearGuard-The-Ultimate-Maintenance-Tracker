from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify
from models import db, Equipment, MaintenanceTeam, Technician
from datetime import datetime

bp = Blueprint('equipment', __name__, url_prefix='/equipment')

@bp.route('/')
def list_equipment():
    """List all equipment with filters"""
    department_filter = request.args.get('department', '')
    employee_filter = request.args.get('employee', '')
    search_query = request.args.get('search', '')
    
    query = Equipment.query
    
    if department_filter:
        query = query.filter(Equipment.department == department_filter)
    
    if employee_filter:
        query = query.filter(Equipment.assigned_employee == employee_filter)
    
    if search_query:
        query = query.filter(
            db.or_(
                Equipment.equipment_name.like(f'%{search_query}%'),
                Equipment.serial_number.like(f'%{search_query}%')
            )
        )
    
    equipment_list = query.all()
    
    # Get unique departments and employees for filters
    departments = db.session.query(Equipment.department).distinct().filter(Equipment.department.isnot(None)).all()
    departments = [d[0] for d in departments]
    
    employees = db.session.query(Equipment.assigned_employee).distinct().filter(Equipment.assigned_employee.isnot(None)).all()
    employees = [e[0] for e in employees]
    
    return render_template('equipment.html', 
                         equipment_list=equipment_list,
                         departments=departments,
                         employees=employees,
                         current_department=department_filter,
                         current_employee=employee_filter,
                         current_search=search_query)

@bp.route('/create', methods=['GET', 'POST'])
def create():
    """Create new equipment"""
    if request.method == 'POST':
        try:
            equipment = Equipment(
                equipment_name=request.form['equipment_name'],
                serial_number=request.form['serial_number'],
                department=request.form.get('department') or None,
                assigned_employee=request.form.get('assigned_employee') or None,
                purchase_date=datetime.strptime(request.form['purchase_date'], '%Y-%m-%d').date() if request.form.get('purchase_date') else None,
                warranty_expiry=datetime.strptime(request.form['warranty_expiry'], '%Y-%m-%d').date() if request.form.get('warranty_expiry') else None,
                location=request.form['location'],
                maintenance_team_id=int(request.form['maintenance_team_id']),
                default_technician_id=int(request.form['default_technician_id']) if request.form.get('default_technician_id') else None,
                is_scrapped=False
            )
            
            db.session.add(equipment)
            db.session.commit()
            
            flash('Equipment created successfully!', 'success')
            return redirect(url_for('equipment.list_equipment'))
        
        except Exception as e:
            db.session.rollback()
            flash(f'Error creating equipment: {str(e)}', 'error')
    
    teams = MaintenanceTeam.query.all()
    return render_template('equipment_form.html', teams=teams, equipment=None)

@bp.route('/edit/<int:id>', methods=['GET', 'POST'])
def edit(id):
    """Edit equipment"""
    equipment = Equipment.query.get_or_404(id)
    
    if request.method == 'POST':
        try:
            equipment.equipment_name = request.form['equipment_name']
            equipment.serial_number = request.form['serial_number']
            equipment.department = request.form.get('department') or None
            equipment.assigned_employee = request.form.get('assigned_employee') or None
            equipment.purchase_date = datetime.strptime(request.form['purchase_date'], '%Y-%m-%d').date() if request.form.get('purchase_date') else None
            equipment.warranty_expiry = datetime.strptime(request.form['warranty_expiry'], '%Y-%m-%d').date() if request.form.get('warranty_expiry') else None
            equipment.location = request.form['location']
            equipment.maintenance_team_id = int(request.form['maintenance_team_id'])
            equipment.default_technician_id = int(request.form['default_technician_id']) if request.form.get('default_technician_id') else None
            
            db.session.commit()
            
            flash('Equipment updated successfully!', 'success')
            return redirect(url_for('equipment.list_equipment'))
        
        except Exception as e:
            db.session.rollback()
            flash(f'Error updating equipment: {str(e)}', 'error')
    
    teams = MaintenanceTeam.query.all()
    return render_template('equipment_form.html', teams=teams, equipment=equipment)

@bp.route('/delete/<int:id>', methods=['POST'])
def delete(id):
    """Delete equipment"""
    equipment = Equipment.query.get_or_404(id)
    
    try:
        db.session.delete(equipment)
        db.session.commit()
        flash('Equipment deleted successfully!', 'success')
    except Exception as e:
        db.session.rollback()
        flash(f'Error deleting equipment: {str(e)}', 'error')
    
    return redirect(url_for('equipment.list_equipment'))

@bp.route('/api/technicians/<int:team_id>')
def get_technicians(team_id):
    """API endpoint to get technicians for a team"""
    technicians = Technician.query.filter_by(team_id=team_id).all()
    return jsonify([{'id': t.id, 'name': t.name} for t in technicians])

@bp.route('/api/details/<int:equipment_id>')
def get_equipment_details(equipment_id):
    """API endpoint to get equipment details for auto-fill"""
    equipment = Equipment.query.get_or_404(equipment_id)
    return jsonify({
        'maintenance_team_id': equipment.maintenance_team_id,
        'default_technician_id': equipment.default_technician_id,
        'is_scrapped': equipment.is_scrapped
    })