from flask import Blueprint, render_template, request, redirect, session
from config.db import app, db, ma
from models.AdministradorModel import Admin, AdminSchema
from models.EmpresaModel import EMP, EMPSchema

ruta_administrador = Blueprint('route_administrador', __name__)

Admin_schema = AdminSchema()
Admins_schema = AdminSchema(many=True)

@app.route('/ingresaradmin', methods=['POST'])
def ingresaradmin():
    userad = request.form['userad'].replace(' ', '')
    passwordad = request.form['passwordad']
    userad = db.session.query(Admin).filter(Admin.userad == userad, Admin.passwordad == passwordad).all()
    
    
    if userad:
        resultado = Admin_schema.dump(userad)
        session['usuarioad'] = resultado
        
        return redirect('/portaladmin')
    else:
        return redirect('/loginad')
    

@app.route('/portaladmin', methods=['GET'])
def portaladministrativo():
    
    empresas = EMP.query.all()
    if 'usuarioad' in session:
        return render_template('./Admin/portalAdministrativo.html',usuario = session['usuarioad'],  empresas=empresas)
    else:
        return redirect('/')
    


@app.route('/loginad', methods=['GET'])
def loginadmin():
    return render_template('./Admin/loginadmin.html')


@app.route('/Crearempresa')
def crearempresa():
    return render_template('./Admin/Crearempresas.html')