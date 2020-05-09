from login_example import db, User
# anthony = User(username='Anthony')
# db.session.add(anthony)
# db.session.commit()
result = User.query.all()
print(result[0].username)
