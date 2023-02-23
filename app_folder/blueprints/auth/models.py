from app_folder.extensions import db
from app_folder.extensions import login_manager
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from flask import current_app

@login_manager.user_loader
def load_user(id):
    return User.query.get(int(id))

class User(db.Model, UserMixin):
    id = db.Column(db.Integer,primary_key=True)
    first_name = db.Column(db.String, nullable=False)
    last_name = db.Column(db.String, nullable=False)
    email = db.Column(db.String, nullable=False, unique=True)
    #password = db.Column(db.String, nullable=False)
    hash_password = db.Column(db.String(250))
    

    @property
    def password(self):
        raise AttributeError("password is not a readable property")

    @password.setter
    def password(self,password):
        self.hash_password = generate_password_hash(password)
    
    def verify_password(self,password):
        return check_password_hash(self.hash_password,password)

    def generate_password_rest_token(self):
        s = Serializer(current_app.config['SECRET_KEY'], expires_in=3600)
        return s.dumps({"user":self.id}).decode("utf-8")

    @staticmethod 
    def confirm_password_reset_token(token,new_password):
        s = Serializer(current_app.config['SECRET_KEY'])
        try:
            data = s.loads(token)
        except:
            return False
        user = User.query.get(int(data.get('user')))
        if User is None:
            return False
        user.password = new_password
        db.session.add(user)
        db.session.commit()
        return True

        


    
#flask db migrate -m "Updating Coloumn"
#flask db upgrade