from flask import Flask, render_template, redirect, url_for
from config import Config
from models import db
import routes.equipment as equipment_routes
import routes.teams as teams_routes
import routes.requests as requests_routes
import routes.dashboard as dashboard_routes

app = Flask(__name__)
app.config.from_object(Config)

# Initialize database
db.init_app(app)

# Register blueprints
app.register_blueprint(equipment_routes.bp)
app.register_blueprint(teams_routes.bp)
app.register_blueprint(requests_routes.bp)
app.register_blueprint(dashboard_routes.bp)

@app.route('/')
def index():
    return redirect(url_for('dashboard.kanban'))

# Create tables
with app.app_context():
    db.create_all()

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)