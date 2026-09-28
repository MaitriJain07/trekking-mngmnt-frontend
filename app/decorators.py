from functools import wraps
from flask import session, redirect, url_for, flash
from app.models import User
def check_login():
    if 'user_id' not in session:
        flash("Please Login!")
        return redirect(url_for("main.login"))
    return None

def check_blacklisted(user):
    if user.is_blacklisted:
        session.clear()
        flash("You have been Blacklisted. Please contact Admin")
        return redirect(url_for('main.home'))
    return None

def login_as_admin(f):
    @wraps(f)
    def decorated_function(*args,**kwargs):
        #check if the user is logged in  between sessions
        response=check_login()
        if response:
            return response
        #check if the user got blacklisted between valid sessions
        user=User.query.get(session['user_id'])
        blacklisted=check_blacklisted(user)
        if blacklisted:
            return blacklisted
        if session['role']!='admin':
            flash(f'Access Denied')
            return redirect(url_for(f"main.{session['role']}_dashboard"))
        else:
            return f(*args,**kwargs)
    return decorated_function

def login_as_staff(f):
    @wraps(f)
    def decorated_function(*args,**kwargs):
        response=check_login()
        if response:
            return response
        user=User.query.get(session['user_id'])
        blacklisted=check_blacklisted(user)
        if blacklisted:
            return blacklisted
        
        if session['role']!='staff':
            flash(f'Access Denied')
            return redirect(url_for(f"main.{session['role']}_dashboard"))
        else:
            return f(*args,**kwargs)
    return decorated_function

def login_as_trekker(f):
    @wraps(f)
    def decorated_function(*args,**kwargs):
        response=check_login()
        if response:
            return response
        user=User.query.get(session['user_id'])
        blacklisted=check_blacklisted(user)
        if blacklisted:
            return blacklisted
        
        if session['role']!='trekker':
            flash(f'Access Denied')
            return redirect(url_for(f"main.{session['role']}_dashboard"))
        else:
            return f(*args,**kwargs)
    return decorated_function