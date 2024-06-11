<<<<<<< HEAD
from flask import Blueprint, Flask, render_template, redirect, request, json, jsonify, session
from datetime import datetime, timedelta, timezone
import jwt
from config.db import db
from models.Usuario import Usuario, UsuarioSchema
from models.ClientesEmpresas import ClientesEmpresas
from .Auth import token_required
from .hashing_helper import verify_password, hash_password
=======
from flask import Blueprint, jsonify, render_template, request, redirect, session
from config.db import app, db, ma
from models.Cliente import Cliente
>>>>>>> 60ef691bcfa307388cf9b2e8ec8558a96a6a6dfd

ruta_cliente = Blueprint('ruta_cliente', __name__)

@ruta_cliente.route('/home', methods=['GET'])
def login_route():
    return render_template('cliente.html')

@ruta_cliente.route('/add-clientes', methods=['GET', 'POST'])
@token_required
def add_clientes():
    if request.method == 'GET':
        return render_template('empresas-templates/clientes-empresas.html')
    
    if request.method == 'POST':
        data = request.json
        nombre = data.get('nombre')
        apellidos = data.get('apellidos')
        nit = data.get('nit')
        direccion = data.get('direccion')
        telefono = data.get('telefono')
        email = data.get('email')
        contraseña = hash_password(data.get('nit'))

        # Check if a user with the same email or cedula already exists
        existing_user = Usuario.query.filter(
            (Usuario.email == email) | 
            (Usuario.cedula == nit)
        ).first()
        
        if existing_user:
            return jsonify({"error": "Ya existe un usuario con este correo electrónico o NIT."}), 409

        # Create new client user
        nuevo_cliente = Usuario(
            nombre=nombre,
<<<<<<< HEAD
            apellidos=apellidos,
            usuario=email,
            contraseña=contraseña,
            rol='cliente',
            cedula=nit,
            direccion=direccion,
            telefono=telefono,
            email=email
=======
            p_number=p_number,
            email=email,
            user = user,
            pswd = pswd,
            dire=dire
>>>>>>> 60ef691bcfa307388cf9b2e8ec8558a96a6a6dfd
        )
        
        db.session.add(nuevo_cliente)
        db.session.commit()

        # Relate new client with the current company
        empresa_id = session.get('user_id')
        nuevo_cliente_empresa = ClientesEmpresas(
            usuario_id=nuevo_cliente.id,
            empresa_id=empresa_id
        )

        db.session.add(nuevo_cliente_empresa)
        db.session.commit()

        return jsonify({"success": True})

<<<<<<< HEAD
=======
@app.route('/home_clientes')
def portalcliente():
    if 'usuario' in session:
        return render_template("cliente.html")
    else:
        return redirect('/')
>>>>>>> 60ef691bcfa307388cf9b2e8ec8558a96a6a6dfd
