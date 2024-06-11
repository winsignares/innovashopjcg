from config.db import db, ma, app

class Proveedor(db.Model):
    __tablename__ = "proveedores"
    id = db.Column(db.Integer, primary_key=True)
<<<<<<< HEAD
    nombre = db.Column(db.String(255), unique=True)
    contacto = db.Column(db.String(255))
    telefono = db.Column(db.String(255))
    direccion = db.Column(db.String(255))

    def __init__(self, nombre, contacto, telefono, direccion):
        self.nombre = nombre
        self.contacto = contacto
        self.telefono = telefono
        self.direccion = direccion

=======
    nombre= db.Column(db.String(50), unique=True)
    email = db.Column(db.String(50))
    p_number = db.Column(db.Integer)
    dire = db.Column(db.String(50))
    
    def __init__(self,id, nombre, email, dire, p_number):
      self.id = id
      self.nombre = nombre
      self.email = email
      self.p_number = p_number
      self.dire = dire
      
>>>>>>> 60ef691bcfa307388cf9b2e8ec8558a96a6a6dfd
with app.app_context():
    db.create_all()

class ProveedorSchema(ma.Schema):
    class Meta:
        fields = ('id', 'nombre', 'contacto', 'telefono', 'direccion')
