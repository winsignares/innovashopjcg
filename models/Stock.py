from config.db import db, ma, app

class Stocks(db.Model):
    __tablename__ = "stock"
    id = db.Column(db.Integer, primary_key=True)
    identificacion = db.Column(db.String(255))
    nombre = db.Column(db.String(255))
    cotizacion = db.Column(db.Integer)
    stock = db.Column(db.Integer)
    pdf = db.Column(db.String(255))

    def __init__(self, identificacion, nombre, cotizacion, stock, pdf):
        self.nombre = nombre
        self.identificacion = identificacion
        self.cotizacion = cotizacion
        self.stock = stock
        self.pdf = pdf

with app.app_context():
    db.create_all()

class Stockchema(ma.Schema):
    class Meta:
        fields = ('id', 'identificacion', 'nombre', 'cotizacion', 'stock', 'pdf')

stock_schema = Stockchema()
stocks_schema = Stockchema(many=True)
