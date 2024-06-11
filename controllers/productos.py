import os
from flask import Blueprint, jsonify, request, redirect
from config.db import app, db
from models.Producto import Productos, ProductoSchema

productos_bp = Blueprint("ruta_productos", __name__)

producto_schema = ProductoSchema()
productos_schema = ProductoSchema(many=True)

def to_float(value, default=0.0):
    try:
        return float(value) if value else default
    except ValueError:
        return default

@productos_bp.route('/registrar_productos', methods=['POST'])
def registrar_producto():
    id_producto = request.form['id']
    nombre = request.form.get('nombre', '')
    preciouni = to_float(request.form.get('preciouni'), 0.0)
    alternos = request.form.get('alternos', '')
    precioventa = to_float(request.form.get('precioventa'), 0.0)
    cantidad = to_float(request.form.get('cantidad'), 0)
    cantidadmin = to_float(request.form.get('cantidadmin'), 0)
    iva = to_float(request.form.get('iva'), 0.0)

    if not nombre:
        return jsonify({"error": "El nombre es obligatorio"}), 400

    producto_existente = Productos.query.filter_by(id=id_producto).all()

    if producto_existente:
        return jsonify({"error": "Este producto ya existe."}), 409

    nuevo_producto = Productos(
        id=id_producto,
        nombre=nombre,
        preciouni=float(preciouni),
        alternos=alternos,
        precioventa=float(precioventa),
        cantidad=cantidad,
        cantidadmin=cantidadmin,
        iva=float(iva)
    )
    db.session.add(nuevo_producto)
    db.session.commit()

    return redirect('/vendedor_agg_productos')

@productos_bp.route('/search', methods=['GET'])
def search_products():
    termino = request.args.get('termino', '')

    if not termino:
        return jsonify([])

    productos = Productos.query.filter(Productos.nombre.ilike(f"%{termino}%")).limit(10).all()

    return jsonify([{'id': producto.id, 'nombre': producto.nombre} for producto in productos])

