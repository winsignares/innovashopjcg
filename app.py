<<<<<<< HEAD
# main.py or app.py (your main application file)
from flask import Flask, render_template, request, jsonify, redirect, session, make_response
from config.db import app, db  # Assuming this sets up your Flask app
=======
from flask import Flask, request, jsonify, render_template, session, redirect
import flask_sqlalchemy
import json
import jwt
from config.db import db, ma, app
from datetime import datetime, timedelta, timezone
from functools import wraps
from models.User import Administrador, AdminSchema
from models.Vendedor import Vendedor, VendedorSchema
from models.Empresa import Empresa, EmpresaSchema
from models.Cliente import Cliente, ClientesSchema
from flask_sqlalchemy import SQLAlchemy
>>>>>>> 60ef691bcfa307388cf9b2e8ec8558a96a6a6dfd

from controllers.Auth import ruta_auth
from controllers.Administrador import ruta_admin
from controllers.Usuarios import ruta_user
from controllers.Indexes import ruta_index  
from controllers.Empresa import ruta_empresa
from controllers.Cliente import ruta_cliente
from controllers.Proveedor import ruta_proveedor
from controllers.Producto import ruta_productos
from controllers.Vendedores import ruta_vendedor

# Register blueprints
app.register_blueprint(ruta_auth, url_prefix="/auth")
app.register_blueprint(ruta_admin, url_prefix="/admin")
app.register_blueprint(ruta_user, url_prefix="/user")
app.register_blueprint(ruta_empresa, url_prefix="/empresa")
app.register_blueprint(ruta_cliente, url_prefix="/cliente")
app.register_blueprint(ruta_proveedor, url_prefix="/proveedor")  # Ensure this line is correct
app.register_blueprint(ruta_productos, url_prefix="/producto")
app.register_blueprint(ruta_vendedor, url_prefix="/vendedor")

<<<<<<< HEAD
app.register_blueprint(ruta_index, url_prefix="/")
=======
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root@localhost:3307/inn'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

admin_shchema = AdminSchema()
admins_shchema = AdminSchema(many=True)

vendedor_schema = VendedorSchema()
vendedores_schema = VendedorSchema(many=True)

empresa_schema = EmpresaSchema()

cliente_schema = ClientesSchema()

from controllers.empresa import empresa_schema, ruta_empresa
from controllers.productos import productos_bp
from controllers.vendedor import ruta_vendedor, vendedor_schema
from controllers.proveedores import ruta_proveedores
from controllers.cliente import ruta_clientes
from controllers.users import ruta_user

app.register_blueprint(ruta_user, url_prefix="/controller")
app.register_blueprint(productos_bp, url_prefix="/controller")
app.register_blueprint(ruta_empresa, url_prefix="/controller")
app.register_blueprint(ruta_proveedores, url_prefix="/controller")
app.register_blueprint(ruta_vendedor, url_prefix="/controller")
app.register_blueprint(ruta_clientes, url_prefix="/controller")
>>>>>>> 60ef691bcfa307388cf9b2e8ec8558a96a6a6dfd

@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

<<<<<<< HEAD
@app.errorhandler(403)
def unauthorized_error(e):
    return render_template('403.html'), 403

if __name__ == '__main__':
=======
@app.route('/ingresar', methods=['POST'])
def ingresar():
    user = request.form['user'].replace(' ', '')
    pswd = request.form['pswd']

    admin = db.session.query(Administrador).filter(Administrador.user == user, Administrador.pswd == pswd).first()
    vendedor = db.session.query(Vendedor).filter(Vendedor.user == user, Vendedor.pswd == pswd).first()
    empresa = db.session.query(Empresa).filter(Empresa.user == user, Empresa.pswd == pswd).first()
    cliente = db.session.query(Cliente).filter(Cliente.user == user, Cliente.pswd == pswd).first()

    if admin:
        session['usuario'] = admin_shchema.dump(admin)
        return redirect('/admins')
    elif vendedor:
        session['usuario'] = vendedor_schema.dump(vendedor)
        return redirect('/home_vendedor')
    elif empresa:
        session['usuario'] = empresa_schema.dump(empresa)
        session['company_id'] = empresa.companyid
        return redirect('/home_empresas')
    elif cliente:
        session['usuario'] = cliente_schema.dump(cliente)
        return redirect('/home_clientes')
    else:
        return redirect('/')


if __name__ == "__main__":
>>>>>>> 60ef691bcfa307388cf9b2e8ec8558a96a6a6dfd
    app.run(debug=True)
