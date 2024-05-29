from config.db import db, ma, app
from sqlalchemy.orm import relationship, backref

class Cliente(db.Model):
    __tablename__ = 'cliente'
    
    id = db.Column(db.Integer, primary_key=True)
    nombre= db.Column(db.String(255), unique=True)
    email = db.Column(db.String(255))
    p_number = db.Column(db.Integer)
    user = db.Column(db.String(50), unique=True)
    pswd = db.Column(db.String(50))
    dire = db.Column(db.String(255))
    id_vendedor = db.Column(db.Integer, db.ForeignKey('vendedor.id'))
    vendedor = db.relationship('vendedor', backref=db.backref('clientes', lazy=True))
    
    def __init__(self, id, nombre, email, dire, p_number, user, pswd, id_vendedor):
      self.id = id
      self.nombre = nombre
      self.email = email
      self.p_number = p_number
      self.user = user
      self.pswd = pswd
      self.dire = dire
      self.id_vendedor = id_vendedor

with app.app_context():
    db.create_all()

class ClientesSchema(ma.Schema):
    class Meta:
        fields = ('id', 'nombre', 'email', 'p_number', 'user','pswd''dire')