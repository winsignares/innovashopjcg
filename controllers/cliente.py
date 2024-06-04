from flask import Blueprint, jsonify, render_template, request, redirect, session
from config.db import app, db, ma
from models.Cliente import Cliente, cliente_schema, clientes_schema

ruta_clientes = Blueprint("route_clientes", __name__)

@app.route('/newcliente', methods=['POST'])
def client_register():
    if request.method == 'POST':
        idc = request.form['id']
        nombre = request.form['nombre']
        p_number = request.form['telefono']
        email = request.form['email'] 
        user = request.form['user'] 
        pswd = request.form['password'] 
        dire = request.form['direccion']

        c_bdd = Cliente.query.filter_by(id=idc).all()
        new_user = Cliente.query.filter_by(user=user).all()
        
        # Si la id se encuentra actualmente registrada, no se vuelve a registrar
        if c_bdd:
            return jsonify({"error": "El ID ya esta en uso."}), 409
        if new_user:
            return jsonify({"error": "El Usuario-Login ya esta en uso."}), 409
        
        nuevo_cliente = Cliente(
            id=idc,
            nombre=nombre,
            email=email,
            dire=dire,
            p_number=p_number,
            user = user,
            pswd = pswd
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
