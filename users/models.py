
from users import db

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(100), unique=True, nullable=False)
    username = db.Column(db.String(20), unique=True, nullable=False)


    def __repr__(self):
        return 'User(%r, %r)' % (self.email, self.username)

    


