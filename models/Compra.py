from config.db import db, ma, app
from datetime import datetime

class Compra(db.Model):
    __tablename__ = "compras"
    id = db.Column(db.Integer, primary_key=True)
<<<<<<< HEAD
    empresa_id = db.Column(db.Integer, nullable=False)
    proveedor_id = db.Column(db.Integer, nullable=False)
    fecha = db.Column(db.DateTime, default=datetime.utcnow)
=======
    cliente_id = db.Column(db.Integer, db.ForeignKey('cliente.id'))
    vendedor_id = db.Column(db.Integer, db.ForeignKey('vendedor.id'))
    producto_id = db.Column(db.Integer, db.ForeignKey('productos.id'))
    codigo = db.Column(db.String(255))
    nombre = db.Column(db.String(255))
    cotizacion = db.Column(db.Integer)
    stock = db.Column(db.Integer)
>>>>>>> 60ef691bcfa307388cf9b2e8ec8558a96a6a6dfd

    def __init__(self, empresa_id, proveedor_id, fecha=None):
        self.empresa_id = empresa_id
        self.proveedor_id = proveedor_id
        if fecha:
            self.fecha = fecha
        else:
            self.fecha = datetime.utcnow()

with app.app_context():
    db.create_all()

class CompraSchema(ma.Schema):
    class Meta:
        fields = ('id', 'empresa_id', 'proveedor_id', 'fecha')
