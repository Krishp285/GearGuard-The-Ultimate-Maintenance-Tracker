"""
GearGuard - Dashboard Routes
"""
from flask import Blueprint, render_template, request
from models import db, MaintenanceRequest, Equipment
from datetime import datetime
from calendar import monthrange

bp = Blueprint('dashboard', __name__, url_prefix='/dashboard')


@bp.route('/kanban')
def kanban():
    """Kanban board view - primary screen"""
    # Get all requests organized by status
    PRIORITY_ORDER = {
    'High': 1,
    'Medium': 2,
    'Low': 3
    }

    new_requests = MaintenanceRequest.query.filter_by(status='New').all()
    new_requests.sort(key=lambda r: PRIORITY_ORDER.get(r.priority, 2))
    
    in_progress_requests = MaintenanceRequest.query.filter_by(status='In Progress').order_by(
        MaintenanceRequest.created_at.desc()
    ).all()
    
    repaired_requests = MaintenanceRequest.query.filter_by(status='Repaired').order_by(
        MaintenanceRequest.created_at.desc()
    ).all()
    
    scrap_requests = MaintenanceRequest.query.filter_by(status='Scrap').order_by(
        MaintenanceRequest.created_at.desc()
    ).all()
    
    return render_template(
        'kanban.html',
        new_requests=new_requests,
        in_progress_requests=in_progress_requests,
        repaired_requests=repaired_requests,
        scrap_requests=scrap_requests
    )


@bp.route('/calendar')
def calendar_view():
    """Calendar view for preventive maintenance"""
    # Get current month and year from query params or use current date
    year = int(request.args.get('year', datetime.now().year))
    month = int(request.args.get('month', datetime.now().month))
    
    # Calculate previous and next month
    if month == 1:
        prev_month, prev_year = 12, year - 1
    else:
        prev_month, prev_year = month - 1, year
    
    if month == 12:
        next_month, next_year = 1, year + 1
    else:
        next_month, next_year = month + 1, year
    
    # Get first and last day of the month
    first_day = datetime(year, month, 1)
    last_day_num = monthrange(year, month)[1]
    last_day = datetime(year, month, last_day_num)
    
    # Get all preventive maintenance requests for this month
    preventive_requests = MaintenanceRequest.query.filter(
        MaintenanceRequest.request_type == 'Preventive',
        MaintenanceRequest.scheduled_date >= first_day.date(),
        MaintenanceRequest.scheduled_date <= last_day.date()
    ).all()
    
    # Organize requests by date
    requests_by_date = {}
    for req in preventive_requests:
        date_key = req.scheduled_date.day
        if date_key not in requests_by_date:
            requests_by_date[date_key] = []
        requests_by_date[date_key].append(req)
    
    # Build calendar grid
    calendar_grid = []
    first_weekday = first_day.weekday()  # Monday = 0, Sunday = 6
    
    # Adjust for Sunday start (0 = Sunday)
    first_weekday = (first_weekday + 1) % 7
    
    # Add empty cells for days before month starts
    current_week = [None] * first_weekday
    
    for day in range(1, last_day_num + 1):
        current_week.append(day)
        
        if len(current_week) == 7:
            calendar_grid.append(current_week)
            current_week = []
    
    # Fill remaining days with None
    if current_week:
        while len(current_week) < 7:
            current_week.append(None)
        calendar_grid.append(current_week)
    
    return render_template(
        'calendar.html',
        year=year,
        month=month,
        month_name=first_day.strftime('%B'),
        calendar_grid=calendar_grid,
        requests_by_date=requests_by_date,
        prev_month=prev_month,
        prev_year=prev_year,
        next_month=next_month,
        next_year=next_year
    )


@bp.route('/')
def dashboard():
    """Main dashboard with statistics"""
    total_equipment = Equipment.query.count()
    scrapped_equipment = Equipment.query.filter_by(is_scrapped=True).count()
    active_equipment = total_equipment - scrapped_equipment
    
    total_requests = MaintenanceRequest.query.count()
    new_requests = MaintenanceRequest.query.filter_by(status='New').count()
    in_progress_requests = MaintenanceRequest.query.filter_by(status='In Progress').count()
    repaired_requests = MaintenanceRequest.query.filter_by(status='Repaired').count()
    
    # Overdue requests
    overdue_requests = MaintenanceRequest.query.filter(
        MaintenanceRequest.scheduled_date < datetime.now().date(),
        MaintenanceRequest.status.in_(['New', 'In Progress'])
    ).all()
    
    return render_template(
        'dashboard.html',
        total_equipment=total_equipment,
        active_equipment=active_equipment,
        scrapped_equipment=scrapped_equipment,
        total_requests=total_requests,
        new_requests=new_requests,
        in_progress_requests=in_progress_requests,
        repaired_requests=repaired_requests,
        overdue_requests=overdue_requests
    )