from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify
from models import db, MaintenanceRequest, Equipment, MaintenanceTeam, Technician
from datetime import datetime

bp = Blueprint('requests', __name__, url_prefix='/requests')

@bp.route('/create', methods=['GET', 'POST'])
def create():
    """Create new maintenance request"""
    if request.method == 'POST':
        try:
            equipment_id = int(request.form['equipment_id'])
            equipment = Equipment.query.get(equipment_id)
            
            # Block requests for scrapped equipment
            if equipment.is_scrapped:
                flash('Cannot create request for scrapped equipment!', 'error')
                return redirect(url_for('requests.create'))
            
            # Create request
            maintenance_request = MaintenanceRequest(
                subject=request.form['subject'],
                request_type=request.form['request_type'],
                equipment_id=equipment_id,
                maintenance_team_id=int(request.form['maintenance_team_id']),
                assigned_technician_id=int(request.form['assigned_technician_id']) if request.form.get('assigned_technician_id') else None,
                scheduled_date=datetime.strptime(request.form['scheduled_date'], '%Y-%m-%d').date() if request.form.get('scheduled_date') else None,
                priority=request.form.get('priority', 'Medium'),
                status='New'
            )
            
            db.session.add(maintenance_request)
            db.session.commit()
            
            flash('Maintenance request created successfully!', 'success')
            return redirect(url_for('dashboard.kanban'))
        
        except Exception as e:
            db.session.rollback()
            flash(f'Error creating request: {str(e)}', 'error')
    
    equipment_list = Equipment.query.filter_by(is_scrapped=False).all()
    teams = MaintenanceTeam.query.all()
    
    # Pre-fill from query params (for calendar)
    scheduled_date = request.args.get('date', '')
    
    return render_template('request_form.html', 
                         equipment_list=equipment_list, 
                         teams=teams,
                         request_obj=None,
                         scheduled_date=scheduled_date)

@bp.route('/edit/<int:id>', methods=['GET', 'POST'])
def edit(id):
    """Edit maintenance request"""
    maintenance_request = MaintenanceRequest.query.get_or_404(id)
    
    if request.method == 'POST':
        try:
            maintenance_request.subject = request.form['subject']
            maintenance_request.request_type = request.form['request_type']
            maintenance_request.equipment_id = int(request.form['equipment_id'])
            maintenance_request.maintenance_team_id = int(request.form['maintenance_team_id'])
            maintenance_request.assigned_technician_id = int(request.form['assigned_technician_id']) if request.form.get('assigned_technician_id') else None
            maintenance_request.scheduled_date = datetime.strptime(request.form['scheduled_date'], '%Y-%m-%d').date() if request.form.get('scheduled_date') else None
            maintenance_request.duration_hours = float(request.form['duration_hours']) if request.form.get('duration_hours') else None
            maintenance_request.priority = request.form.get('priority', 'Medium')

            db.session.commit()
            
            flash('Request updated successfully!', 'success')
            return redirect(url_for('dashboard.kanban'))
        
        except Exception as e:
            db.session.rollback()
            flash(f'Error updating request: {str(e)}', 'error')
    
    equipment_list = Equipment.query.all()
    teams = MaintenanceTeam.query.all()
    
    return render_template('request_form.html', 
                         equipment_list=equipment_list, 
                         teams=teams,
                         request_obj=maintenance_request,
                         scheduled_date='')

@bp.route('/delete/<int:id>', methods=['POST'])
def delete_request(id):
    """Delete maintenance request"""
    maintenance_request = MaintenanceRequest.query.get_or_404(id)
    
    try:
        db.session.delete(maintenance_request)
        db.session.commit()
        flash('Request deleted successfully!', 'success')
    except Exception as e:
        db.session.rollback()
        flash(f'Error deleting request: {str(e)}', 'error')
    
    return redirect(url_for('dashboard.kanban'))

@bp.route('/update_status', methods=['POST'])
def update_status():
    """Update request status (for Kanban drag & drop)"""
    data = request.get_json()
    request_id = data.get('request_id')
    new_status = data.get('status')
    
    try:
        maintenance_request = MaintenanceRequest.query.get(request_id)
        if not maintenance_request:
            return jsonify({'success': False, 'message': 'Request not found'}), 404
        
        # Scrap logic: mark equipment as scrapped
        if new_status == 'Scrap':
            equipment = Equipment.query.get(maintenance_request.equipment_id)
            equipment.is_scrapped = True
        
        maintenance_request.status = new_status
        db.session.commit()
        
        return jsonify({'success': True})
    
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'message': str(e)}), 500

@bp.route('/delete/<int:id>', methods=['POST'])
def delete(id):
    """Delete maintenance request"""
    maintenance_request = MaintenanceRequest.query.get_or_404(id)
    
    try:
        db.session.delete(maintenance_request)
        db.session.commit()
        flash('Request deleted successfully!', 'success')
    except Exception as e:
        db.session.rollback()
        flash(f'Error deleting request: {str(e)}', 'error')
    
    return redirect(url_for('dashboard.kanban'))