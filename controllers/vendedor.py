from flask import Blueprint, Flask, render_template,json, jsonify, redirect, session, request
from config.db import app, db, ma
from models.VendedoresModel import Vendedor, VendedorSchema
from models.ClienteModel import Cliente, ClientesSchema
from models.ProductosModel import Productos, ProductoSchema

ruta_vendedor = Blueprint("route_vendedor", __name__)

vendedor_schema = VendedorSchema()
vendedores_schema = VendedorSchema(many=True)

@app.route('/registrovendedor', methods=['POST'])
def registrar_vendedor():
    if request.method == 'POST':
        
        id_vendedor = request.form['id']
        Nombre = request.form['nombre']
        Email = request.form['email'] 
        Fecha_inicio = request.form['fecha_inicio']
        user = request.form['user'] 
        password = request.form['password'] 

        vendedor_existente = Vendedor.query.filter_by(id=id_vendedor).all()
        usuario = Vendedor.query.filter_by(user=user).all()
        
        if vendedor_existente:
            return jsonify({"error": "El ID ya esta en uso."}), 409
        if usuario:
            return jsonify({"error": "El Usuario-Login ya esta en uso."}), 409
        
        nuevo_vendedor = Vendedor(
            id=id_vendedor,
            nombre=Nombre,
            email=Email,
            fecha_inicio=Fecha_inicio,
            user = user,
            password = password
        )

        db.session.add(nuevo_vendedor)
        db.session.commit()

    return redirect('/Portal_Empresa')


@app.route('/Portal_Vendedor')
def portalvendedor():
    
    if 'usuario' in session:
        clientes = Cliente.query.all()
        productos = Productos.query.all()
        return render_template("./Portales/Portal_Vendedores.html", clientes=clientes, productos=productos)
    else:
        return redirect('/')
