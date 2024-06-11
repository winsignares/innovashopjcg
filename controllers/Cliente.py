from flask import Blueprint, Flask, render_template, redirect, request, json, jsonify, session
from datetime import datetime, timedelta, timezone
import jwt
from config.db import db
from models.Usuario import Usuario, UsuarioSchema
from models.ClientesEmpresas import ClientesEmpresas
from models.VendedoresEmpresas import VendedoresEmpresas
from controllers.Auth import token_required
from .Auth import token_required
from .hashing_helper import verify_password, hash_password

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
            apellidos=apellidos,
            usuario=email,
            contraseña=contraseña,
            rol='cliente',
            cedula=nit,
            direccion=direccion,
            telefono=telefono,
            email=email
        )
        
        db.session.add(nuevo_cliente)
        db.session.commit()

        # Relate new client with the current company
        empresa_id = session.get('empresa_id')
        nuevo_cliente_empresa = ClientesEmpresas(
            usuario_id=nuevo_cliente.id,
            empresa_id=empresa_id
        )

        db.session.add(nuevo_cliente_empresa)
        db.session.commit()

        return jsonify({"success": True})

@ruta_cliente.route('/clientes', methods=['GET'])
@token_required
def list_clientes():
    vendedor_id = session.get('user_id')
    if not vendedor_id:
        return jsonify({"error": "Not logged in"}), 401

    vendedor_empresa = VendedoresEmpresas.query.filter_by(id_vendedor=vendedor_id).first()
    if not vendedor_empresa:
        return jsonify({"error": "Vendedor does not belong to any empresa"}), 404

    empresa_id = vendedor_empresa.id_empresa
    cliente_ids = db.session.query(ClientesEmpresas.usuario_id).filter_by(empresa_id=empresa_id).all()
    cliente_ids = [id[0] for id in cliente_ids]

    usuarios = Usuario.query.filter(Usuario.id.in_(cliente_ids), Usuario.rol == "cliente").all()

    usuarios_info = [
        {
            "id": usuario.id,
            "nombre": usuario.nombre,
            "email": usuario.email
        }
        for usuario in usuarios
    ]

    return jsonify(usuarios_info)

@ruta_cliente.route('/cliente/<int:id>', methods=['GET'])
@token_required
def get_cliente(id):
    cliente = Usuario.query.filter_by(id=id, rol="cliente").first()
    if not cliente:
        return jsonify({"error": "Cliente not found"}), 404

    cliente_info = {
        "id": cliente.id,
        "nombre": cliente.nombre,
        "apellidos": cliente.apellidos,
        "telefono": cliente.telefono,
        "email": cliente.email,
        "direccion": cliente.direccion
    }

    return jsonify(cliente_info)

@ruta_cliente.route('/cliente/cedula/<int:cedula>', methods=['GET'])
@token_required
def get_cliente_by_cedula(cedula):
    cliente = Usuario.query.filter_by(cedula=cedula, rol="cliente").first()
    if not cliente:
        return jsonify({"error": "Cliente not found"}), 404

    cliente_info = {
        "id": cliente.id,
        "nombre": cliente.nombre,
        "apellidos": cliente.apellidos,
        "telefono": cliente.telefono,
        "email": cliente.email,
        "direccion": cliente.direccion
    }

    return jsonify(cliente_info)

@ruta_cliente.route('/cliente', methods=['POST'])
@token_required
def add_cliente():
    data = request.form
    id = data.get('id')
    nombre = data.get('nombre')
    apellidos = data.get('apellidos')
    telefono = data.get('telefono')
    email = data.get('email')
    direccion = data.get('direccion')

    existing_cliente = Usuario.query.filter_by(email=email).first()
    
    if existing_cliente:
        # Cliente exists, update the existing cliente
        existing_cliente.cedula = id
        existing_cliente.nombre = nombre
        existing_cliente.apellidos = apellidos
        existing_cliente.telefono = telefono
        existing_cliente.direccion = direccion

        db.session.commit()

        # Ensure relationship with the company
        vendedor_id = session.get('user_id')
        vendedor_empresa = VendedoresEmpresas.query.filter_by(id_vendedor=vendedor_id).first()
        empresa_id = vendedor_empresa.id_empresa

        cliente_empresa = ClientesEmpresas.query.filter_by(usuario_id=existing_cliente.id, empresa_id=empresa_id).first()
        if not cliente_empresa:
            cliente_empresa = ClientesEmpresas(
                usuario_id=existing_cliente.id,
                empresa_id=empresa_id
            )
            db.session.add(cliente_empresa)
            db.session.commit()

        return jsonify({"success": True})

    # Create new cliente
    nuevo_cliente = Usuario(
        cedula=id,
        nombre=nombre,
        apellidos=apellidos,
        telefono=telefono,
        email=email,
        direccion=direccion,
        usuario=email,
        contraseña=id,
        rol="cliente"
    )
    db.session.add(nuevo_cliente)
    db.session.commit()

    # Establish relationship with the company
    vendedor_id = session.get('user_id')
    vendedor_empresa = VendedoresEmpresas.query.filter_by(id_vendedor=vendedor_id).first()
    empresa_id = vendedor_empresa.id_empresa

    cliente_empresa = ClientesEmpresas(
        usuario_id=nuevo_cliente.id,
        empresa_id=empresa_id
    )
    db.session.add(cliente_empresa)
    db.session.commit()

    return jsonify({"success": True})


@ruta_cliente.route('/cliente/<int:id>', methods=['PUT'])
@token_required
def edit_cliente(id):
    cliente = Usuario.query.filter_by(id=id, rol="cliente").first()
    if not cliente:
        return jsonify({"error": "Cliente not found"}), 404

    data = request.form
    cliente.nombre = data.get('nombre')
    cliente.apellidos = data.get('apellidos')
    cliente.telefono = data.get('telefono')
    cliente.email = data.get('email')
    cliente.direccion = data.get('direccion')

    db.session.commit()

    return jsonify({"success": True})


@ruta_cliente.route('/cliente/<int:id>', methods=['DELETE'])
@token_required
def delete_cliente(id):
    cliente = Usuario.query.filter_by(id=id, rol="cliente").first()
    if not cliente:
        return jsonify({"error": "Cliente not found"}), 404

    ClientesEmpresas.query.filter_by(usuario_id=id).delete()
    db.session.delete(cliente)
    db.session.commit()

    return jsonify({"success": True})