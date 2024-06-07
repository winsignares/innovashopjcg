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

SECRET_KEY = "newtoken"

app = Flask(__name__, 
            static_folder='config/static',
            template_folder='config/templates')

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

@app.route('/', methods=['GET'])
def index():
    return render_template('login.html')


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
    app.run(debug=True)
    
    
