from config.db import db, ma, app

class User(db.Model):
    __tablename__ = "user"
    
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(255))
    contraseña = db.Column(db.String(255))
    user = db.Column(db.String(255))
    is_admin = db.Column(db.Boolean)

    def __init__(self, nombre, contraseña, user, is_admin):
        self.nombre = nombre
        self.contraseña = contraseña
        self.user = user
        self.is_admin = is_admin

def create_default_data():
    if not User.query.first():
        users = [
            User(nombre='Jesus Garcia', contraseña='jgarcia123', user='jesusgarcia123', is_admin=True),
            User(nombre='Juan Verdugo', contraseña='jberdugo123', user='juanberdugo123', is_admin=True),
            User(nombre='David Campo', contraseña='dcampo123', user='davidcampo123', is_admin=True)
        ]
        db.session.add_all(users)
        db.session.commit()

with app.app_context():
    db.create_all()
    create_default_data()

class UserSchema(ma.Schema):
    class Meta:
        fields = ('id', 'nombre', 'contraseña', 'user', 'rol')

user_schema = UserSchema()
users_schema = UserSchema(many=True)
