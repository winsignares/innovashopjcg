from config.db import db, ma, app

class Empresa(db.Model):
    __tablename__ = "empresas" 
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(255))
    cotizaciones = db.Column(db.Boolean)
    clientes = db.Column(db.Boolean)
    compras = db.Column(db.Boolean)
    informes = db.Column(db.Boolean)
    parametros = db.Column(db.Boolean)
    productos = db.Column(db.Boolean)
    stock = db.Column(db.Boolean)
    vendedores = db.Column(db.Boolean)
    empresas = db.Column(db.Boolean)
    estado = db.Column(db.String(50))

    def __init__(self, nombre, cotizaciones, clientes, compras, informes, parametros, productos, stock, vendedores, empresas, estado):
        self.nombre = nombre
        self.cotizaciones = cotizaciones
        self.clientes = clientes
        self.compras = compras
        self.informes = informes
        self.parametros = parametros
        self.productos = productos
        self.stock = stock
        self.vendedores = vendedores
        self.empresas = empresas
        self.estado = estado

with app.app_context():
    db.create_all()

class EmpresaSchema(ma.Schema):
    class Meta:
        fields = ('id', 'nombre', 'cotizaciones', 'clientes', 'compras', 'informes', 'parametros', 'productos', 'stock', 'vendedores', 'empresas', 'estado')

empresa_schema = EmpresaSchema()
empresas_schema = EmpresaSchema(many=True)