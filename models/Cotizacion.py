from config.db import db, ma, app
from sqlalchemy import ForeignKey

class Cotizacion(db.Model):
    __tablename__ = "cotizaciones"
    id = db.Column(db.Integer, primary_key=True)
    cliente_id = db.Column(db.Integer, db.ForeignKey('cliente.id'))
    vendedor_id = db.Column(db.Integer, db.ForeignKey('vendedor.id'))
    producto_id = db.Column(db.Integer, db.ForeignKey('productos.id'))
    codigo = db.Column(db.String(255))
    nombre = db.Column(db.String(255))
    stock = db.Column(db.Integer)
    detalles = db.Column(db.String(255))
    cliente = db.relationship('Cliente', backref=db.backref('cotizaciones', lazy=True))
    vendedor = db.relationship('Vendedor', backref=db.backref('cotizaciones', lazy=True))
    producto = db.relationship('Productos', backref=db.backref('cotizaciones', lazy=True))

    def __init__(self, codigo, nombre, cliente, stock, detalles):
        self.codigo = codigo
        self.nombre = nombre
        self.cliente = cliente
        self.stock = stock
        self.detalles = detalles

with app.app_context():
    db.create_all()

class CotizacionSchema(ma.Schema):
    class Meta:
        fields = ('id', 'codigo', 'nombre', 'cliente', 'stock', 'detalles')

cotizacion_schema = CotizacionSchema()
cotizaciones_schema = CotizacionSchema(many=True)
