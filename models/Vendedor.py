from config.db import db, ma, app

class Vendedor(db.Model):
    __tablename__ = "vendedores"
    id = db.Column(db.Integer, primary_key=True)
    identificacion = db.Column(db.String(255))
    nombre = db.Column(db.String(255))
    telefono = db.Column(db.String(255))
    ventas = db.Column(db.Integer)

    def __init__(self, identificacion, nombre, telefono, ventas):
        self.identificacion = identificacion
        self.nombre = nombre
        self.telefono = telefono
        self.ventas = ventas

with app.app_context():
    db.create_all()

class VendedorSchema(ma.Schema):
    class Meta:
        fields = ('id', 'identificacion', 'nombre', 'telefono', 'ventas')

vendedor_schema = VendedorSchema()
vendedores_schema = VendedorSchema
