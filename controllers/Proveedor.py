# controllers/Proveedor.py
from flask import Blueprint, request, jsonify, session
from config.db import db
from models.Proveedor import Proveedor
from models.ProveedorEmpresa import ProveedorEmpresas
from models.Compra import Compra
from .Auth import token_required, empresa_required

ruta_proveedor = Blueprint('proveedor_route', __name__)

@ruta_proveedor.route('/proveedores', methods=['GET'])
def get_proveedores():
    proveedores = Proveedor.query.all()
    proveedores_info = [{"id": proveedor.id, "nombre": proveedor.nombre} for proveedor in proveedores]
    return jsonify(proveedores_info)

@ruta_proveedor.route('/proveedores-list', methods=['GET'])
@token_required
def get_proveedor():
    print("Route /proveedores-list accessed")  # Debugging statement

    empresa_id = session.get('empresa_id')
    print(f"Session empresa_id: {empresa_id}")  # Debugging statement

    if not empresa_id:
        print("No enterprise in session")  # Debugging statement
        return jsonify({"error": "No enterprise in session"}), 400

    proveedor_ids = ProveedorEmpresas.query.filter_by(empresa_id=empresa_id).with_entities(ProveedorEmpresas.proveedor_id).all()
    print(f"Proveedor IDs: {proveedor_ids}")  # Debugging statement

    if not proveedor_ids:
        print("No proveedores found for this enterprise")  # Debugging statement
        return jsonify({"error": "No proveedores found for this enterprise"}), 404

    proveedores = Proveedor.query.filter(Proveedor.id.in_([id for (id,) in proveedor_ids])).all()
    print(f"Proveedores found: {proveedores}")  # Debugging statement

    proveedores_info = [{
        "id": proveedor.id,
        "nombre": proveedor.nombre,
        "contacto": proveedor.contacto,
        "telefono": proveedor.telefono,
        "direccion": proveedor.direccion
    } for proveedor in proveedores]

    print(f"Proveedores info to return: {proveedores_info}")  # Debugging statement

    return jsonify(proveedores_info)


@ruta_proveedor.route('/add-proveedor', methods=['POST'])
@token_required
@empresa_required
def add_proveedor():
    data = request.json
    nombre = data.get('nombre')
    contacto = data.get('contacto')
    telefono = data.get('telefono')
    direccion = data.get('direccion')

    existing_proveedor = Proveedor.query.filter_by(nombre=nombre, contacto=contacto).first()
    if existing_proveedor:
        return jsonify({"error": "Proveedor already exists"}), 409

    nuevo_proveedor = Proveedor(
        nombre=nombre,
        contacto=contacto,
        telefono=telefono,
        direccion=direccion
    )
        
    db.session.add(nuevo_proveedor)
    db.session.commit()

    empresa_id = session.get('empresa_id')
    if not empresa_id:
        return jsonify({"error": "No enterprise in session"}), 400

    proveedor_empresa = ProveedorEmpresas(
        empresa_id=empresa_id,
        proveedor_id=nuevo_proveedor.id
    )
    
    db.session.add(proveedor_empresa)
    db.session.commit()

    return jsonify({"success": True})