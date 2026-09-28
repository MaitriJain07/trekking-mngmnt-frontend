from app import db, create_app
from app.models import User
from werkzeug.security import generate_password_hash
app=create_app()
with app.app_context():
    db.create_all()
    if not User.query.filter_by(email='admin@trekking.com').first():
        admin=User(
        name='admin',
        email='admin@trekking.com',
        password=generate_password_hash('admin123'),
        role='admin',
        is_approved=True
        )
        db.session.add(admin)
        db.session.commit()
