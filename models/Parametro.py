from config.db import db, ma, app

class Parametros(db.Model):
    __tablename__ = "parametros"
    id = db.Column(db.Integer, primary_key=True)
    codigo = db.Column(db.String(255))
    producto = db.Column(db.String(255))
    precio = db.Column(db.Float)
    ganancia = db.Column(db.Float)
    iva = db.Column(db.Float)
    precio_final = db.Column(db.Float)

    def __init__(self, id, codigo, producto, precio, ganancia, iva, precio_final):
        self.id = id
        self.codigo = codigo
        self.producto = producto
        self.precio = precio
        self.ganancia = ganancia
        self.iva = iva
        self.precio_final = precio_final

with app.app_context():
    db.create_all()

class ParametroSchema(ma.Schema):
    class Meta:
        fields = ('id', 'codigo', 'producto', 'precio', 'ganancia', 'iva', 'precio_final')

parametro_schema = ParametroSchema()
parametro_schema = ParametroSchema(many=True)
