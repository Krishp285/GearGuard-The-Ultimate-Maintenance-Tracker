from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from models import db, User
from werkzeug.security import generate_password_hash, check_password_hash

auth = Blueprint('auth', __name__)

# ---------------- LOGIN ----------------
@auth.route('/login', methods=['GET', 'POST'])
def login():
    if 'user_id' in session:
        return redirect_user_by_role()

    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        user = User.query.filter_by(email=email).first()

        if user and user.check_password(password):
            session['user_id'] = user.id
            session['role'] = user.role
            session['technician_id'] = user.technician_id

            flash('Login successful!', 'success')
            return redirect_user_by_role()

        flash('Invalid email or password', 'error')

    return render_template('auth/login.html')


# ---------------- SIGNUP ----------------
@auth.route('/signup', methods=['GET', 'POST'])
def signup():
    if 'user_id' in session:
        return redirect_user_by_role()

    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        password = request.form['password']
        role = request.form['role']  # Admin / Technician

        if User.query.filter_by(email=email).first():
            flash('Email already exists', 'error')
            return redirect(url_for('auth.signup'))

        user = User(
            name=name,
            email=email,
            role=role
        )
        user.set_password(password)

        db.session.add(user)
        db.session.commit()

        session['user_id'] = user.id
        session['role'] = user.role
        session['technician_id'] = user.technician_id

        flash('Account created successfully!', 'success')
        return redirect_user_by_role()

    return render_template('auth/signup.html')

# ---------------- LOGOUT ----------------
@auth.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('auth.login'))


# ---------------- ROLE REDIRECT HELPER ----------------
def redirect_user_by_role():
    if session.get('role') == 'Admin':
        return redirect(url_for('dashboard.dashboard'))
    elif session.get('role') == 'Technician':
        return redirect(url_for('dashboard.technician_dashboard'))
    return redirect(url_for('auth.login'))
