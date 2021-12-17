from flask import Flask,request, send_from_directory
from .image import *
import os

app = Flask(__name__)

root = os.listdir()
if "bank" not in root:
    image.criar_diretorio("./bank")

@app.get('/')
def home():
    return "<h1>Entrega 6 - Banco de Imagens</h1>"

@app.post('/upload')
def upload():    
    recebidos = request.files.items()
    image.salvar_item(recebidos)
    return {"message": "Imagens Salvas"}

@app.get('/files/<extension>')
def list_files_by_extension(extension):    
    return image.listar_por_extensao(extension)

@app.get('/files')
def list_files():
    return image.listar_todos_items()

@app.get('/download-zip')
def download_dir_as_zip():      
    pass
@app.get('/download/<file_name>')
def download():
    pass