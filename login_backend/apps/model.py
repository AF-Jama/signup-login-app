from app import db
import bcrypt
from datetime import datetime
'''Database/model creation'''



class User(db.Model):
    '''User model'''
    __tablename__ = "theUsers"
    id = db.Column(db.Integer,primary_key = True,nullable = False)
    userName  = db.Column(db.String(100),nullable = False)
    password = db.Column(db.String(100),nullable = False)
    date_created = db.Column(db.DateTime, default = datetime.utcnow)

    def is_password_valid(self, password):
        return bcrypt.checkpw(password.encode('utf-8'), self.password.encode('utf-8'))


    def __repr__(self) -> str:
        return f'{self.id}:{self.userName}'


db.create_all()


# first = User(userName = "James123",password = "Testpassword123.")

# try:
#     db.session.add(first)
#     db.session.commit()

# except:
#     print("Rollback")
#     db.session.rollback()

a = User.query.count()

print("Number",a)
