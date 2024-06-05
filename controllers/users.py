import controllers.user
from flask import Flask, jsonify, request, redirect, session, make_response, Blueprint, render_template
from datetime import datetime, timedelta, timezone
import jwt
from models.Admin import Admin, AdminSchema
from models.Vendedor import Vendedor, VendedorSchema
from models.Empresa import Empresa, EmpresaSchema
from models.Cliente import Cliente, ClientesSchema
from functools import wraps
from config.db import app, db, ma
from controllers.admin import ruta_administrador

ruta_user = Blueprint("auth", __name__)

user_schema = AdminSchema()
users_schema = AdminSchema(many=True)

SECRET_KEY = "newtoken"

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

@app.route('/login', methods=[ 'POST', 'GET'])
def login():
    if request.method == 'POST':
        username = request.form['user'].replace(' ', '')
        pswd = request.form['pswd']

        adminu = db.session.query(AdminSchema).filter(AdminSchema.user == username, AdminSchema.pswd == pswd).all()
        vendor = db.session.query(Vendedor).filter(Vendedor.user == username, Vendedor.password == pswd).first()
        company = db.session.query(Empresa).filter(Empresa.user == username, Empresa.password == pswd).first()
        client = db.session.query(Cliente).filter(Cliente.user == username, Cliente.password == pswd).first()

        if adminu:
            token = generate_token(adminu.id)
            session['adminu'] = user_schema.dump(adminu)
            response = redirect('/admins')
            response.set_cookie('token', token)
            return response
        elif vendor:
            token = generate_token(vendor.id)
            session['user'] = user_schema.dump(vendor)
            response = redirect('/portal_vendor')
            response.set_cookie('token', token)
            return response
        elif company:
            token = generate_token(company.companyid)
            session['user'] = user_schema.dump(company)
            session['company_id'] = company.companyid
            response = redirect('/portal_company')
            response.set_cookie('token', token)
            return response
        elif client:
            token = generate_token(client.id)
            session['user'] = user_schema.dump(client)
            response = redirect('/portal_client')
            response.set_cookie('token', token)
            return response
        else:
            redirect('/login_view')
    return render_template('login.html')

@app.route('/protected_route')
@token_required
def protected_route():
    return jsonify({'message': 'This is protected content'})
