from config.db import db, ma, app

class Vendedor(db.Model):
    __tablename__ = 'vendedor'
    
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(50))
    email = db.Column(db.String(50))
    fecha_inicio = db.Column(db.Date)
    user = db.Column(db.String(50), unique=True)
    pswd = db.Column(db.String(50))
    company_id = db.Column(db.Integer, db.ForeignKey('empresa.id'))
    
    def __init__(self, id, nombre, email, fecha_inicio, user, pswd, company_id):
      self.id = id
      self.nombre = nombre
      self.email = email
      self.fecha_inicio = fecha_inicio
      self.user = user
      self.pswd = pswd
      self.company_id = company_id
    
with app.app_context():
    db.create_all()
class VendedorSchema(ma.Schema):
    class Meta:
        fields = ('id', 'nombre', 'email', 'fecha_inicio', 'user','pswd')