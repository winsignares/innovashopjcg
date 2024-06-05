from flask import Flask, request, jsonify, render_template, session, redirect
import json
import jwt
from config.db import db, ma, app
from datetime import datetime, timedelta, timezone
from functools import wraps
from models.Admin import Admin, AdminSchema
from models.Vendedor import Vendedor, VendedorSchema
from models.Empresa import Empresa, EmpresaSchema
from models.Cliente import Cliente, ClientesSchema

SECRET_KEY = "newtoken"

app = Flask(__name__, 
            static_folder='config/static',
            template_folder='config/templates')

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


def generar_fecha_vencimiento(dias=0, horas=0, minutos=0, segundos=0):
    fecha_actual = datetime.now(tz=timezone.utc)
    tiempo_vencimiento = timedelta(days=dias, hours=horas, minutes=minutos, seconds=segundos)
    return fecha_actual + tiempo_vencimiento

def generate_token(user_id):
    fecha_vencimiento = generar_fecha_vencimiento(segundos=200)
    payload = {
        "exp": fecha_vencimiento,
        "user_id": user_id,
    }
    token = jwt.encode(payload, SECRET_KEY, algorithm="HS256")
    return token

def verify_token(token):
    try:
        jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
        return {"error": False, "message": "Valid token"}
    except jwt.ExpiredSignatureError:
        return {"error": True, "message": "Expired token"}
    except jwt.InvalidTokenError:
        return {"error": True, "message": "Invalid token"}

def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = request.cookies.get('token')
        if not token:
            return jsonify({'message': 'Token is required!'}), 403
        try:
            jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
        except jwt.ExpiredSignatureError:
            return jsonify({'message': 'Token has expired!'}), 403
        except jwt.InvalidTokenError:
            return jsonify({'message': 'Invalid token!'}), 403
        return f(*args, **kwargs)
    return decorated

@app.route('/protected_route')
@token_required
def protected_route():
    return jsonify({'message': 'This is protected content'})


@app.route('/ingresar', methods=['POST'])
def ingresar():
    user = request.form['user'].replace(' ', '')
    pswd = request.form['pswd']
    
    admin = db.session.query(Admin).filter(Admin.user == user, Admin.pswd == pswd).first()
    vendedor = db.session.query(Vendedor).filter(Vendedor.user == user, Vendedor.pswd == pswd).first()
    empresa = db.session.query(Empresa).filter(Empresa.user == user, Empresa.pswd == pswd).first()
    cliente = db.session.query(Cliente).filter(Cliente.user == user, Cliente.pswd == pswd).first()

    if admin:
        token = generate_token(admin.id)
        session['usuario'] = admin_shchema.dump(admin)
        response = redirect('/admins')
        response.set_cookie('token', token)
        return response
    elif vendedor:
        token = generate_token(vendedor.id)
        session['usuario'] = vendedor_schema.dump(vendedor)
        response = redirect('/home_vendedor')
        response.set_cookie('token', token)
        return response
    elif empresa:
        token = generate_token(empresa.companyid)
        session['usuario'] = empresa_schema.dump(empresa)
        session['company_id'] = empresa.companyid
        response = redirect('/home_empresas')
        response.set_cookie('token', token)
        return response
    elif cliente:
        token = generate_token(cliente.id)
        session['usuario'] = cliente.dump(cliente)
        response = redirect('/home_clientes')
        response.set_cookie('token', token)
        return response
    else:
        return redirect('/')


if __name__ == "__main__":
    app.run(debug=True)
    
    
