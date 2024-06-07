from config.db import app, db, ma 
from models.User import Administrador
from models.Vendedor import Vendedor

class Empresa(db.Model):
    __tablename__ = 'empresa'
    
    id = db.Column(db.Integer, primary_key=True)
    user = db.Column(db.String(50), unique=True)
    pswd = db.Column(db.String(50))
    nombre = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(50))
    estado = db.Column(db.String(50), nullable=False, default="activo")
    fecha_i = db.Column(db.Date) 
    f_plazo = db.Column(db.Date)
    
    def __init__(self, id, nombre, email, estado, fecha_i, f_plazo, user, pswd):
        self.id = id
        self.user = user
        self.pswd = pswd
        self.nombre = nombre
        self.email = email
        self.estado = estado
        self.fecha_i = fecha_i
        self.f_plazo = f_plazo
        
with app.app_context():
    db.create_all()

class EmpresaSchema(ma.Schema):
    class Meta:
        fields = ('id', 'user', 'pswd', 'nombre', 'email', 'estado', 'fecha_i', 'f_plazo')