from flask import Blueprint, jsonify, render_template, request, redirect, session, url_for, flash
from config.db import db, app
from models.EmpresaModel import EMP, EMPSchema
from models.VendedoresModel import Vendedor, VendedorSchema
from models.ClienteModel import Cliente, ClientesSchema
from models.ProveedoresModel import Proveedor, ProveedoresSchema
from models.ProductosModel import Productos, ProductoSchema

ruta_empresa = Blueprint('ruta_empresa', __name__)

EMP_schema = EMPSchema() 
EMPS_schema = EMPSchema(many=True) 

@app.route('/registroempresa', methods=['POST'])
def crear_empresa():
    if request.method == 'POST':
        
        id_empresa = request.form['companyid']
        nombre = request.form['name_emp']
        mail = request.form['mail_emp']
        ubicacion = request.form['ubicacion']
        status = request.form['status'] 
        fecha_inicio = request.form['fecha_Inicio']
        fecha_final = request.form['fecha_final']
        user = request.form['user'] 
        password = request.form['password'] 
        
        empresa_existente = EMP.query.filter_by(companyid=id_empresa).all()
        usuario = EMP.query.filter_by(user=user).all()
        
        if empresa_existente:
            return jsonify({"error": "El ID ya esta en uso."}), 409
        if usuario:
            return jsonify({"error": "El Usuario-Login ya esta en uso."}), 409

        nueva_empresa = EMP(
            companyid=id_empresa,
            name_emp=nombre,
            mail_emp=mail,
            ubicacion=ubicacion,
            status=status,
            fecha_Inicio=fecha_inicio,
            fecha_final=fecha_final,
            user = user,
            password = password
        )

        db.session.add(nueva_empresa)
        db.session.commit()

    return redirect('/portaladmin')

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


