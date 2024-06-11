from config.db import db, ma, app

class ProveedorEmpresas(db.Model):
    __tablename__ = "proveedoresempresas"
    id = db.Column(db.Integer, primary_key=True)
    empresa_id = db.Column(db.Integer, db.ForeignKey('empresas.id'), nullable=False)
    proveedor_id = db.Column(db.Integer, db.ForeignKey('proveedores.id'), nullable=False)

    def __init__(self, empresa_id, proveedor_id):
        self.empresa_id = empresa_id
        self.proveedor_id = proveedor_id

with app.app_context():
    db.create_all()

class ProveedorEmpresasSchema(ma.Schema):
    class Meta:
        fields = ('id', 'empresa_id', 'proveedor_id')