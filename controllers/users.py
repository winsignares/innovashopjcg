import controllers.users
from flask import Flask, jsonify, request, redirect, session, make_response, Blueprint, render_template
from datetime import datetime, timedelta, timezone
import jwt
from models.Admin import Admin, AdminSchema
from models.Vendedor import Vendedor, VendedorSchema
from models.Empresa import Empresa, EmpresaSchema
from models.Cliente import Cliente, ClientesSchema
from functools import wraps
from config.db import app, db, ma

ruta_user = Blueprint("route_user", __name__)

user_schema = AdminSchema()
users_schema = AdminSchema(many=True)

SECRET_KEY = "newtoken"

def generar_token_admin(user_id):
    fecha_vencimiento = datetime.now(tz=timezone.utc) + timedelta(seconds=150)
    payload = {
        "exp": fecha_vencimiento,
        "user_id": user_id,
    }
    token = jwt.encode(payload, SECRET_KEY, algorithm="HS256")
    return token

@app.route('/ingresaradmin', methods=['POST'])
def ingresaradmin():
    userad = request.form['userad'].replace(' ', '')
    passwordad = request.form['passwordad']
    user = db.session.query(Admin).filter(Admin.userad == userad, Admin.passwordad == passwordad).first()
    
    if user:
        token = generar_token_admin(user.id)
        session['usuarioad'] = user_schema.dump(user)
        response = redirect('/portaladmin')
        response.set_cookie('token', token)
        return response
    else:
        return redirect('/loginad')

@app.route('/admins', methods=['GET'])
def admins():
    return render_template('admin.html')

@app.route('/reg_empresa')
def crearempresa():
    empresas = Empresa.query.all()
    if 'adminu' in session:
        return render_template('admin-add-empresas.html', usuario = session['adminu'])

@app.route('/view_modules')
def modulosempresa():
    empresas = Empresa.query.all()
    if 'adminu' in session:
        return render_template('admin-modulos.html')

@app.route('/set_impuestos')
def set_impuestos():
    empresas = Empresa.query.all()
    if 'adminu' in session:
        return render_template('admin-impuestos.html')
    
@app.route('/login_v')
def login_view():
    return render_template('login.html')

@app.route('/search_by')
def search():
    query = request.args.get('query', '')

    if query:
        empresas = Empresa.query.filter(
            (Empresa.id.like(f'%{query}%')) |
            (Empresa.nombre.like(f'%{query}%'))
        ).all()
    else:
        empresas = Empresa.query.all()

    if 'adminu' in session:
        return render_template('admin-empresas.html', usuario=session['adminu'], empresas=empresas)


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

@app.route('/ingresar', methods=[ 'POST'])
def ingresar():
    username = request.form.get('user').replace(' ', '')
    pswd = request.form.get('pswd')

    if not username or not pswd:
        return jsonify({'message': 'Invalid request'}), 400

    users = [
        {'model': Admin, 'redirect': '/admins'},
        {'model': Vendedor, 'redirect': '/portal_vendor'},
        {'model': Empresa, 'redirect': '/portal_company'},
        {'model': Cliente, 'redirect': '/portal_client'}
    ]

    for user_config in users:
        user = db.session.query(user_config['model']).filter_by(user=username, password=pswd).first()
        if user:
            token = generate_token(user.id)
            session['user'] = user_schema.dump(user)
            if user_config['model'] == Empresa:
                session['company_id'] = user.companyid
            response = redirect(user_config['redirect'])
            response.set_cookie('token', token)
            return response

    return jsonify({'message': 'Invalid credentials'}), 401

@app.route('/protected_route')
@token_required
def protected_route():
    return jsonify({'message': 'This is protected content'})
