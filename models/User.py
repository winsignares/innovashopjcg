from config.db import db, ma, app

class User(db.Model):
    __tablename__ = "user"
    
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(255))
    contraseña = db.Column(db.String(255))
    rol = db.Column(db.String(255))

    def __init__(self, nombre, contraseña, rol):
        self.nombre = nombre
        self.contraseña = contraseña
        self.rol = rol

def create_default_data():
    if not User.query.first():
        users = [
            User(nombre='Jesus Garcia', contraseña='jgarcia123', rol='Empresa'),
            User(nombre='Juan Verdugo', contraseña='jberdugo123', rol='Vendedor'),
            User(nombre='David', contraseña='dcampo123', rol='Admin')
        ]
        db.session.add_all(users)
        db.session.commit()

with app.app_context():
    db.create_all()
    create_default_data()

class UserSchema(ma.Schema):
    class Meta:
        fields = ('id', 'nombre', 'contraseña', 'rol')

user_schema = UserSchema()
users_schema = UserSchema(many=True)
