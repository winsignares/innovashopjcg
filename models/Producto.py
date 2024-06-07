from config.db import db, ma, app

class Productos(db.Model):
    __tablename__ = "Producto"
    
    id = db.Column(db.Integer, primary_key=True)
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

with app.app_context():
    db.create_all()

class ProductoSchema(ma.Schema):
    class Meta:
        fields = ('id', 'nombre', 'p_uni', 'unidades', 'p_venta',  'u_admin', 'alternos', 'u_admin', 'iva')
