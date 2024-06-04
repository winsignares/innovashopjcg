from flask import Blueprint, render_template, jsonify, request, redirect, session
from config.db import db, app
from models.Empresa import Empresa, EmpresaSchema
from models.Proveedor import Proveedor
from models.Producto import Productos
from models.Vendedor import Vendedor
from models.Cliente import Cliente

ruta_empresa = Blueprint('ruta_empresa', __name__)

empresa_schema = EmpresaSchema() 
empresas_schema = EmpresaSchema(many=True) 

@app.route('/Portal_Empresa', methods=['GET'])
def portalempresa():
    if 'usuario' in session:
        vendedores = Vendedor.query.all()
        clientes = Cliente.query.all()
        proveedores = Proveedor.query.all()
        productos = Productos.query.all()
        return render_template("./Portales/Portal_Empresa.html", usuario = session['usuario'], vendedores=vendedores, clientes=clientes, proveedores=proveedores, productos=productos)
    else:
        return redirect('/')
    
@app.route('/registroempresa', methods=['POST'])
def crear_empresa():
    if request.method == 'POST':
        id_empresa = request.form['companyid']
        user = request.form['user'] 
        password = request.form['password'] 
        nombre = request.form['nombre']
        email = request.form['email']
        estado = request.form['status'] 
        fecha_i = request.form['fecha_Inicio']
        f_plazo = request.form['fecha_final']
        id_admin = request.form['id_admin']
        
        e_bdd = Empresa.query.filter_by(id=id_empresa).all()
        new_e_user = Empresa.query.filter_by(user=user).all()
        
        if e_bdd:
            return jsonify({'error': 'Esta Empresa ya se encuentra registrada'}), 409
        if new_e_user:
            return jsonify({'error': 'Este Usuario ya se encuentra registrado'}), 409

        empresa_data = {
            'id': id_empresa,
            'user': user,
            'password': password,
            'nombre': nombre,
            'email': email,
            'estado': estado,
            'fecha_i': fecha_i,
            'f_plazo': f_plazo,
            'id_admin': id_admin
        }
        n_empresa = Empresa(**empresa_data)


        db.session.add(n_empresa)
        db.session.commit()

    return redirect('/portaladmin')


