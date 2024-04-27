from config.db import db, ma, app
from sqlalchemy.orm import relationship, backref

class Cliente(db.Model):
    __tablename__ = "clientes"
    id = db.Column(db.Integer, primary_key=True)
    identificacion = db.Column(db.String(255))
    nombre = db.Column(db.String(255))
    compras = db.relationship('Compra', backref='cliente')

    def __init__(self, identificacion, nombre, compras):
        self.identificacion = identificacion
        self.cotizaciones = nombre
        self.compras = compras

with app.app_context():
    db.create_all()

class ClienteSchema(ma.Schema):
    class Meta:
        fields = ('id', 'identificacion', 'nombre')

cliente_schema = ClienteSchema()
clientes_schema = ClienteSchema(many=True)
