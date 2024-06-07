from flask import Blueprint, jsonify, render_template, request, redirect, session
from config.db import app, db, ma
from models.Cliente import Cliente

ruta_clientes = Blueprint("route_clientes", __name__)

@app.route('/newcliente', methods=['POST'])
def client_register():
    if request.method == 'POST':
        client_id  = request.form['id']
        nombre = request.form['nombre']
        p_number = request.form['telefono']
        email = request.form['email'] 
        user = request.form['user'] 
        pswd = request.form['password'] 
        dire = request.form['direccion']

        c_bdd = Cliente.query.filter_by(id=client_id ).all()
        new_user = Cliente.query.filter_by(user=user).all()
        
        if c_bdd:
            return jsonify({"error": "El ID ya esta en uso."}), 409
        if new_user:
            return jsonify({"error": "El Usuario-Login ya esta en uso."}), 409
        
        nuevo_cliente = Cliente(
            id=client_id ,
            nombre=nombre,
            p_number=p_number,
            email=email,
            user = user,
            pswd = pswd,
            dire=dire
        )

        db.session.add(nuevo_cliente)
        db.session.commit()

    return redirect('vendedor-clientes.html')

@app.route('/home_clientes')
def portalcliente():
    if 'usuario' in session:
        return render_template("cliente.html")
    else:
        return redirect('/')
