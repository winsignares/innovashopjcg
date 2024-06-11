<<<<<<< HEAD
from config.db import db, ma, app
from datetime import datetime
=======
from config.db import app, db, ma 
from models.User import Administrador
from models.Vendedor import Vendedor
>>>>>>> 60ef691bcfa307388cf9b2e8ec8558a96a6a6dfd

class Empresa(db.Model):
    __tablename__ = "empresas"
    id = db.Column(db.Integer, primary_key=True)
<<<<<<< HEAD
    nombre = db.Column(db.String(255), unique=True)
    direccion = db.Column(db.String(255))
    telefono = db.Column(db.String(255))
    email = db.Column(db.String(255), unique=True)
    usuario = db.Column(db.String(255), unique=True)
    contraseña = db.Column(db.String(255))
    rol = db.Column(db.String(255), default='empresa')
    nit = db.Column(db.String(255), unique=True)
    session_limit = db.Column(db.Date)
    general_discount = db.Column(db.Float, default=0.0)
    tax = db.Column(db.Float, default=0.0)
    profit_percentage = db.Column(db.Float, default=0.0)
    ultima_sesion = db.Column(db.DateTime, default=datetime.utcnow)
    estado = db.Column(db.String(50), default='activo')
    # modulo_clientes = dbColumn(db.Boolean, default=True)
    # modulo_vendedores = dbColumn(db.Boolean, default=True)
    # modulo_porcentajes = dbColumn(db.Boolean, default=True)

    def __init__(self, nombre, direccion, telefono, email, usuario, contraseña, nit, session_limit, general_discount, tax, profit_percentage):
=======
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
>>>>>>> 60ef691bcfa307388cf9b2e8ec8558a96a6a6dfd
        self.nombre = nombre
        self.direccion = direccion
        self.telefono = telefono
        self.email = email
<<<<<<< HEAD
        self.usuario = usuario
        self.contraseña = contraseña
        self.nit = nit
        self.session_limit = session_limit
        self.general_discount = general_discount
        self.tax = tax
        self.profit_percentage = profit_percentage

=======
        self.estado = estado
        self.fecha_i = fecha_i
        self.f_plazo = f_plazo
        
>>>>>>> 60ef691bcfa307388cf9b2e8ec8558a96a6a6dfd
with app.app_context():
    db.create_all()

class EmpresaSchema(ma.Schema):
    class Meta:
        fields = ('id', 'nombre', 'direccion', 'telefono', 'email', 'usuario', 'contraseña', 'rol', 'nit', 'session_limit', 'general_discount', 'tax', 'profit_percentage', 'ultima_sesion', 'estado')
