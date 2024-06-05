from flask import Blueprint, Flask, render_template,json, jsonify, redirect, session, request
from config.db import app, db, ma
from models.Vendedor import Vendedor, VendedorSchema
from models.Cliente import Cliente, ClientesSchema
from models.Producto import Productos, ProductoSchema
from controllers.vendedor import registrar_vendedor

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

    return redirect('/registrar_vendedor')

@app.route('/vendedor-clientes-lista')
def listar_clientes():
    vendedor_id = session['vendedor_id']
    if "empresa" in session:
        clientes = Cliente.query.filter_by(vendedor_id=vendedor_id).all()
    return render_template('vendedor_clientes_lista.html', clientes=clientes)

@app.route('/registrar_vendedor')
def registrar_vendedor():
    return render_template('vendedores-empresas.html')

@app.route('/vendedor_clientes')
def vendedor_clientes():
    return render_template('vendedor_clientes.html')

@app.route('/vendedor_consultar')
def vendedor_consultar():
    return render_template('vendedor_consultar.html')

@app.route('/vendedor_cotizacion')
def vendedor_cotizacion():
    return render_template('vendedor_cotizacion.html')

@app.route('/vendedor_compra')
def vendedor_compra():
    return render_template('vendedor_compra.html')

@app.route('/vendedor_agg_productos')
def vendedor_agg_productos():
    return render_template('vendedor-stock-aggproductos.html')

@app.route('/home_vendedor')
def portalvendedor():
    
    if 'usuario' in session:
        clientes = Cliente.query.all()
        productos = Productos.query.all()
        return render_template("vendedor-inicio.html")
    else:
        return redirect('/')
