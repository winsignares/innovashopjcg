from flask import Blueprint, render_template, request, redirect, session
from config.db import app, db, ma
from models.Admin import Admin, admin_shchema, admins_shchema
from models.Empresa import Empresa, EmpresaSchema
from controllers.user import user_schema

ruta_administrador = Blueprint('route_administrador', __name__)

@app.route('/admins', methods=['GET'])
def admins():
    return render_template('admin.html')

@app.route('/reg_empresa')
def crearempresa():
    empresas = Empresa.query.all()
    if 'adminu' in session:
        return render_template('admin-add-empresas.html', usuario = session['adminu'])

@app.route('/view_modules')
def modulosempresa():
    empresas = Empresa.query.all()
    if 'adminu' in session:
        return render_template('admin-modulos.html')

@app.route('/set_impuestos')
def set_impuestos():
    empresas = Empresa.query.all()
    if 'adminu' in session:
        return render_template('admin-impuestos.html')
    
@app.route('/login_v', methods=['GET'])
def login_view():
    return render_template('login.html')

@app.route('/search_by')
def search():
    query = request.args.get('query', '')

    if query:
        empresas = Empresa.query.filter(
            (Empresa.id.like(f'%{query}%')) |
            (Empresa.nombre.like(f'%{query}%'))
        ).all()
    else:
        empresas = Empresa.query.all()

    if 'adminu' in session:
        return render_template('admin-empresas.html', usuario=session['adminu'], empresas=empresas)