from flask import Blueprint, Flask, render_template,json, jsonify, redirect, session, request
from config.db import app, db, ma
from models.UserModel import User, UsersSchema
from models.VendedoresModel import Vendedor, VendedorSchema
from models.EmpresaModel import EMP, EMPSchema
from models.ClienteModel import Cliente, ClientesSchema

ruta_user = Blueprint("route_user", __name__)

user_schema = UsersSchema()
users_schema = UsersSchema(many=True)

@app.route('/ingresar', methods=['POST'])
def ingresar():
    user = request.form['user'].replace(' ', '')
    password = request.form['password']
    user1 = db.session.query(User).filter(User.user == user, User.password == password).all()
    vendedor = db.session.query(Vendedor).filter(Vendedor.user == user, Vendedor.password == password).all()
    empresa = db.session.query(EMP).filter(EMP.user == user, EMP.password == password).all()
    cliente = db.session.query(Cliente).filter(Cliente.user == user, Cliente.password == password).all()
     
    if user1:
        resultado1 = user_schema.dump(user1)
        session['usuario'] = resultado1
    
        response = redirect('/Portal_Empresa')
        response.set_cookie('isAuthenticated', 'true')
        return response
    elif vendedor:
        resultado2 = user_schema.dump(vendedor)
        session['usuario'] = resultado2
    
        return redirect('/Portal_Vendedor')
    elif empresa:
        resultado3 = user_schema.dump(empresa)
        session['usuario'] = resultado3
    
        return redirect('/Portal_Empresa')
    elif cliente:
        resultado3 = user_schema.dump(cliente)
        session['usuario'] = resultado3
    
        return redirect('/Portal_Cliente')
    else:
        return redirect('/')
