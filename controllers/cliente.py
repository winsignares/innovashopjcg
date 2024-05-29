from flask import Blueprint, jsonify, render_template, request, redirect, session
from config.db import app, db, ma
from models.ClienteModel import Cliente, ClientesSchema

ruta_clientes = Blueprint("route_clientes", __name__)

cliente_schema= ClientesSchema()
clientes_schema= ClientesSchema(many=True)

@app.route('/registrocliente', methods=['POST'])
def registrar_cliente():
    if request.method == 'POST':
        
        id_cliente = request.form['id']
        Nombre = request.form['nombre']
        Email = request.form['email'] 
        Direccion = request.form['direccion']
        Telefono = request.form['telefono']
        user = request.form['user'] 
        password = request.form['password'] 

        cliente_existente = Cliente.query.filter_by(id=id_cliente).all()
        usuario = Cliente.query.filter_by(user=user).all()
        
        if cliente_existente:
            return jsonify({"error": "El ID ya esta en uso."}), 409
        if usuario:
            return jsonify({"error": "El Usuario-Login ya esta en uso."}), 409
        
        nuevo_cliente = Cliente(
            id=id_cliente,
            nombre=Nombre,
            email=Email,
            direccion=Direccion,
            telefono=Telefono,
            user = user,
            password = password
        )

        db.session.add(nuevo_cliente)
        db.session.commit()

    return redirect('/Portal_Vendedor')

@app.route('/Portal_Cliente')
def portalcliente():
    
    if 'usuario' in session:
        return render_template("./Portales/Portal_Cliente.html")
    else:
        return redirect('/')
