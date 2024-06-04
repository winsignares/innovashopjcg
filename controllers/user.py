from flask import Flask, jsonify, request, redirect, session, make_response, Blueprint
from datetime import datetime, timedelta, timezone
import jwt
from models.User import User, UsersSchema
from models.Vendedor import Vendedor, VendedorSchema
from models.Empresa import Empresa, empresa_schema, empresas_schema
from models.Cliente import Cliente, ClientesSchema
from functools import wraps
from config.db import app, db

auth_bp = Blueprint("auth", __name__)

user_schema = UsersSchema()

SECRET_KEY = "newtoken"

def generate_expiration_date(days=0, hours=0, minutes=0, seconds=0):
    current_date = datetime.now(tz=timezone.utc)
    expiration_time = timedelta(days=days, hours=hours, minutes=minutes, seconds=seconds)
    return current_date + expiration_time

def generate_token(user_id):
    expiration_date = generate_expiration_date(seconds=200)
    payload = {
        "exp": expiration_date,
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

@auth_bp.route('/login', methods=['POST'])
def login():
    username = request.form['user'].replace(' ', '')
    pswd = request.form['pswd']

    adminu = db.session.query(User).filter(User.user == adminu, User.pswd == pswd, User.is_admin == True).all()
    vendor = db.session.query(Vendedor).filter(Vendedor.user == username, Vendedor.password == pswd).first()
    company = db.session.query(Empresa).filter(Empresa.user == username, Empresa.password == pswd).first()
    client = db.session.query(Cliente).filter(Cliente.user == username, Cliente.password == pswd).first()

    if adminu:
        token = generate_token(adminu.id)
        session['user'] = user_schema.dump(adminu)
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
        return redirect('/')

@auth_bp.route('/protected_route')
@token_required
def protected_route():
    return jsonify({'message': 'This is protected content'})
