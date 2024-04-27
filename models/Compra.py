from config.db import db, ma, app
from sqlalchemy import ForeignKey
class Compra(db.Model):
    __tablename__ = "compras"
    id = db.Column(db.Integer, primary_key=True)
    cliente_id = db.Column(db.Integer, db.ForeignKey('cliente.id'))
    codigo = db.Column(db.String(255))
    nombre = db.Column(db.String(255))
    cotizacion = db.Column(db.Integer)
    stock = db.Column(db.Integer)
    detalles = db.Column(db.String(255))

    def __init__(self, codigo, nombre, clientes, cotizacion, stock, detalles):
        self.codigo = codigo
        self.nombre = nombre
        self.clientes = clientes
        self.cotizacion = cotizacion
        self.stock = stock
        self.detalles = detalles

with app.app_context():
    db.create_all()

class CompraSchema(ma.Schema):
    class Meta:
        fields = ('id', 'codigo', 'nombre', 'clientes', 'cotizacion', 'stock', 'detalles')

compra_schema = CompraSchema()
compras_schema = CompraSchema(many=True)
