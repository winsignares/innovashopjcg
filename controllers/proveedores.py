from flask import Blueprint, jsonify, render_template, request, redirect
from config.db import app, db, ma
from models.Proveedor import Proveedor, ProveedoresSchema

ruta_proveedores = Blueprint("route_proveedores", __name__)

proveedor_schema= ProveedoresSchema()
proveedores_schema= ProveedoresSchema(many=True)

@app.route('/registroproveedor', methods=['POST'])
def registrar_proveedor():
    if request.method == 'POST':
        
        id_proveedor = request.form['id']
        Nombre = request.form['nombre']
        Email = request.form['email'] 
        Direccion = request.form['direccion']
        Telefono = request.form['telefono'] 

        proveedor_existente = Proveedor.query.filter_by(id=id_proveedor).all()
        
        if proveedor_existente:
            return jsonify({"error": "El ID ya esta en uso."}), 409
        
        nuevo_proveedor = Proveedor(
            id=id_proveedor,
            nombre=Nombre,
            email=Email,
            direccion=Direccion,
            telefono=Telefono
        )

        db.session.add(nuevo_proveedor)
        db.session.commit()

    return redirect('/Portal_Empresa')