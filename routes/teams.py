from flask import Blueprint, render_template, request, redirect, url_for, flash
from models import db, MaintenanceTeam, Technician

bp = Blueprint('teams', __name__, url_prefix='/teams')

@bp.route('/')
def list_teams():
    """List all maintenance teams"""
    teams = MaintenanceTeam.query.all()
    return render_template('teams.html', teams=teams)

@bp.route('/create', methods=['GET', 'POST'])
def create():
    """Create new maintenance team"""
    if request.method == 'POST':
        try:
            team = MaintenanceTeam(
                team_name=request.form['team_name']
            )
            
            db.session.add(team)
            db.session.commit()
            
            flash('Team created successfully!', 'success')
            return redirect(url_for('teams.list_teams'))
        
        except Exception as e:
            db.session.rollback()
            flash(f'Error creating team: {str(e)}', 'error')
    
    return render_template('team_form.html', team=None)

@bp.route('/edit/<int:id>', methods=['GET', 'POST'])
def edit(id):
    """Edit maintenance team"""
    team = MaintenanceTeam.query.get_or_404(id)
    
    if request.method == 'POST':
        try:
            team.team_name = request.form['team_name']
            db.session.commit()
            
            flash('Team updated successfully!', 'success')
            return redirect(url_for('teams.list_teams'))
        
        except Exception as e:
            db.session.rollback()
            flash(f'Error updating team: {str(e)}', 'error')
    
    return render_template('team_form.html', team=team)

@bp.route('/delete/<int:id>', methods=['POST'])
def delete(id):
    """Delete maintenance team"""
    team = MaintenanceTeam.query.get_or_404(id)
    
    try:
        db.session.delete(team)
        db.session.commit()
        flash('Team deleted successfully!', 'success')
    except Exception as e:
        db.session.rollback()
        flash(f'Error deleting team: {str(e)}', 'error')
    
    return redirect(url_for('teams.list_teams'))

@bp.route('/<int:team_id>/technician/create', methods=['POST'])
def create_technician(team_id):
    """Add technician to team"""
    team = MaintenanceTeam.query.get_or_404(team_id)
    
    try:
        technician = Technician(
            name=request.form['name'],
            team_id=team_id
        )
        
        db.session.add(technician)
        db.session.commit()
        
        flash('Technician added successfully!', 'success')
    except Exception as e:
        db.session.rollback()
        flash(f'Error adding technician: {str(e)}', 'error')
    
    return redirect(url_for('teams.list_teams'))

@bp.route('/technician/<int:id>/delete', methods=['POST'])
def delete_technician(id):
    """Delete technician"""
    technician = Technician.query.get_or_404(id)
    
    try:
        db.session.delete(technician)
        db.session.commit()
        flash('Technician deleted successfully!', 'success')
    except Exception as e:
        db.session.rollback()
        flash(f'Error deleting technician: {str(e)}', 'error')
    
    return redirect(url_for('teams.list_teams'))