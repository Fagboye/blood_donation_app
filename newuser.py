from app import app, db, User 

with app.app_context():
    user = User(username='john', password='password123', first_name='John', last_name='Doe', gender='male', blood_group="B+")
    db.session.add(user)
    db.session.commit()


