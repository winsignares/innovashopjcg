from config.db import db, ma, app

class Productos(db.Model):
    __tablename__ = "productos"
    id = db.Column(db.Integer, primary_key=True)
    codigo = db.Column(db.String(255))
    imagen = db.Column(db.String(255))
    stock = db.Column(db.Integer)
    producto = db.Column(db.String(255))
    descuento_tiempo = db.Column(db.String(255))
    precio = db.Column(db.Float)

    def __init__(self, codigo, imagen, stock, producto, informes, descuento_tiempo, precio):
        self.nombre = codigo
        self.imagen = imagen
        self.stock = stock
        self.producto = producto
        self.informes = informes
        self.descuento_tiempo = descuento_tiempo
        self.precio = precio

with app.app_context():
    db.create_all()

class ProductoSchema(ma.Schema):
    class Meta:
        fields = ('id', 'codigo', 'imagen', 'stock', 'producto', 'informes', 'descuento_tiempo', 'precio')

producto_schema = ProductoSchema()
productos_schema = ProductoSchema(many=True)