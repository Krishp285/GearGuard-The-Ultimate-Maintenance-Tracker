from flask import Flask, redirect, url_for, session
from config import Config
from models import db
import routes.equipment as equipment_routes
import routes.teams as teams_routes
import routes.requests as requests_routes
import routes.dashboard as dashboard_routes
from routes.auth import auth



app = Flask(__name__)
app.config.from_object(Config)

# Initialize database
db.init_app(app)

# Register blueprints
app.register_blueprint(equipment_routes.bp)
app.register_blueprint(teams_routes.bp)
app.register_blueprint(requests_routes.bp)
app.register_blueprint(dashboard_routes.bp)

app.register_blueprint(auth)


@app.route('/')
def index():
    if 'user_id' not in session:
        return redirect(url_for('auth.login'))

    # redirect by role
    if session.get('role') == 'Admin':
        return redirect(url_for('dashboard.dashboard'))
    elif session.get('role') == 'Technician':
        return redirect(url_for('dashboard.technician_dashboard'))

    return redirect(url_for('auth.login'))


# Create tables
with app.app_context():
    db.create_all()

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)