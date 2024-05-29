from config.db import app, db, ma 

class Empresa(db.Model):
    __tablename__ = 'empresa'
    
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(50))
    estado = db.Column(db.String(50), nullable=False, default="activo")
    fecha_i = db.Column(db.Date) 
    f_plazo = db.Column(db.Date)
    user = db.Column(db.String(50), unique=True)
    pswd = db.Column(db.String(50))
    admin_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    admin = db.relationship('user', backref=db.backref('empresas', lazy=True))
    vendedores = db.relationship('vendedor', backref=db.backref('empresa', lazy=True))
    
    def __init__(self, id, nombre, email, estado, fecha_i, f_plazo, user, pswd, admin_id):
        self.id = id
        self.nombre = nombre
        self.email = email
        self.estado = estado
        self.fecha_i = fecha_i
        self.f_plazo = f_plazo
        self.user = user
        self.pswd = pswd
        self.admin_id = admin_id
        
with app.app_context():
    db.create_all()

class EMPSchema(ma.Schema):
    class Meta:
        fields = ('companyid','nombre', 'email', 'estado', 'fecha_i', 'f_plazo','user','pswd')