from config.db import db, ma, app
from datetime import datetime

class Producto(db.Model):
    __tablename__ = "productos"
    id = db.Column(db.Integer, primary_key=True)
<<<<<<< HEAD
    nombre = db.Column(db.String(255))
    descripcion = db.Column(db.Text)
    precio = db.Column(db.Float)  # Cost price
    precio_venta = db.Column(db.Float)  # Selling price
    existencias = db.Column(db.Integer)
    min_existencias = db.Column(db.Integer)
    img_src = db.Column(db.String(255))

    def __init__(self, nombre, descripcion, precio, precio_venta, existencias, min_existencias, img_src):
        self.nombre = nombre
        self.descripcion = descripcion
        self.precio = precio
        self.precio_venta = precio_venta
        self.existencias = existencias
        self.min_existencias = min_existencias
        self.img_src = img_src
=======
    nombre = db.Column(db.String(255), unique=True)
    p_uni = db.Column(db.Float())
    p_venta = db.Column(db.Float())
    unidades = db.Column(db.Integer)
    u_admin = db.Column(db.Integer)
    alternos = db.Column(db.String(255))
    iva = db.Column(db.Float())

    def __init__(self, id, nombre, p_uni, unidades, p_venta, u_admin, alternos, iva, src=None):
        self.id = id
        self.nombre = nombre  
        self.p_uni = p_uni  
        self.alternos = alternos  
        self.p_venta = p_venta  
        self.unidades = unidades 
        self.u_admin = u_admin  
        self.iva = iva
        # self.src = src
>>>>>>> 60ef691bcfa307388cf9b2e8ec8558a96a6a6dfd

with app.app_context():
    db.create_all()

class ProductoSchema(ma.Schema):
    class Meta:
        fields = ('id', 'nombre', 'descripcion', 'precio', 'precio_venta', 'existencias', 'min_existencias', 'img_src')
