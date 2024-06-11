from flask import Blueprint, jsonify, render_template, request, redirect
from config.db import app, db, ma
from models.Proveedor import Proveedor, ProveedoresSchema

ruta_proveedores = Blueprint("route_proveedores", __name__)

proveedor_schema= ProveedoresSchema()
proveedores_schema= ProveedoresSchema(many=True)