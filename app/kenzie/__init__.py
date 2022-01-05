from flask import Flask,request,send_from_directory
from .image import *  #TODAS FUNÇỖES USADAS AQUI ESTÃO SENDO IMPORTADA DE image.
import os

app = Flask(__name__)
app.config['MAX_CONTENT_LENGTH'] = MAX_CONTENT_LENGTH

root = os.listdir()
if f'{FILES_DIRECTORY}' not in root:
    create_directory(f'./{FILES_DIRECTORY}')

@app.errorhandler(413)
def size_error(_):
    return {'message': f'Sorry the maximum size per image is {MAX_CONTENT_LENGTH} bytes equivalent 1MB!'},413
@app.get('/')
def home():
    return "<h1>Entrega 6 - Banco de Imagens</h1>"

@app.post('/upload')
def upload():  
    return save_item()  

@app.get('/files/<extension>')
def list_files_by_extension(extension):    
    return list_by_extension(extension)

@app.get('/files')
def list_files():
    return list_all_items()

@app.get('/download/<file_name>')
def download(file_name):
    extension = file_name[-3::]
    if not extension in ALLOWED_EXTENSIONS:
        return {'message': 'file not found.'}, 404
    else:
        return donwload_by_name(file_name,FILES_DIRECTORY,extension)

@app.get('/download-zip/')
def download_dir_as_zip():
    extension = request.args.get('file_extension')
    ratio = request.args.get('compression_ratio', 1)
    path = FILES_DIRECTORY
    if extension == None:
        return {'message': 'Incorrect parameter'}, 404
    elif not extension == None:
        path = extension
    try:
        zipping(extension, ratio)
        return send_from_directory('/tmp', path=f'{path}.zip', as_attachment=True), 200
    except:
        return {'message': f'{extension} file not found'}, 404
    
