from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_wtf.csrf import CSRFProtect

# Assuming db is initialized in app.py and passed or accessed via current_app
# from flask import current_app as app
# db = app.config['DB'] # Example if db is stored in app config

main_bp = Blueprint('main', __name__)

# This will be passed from app.py
_db = None
_csrf = None

def set_db_and_csrf(db_instance, csrf_instance):
    global _db, _csrf
    _db = db_instance
    _csrf = csrf_instance

@main_bp.route('/')
def index():
    """Display all users"""
    try:
        users = _db.get_all_users()
        return render_template('index.html', users=users)
    except Exception as e:
        flash(f'Error loading users: {str(e)}', 'error')
        return render_template('index.html', users=[])


@main_bp.route('/add', methods=['GET', 'POST'])
def add_user():
    """Add a new user"""
    if request.method == 'POST':
        name = request.form.get('name')
        email = request.form.get('email')
        address = request.form.get('address')
        
        if name and email and address:
            try:
                user_id = _db.add_user(name, email, address)
                if user_id:
                    flash('User added successfully!', 'success')
                else:
                    flash('Email already exists!', 'error')
            except Exception as e:
                flash(f'Error adding user: {str(e)}', 'error')
            return redirect(url_for('main.index'))
        else:
            flash('Please provide both name and email', 'error')
    
    return render_template('add_user.html')


@main_bp.route('/update/<int:user_id>', methods=['GET', 'POST'])
def update_user(user_id):
    """Update an existing user"""
    if request.method == 'POST':
        name = request.form.get('name')
        email = request.form.get('email')
        address = request.form.get('address')
        
        if name and email and address:
            try:
                success = _db.update_user(user_id, name, email, address)
                if success:
                    flash('User updated successfully!', 'success')
                else:
                    flash('Failed to update user!', 'error')
            except Exception as e:
                flash(f'Error updating user: {str(e)}', 'error')
            return redirect(url_for('main.index'))
        else:
            flash('Please provide both name and email', 'error')
    
    try:
        user = _db.get_user(user_id)
        if not user:
            flash('User not found', 'error')
            return redirect(url_for('main.index'))
        return render_template('update_user.html', user=user)
    except Exception as e:
        flash(f'Error loading user: {str(e)}', 'error')
        return redirect(url_for('main.index'))


@main_bp.route('/delete/<int:user_id>')
def delete_user(user_id):
    """Delete a user"""
    try:
        success = _db.delete_user(user_id)
        if success:
            flash('User deleted successfully!', 'success')
        else:
            flash('Failed to delete user!', 'error')
    except Exception as e:
        flash(f'Error deleting user: {str(e)}', 'error')
    return redirect(url_for('main.index'))

@main_bp.route('/favicon.ico')
def favicon():
    """Handle favicon requests to prevent 404 errors."""
    return '', 204
