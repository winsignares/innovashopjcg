from config.db import app, db, ma 

class Proveedor(db.Model):
    __tablename__ = 'proveedor'
    
    id = db.Column(db.Integer, primary_key=True)
    nombre= db.Column(db.String(50), unique=True)
    email = db.Column(db.String(50))
    p_number = db.Column(db.Integer)
    dire = db.Column(db.String(50))
    id_empresa = db.Column(db.Integer, db.ForeignKey('empresa.id'))
    empresa = db.relationship('empresa', backref=db.backref('proveedores', lazy=True))
    
    def __init__(self,id, nombre, email, dire, p_number, id_empresa):
      self.id = id
      self.nombre = nombre
      self.email = email
      self.p_number = p_number
      self.dire = dire
      self.id_empresa = id_empresa
      
with app.app_context():
    db.create_all()

class ProveedoresSchema(ma.Schema):
    class Meta:
        fields = ('id', 'nombre', 'email', 'dire', 'p_number')