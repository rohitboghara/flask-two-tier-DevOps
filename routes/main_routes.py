from flask import Blueprint, render_template, request, redirect, url_for, flash, current_app
from forms import UserForm, UpdateUserForm

main_bp = Blueprint('main', __name__)

@main_bp.route('/')
def index():
    """Display all users"""
    try:
        current_app.logger.info("Viewing all user details", extra={
            "event": "view_users",
            "ip": request.remote_addr
        })
        users = current_app.db.get_all_users()
        return render_template('index.html', users=users)
    except Exception as e:
        current_app.logger.error(f"Error loading users: {str(e)}", extra={
            "event": "error_loading_users",
            "ip": request.remote_addr
        })
        flash(f'Error loading users: {str(e)}', 'error')
        return render_template('index.html', users=[])


@main_bp.route('/add', methods=['GET', 'POST'])
def add_user():
    """Add a new user"""
    form = UserForm()
    if form.validate_on_submit():
        name = form.name.data
        email = form.email.data
        address = form.address.data
        
        try:
            user_id = current_app.db.add_user(name, email, address)
            if user_id:
                current_app.logger.info(f"User created: {name}", extra={
                    "event": "user_created",
                    "username": name,
                    "email": email,
                    "ip": request.remote_addr
                })
                flash('User added successfully!', 'success')
            else:
                flash('Email already exists or a user with that name already exists!', 'error')
            return redirect(url_for('main.index'))
        except Exception as e:
            current_app.logger.error(f"Error creating user: {str(e)}", extra={
                "event": "user_creation_failed",
                "username": name,
                "email": email,
                "ip": request.remote_addr
            })
            flash(f'Error adding user: {str(e)}', 'error')
            return redirect(url_for('main.index'))
    
    # Flash form errors if any
    for field, errors in form.errors.items():
        for error in errors:
            flash(f"Error in {getattr(form, field).label.text}: {error}", 'error')

    return render_template('add_user.html', form=form)


@main_bp.route('/update/<int:user_id>', methods=['GET', 'POST'])
def update_user(user_id):
    """Update an existing user"""
    form = UpdateUserForm()
    if form.validate_on_submit():
        name = form.name.data
        email = form.email.data
        address = form.address.data
        
        try:
            success = current_app.db.update_user(user_id, name, email, address)
            if success:
                flash('User updated successfully!', 'success')
            else:
                flash('Failed to update user!', 'error')
            return redirect(url_for('main.index'))
        except Exception as e:
            flash(f'Error updating user: {str(e)}', 'error')
            return redirect(url_for('main.index'))
    
    # If GET request or validation failed
    try:
        user = current_app.db.get_user(user_id)
        if not user:
            flash('User not found', 'error')
            return redirect(url_for('main.index'))
        
        # Populate form with user data for GET request
        if request.method == 'GET':
            form.name.data = user['name']
            form.email.data = user['email']
            form.address.data = user['address']
        
        return render_template('update_user.html', form=form, user=user)
    except Exception as e:
        flash(f'Error loading user: {str(e)}', 'error')
        return redirect(url_for('main.index'))


@main_bp.route('/delete/<int:user_id>')
def delete_user(user_id):
    """Delete a user"""
    try:
        success = current_app.db.delete_user(user_id)
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
