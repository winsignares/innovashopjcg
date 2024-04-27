from config.db import db, ma, app

class Informes(db.Model):
    __tablename__ = "informes"
    id = db.Column(db.Integer, primary_key=True)
    identificacion = db.Column(db.String(255))
    nombre = db.Column(db.String(255))
    factura = db.Column(db.Integer)
    estado = db.Column(db.String(255))
    pdf = db.Column(db.String(255))

    def __init__(self, identificacion, nombre, factura, pdf):
        self.identificacion = identificacion
        self.nombre = nombre
        self.factura = factura
        self.pdf = pdf
    

with app.app_context():
    db.create_all()

class InformeSchema(ma.Schema):
    class Meta:
        fields = ('id', 'identificacion', 'nombre', 'factura', 'pdf') 

informe_schema = InformeSchema()
informes_schema = InformeSchema(many=True)
