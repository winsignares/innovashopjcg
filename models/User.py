from config.db import db, ma, app

class Administrador(db.Model):
    __tablename__ = "administrador"

    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(255))
    pswd = db.Column(db.String(255))
    user = db.Column(db.String(255))

    def __init__(self, nombre, pswd, user, is_admin):
        self.nombre = nombre
        self.pswd = pswd
        self.user = user
        self.is_admin = is_admin

def create_default_data():
    if not Administrador.query.first():
        admins = [
            Administrador(nombre='Jesus Garcia', pswd='jgarcia123', user='jesusgarcia123', is_admin=True),
            Administrador(nombre='Juan Verdugo', pswd='jberdugo123', user='juanberdugo123', is_admin=True),
            Administrador(nombre='David Campo', pswd='dcampo123', user='davidcampo123', is_admin=True)
        ]
        db.session.add_all(admins)
        db.session.commit()

with app.app_context():
    db.create_all()
    create_default_data()

class AdminSchema(ma.Schema):
    class Meta:
        fields = ('id', 'nombre', 'pswd', 'user', 'rol')

admin_shchema = AdminSchema()
admins_shchema = AdminSchema(many=True)
