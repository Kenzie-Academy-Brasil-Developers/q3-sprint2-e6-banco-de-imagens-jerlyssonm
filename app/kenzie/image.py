from flask import jsonify, safe_join,send_file
import os

ALLOWED_EXTENSIONS = os.getenv('ALLOWED_EXTENSIONS').split(',')
FILES_DIRECTORY = os.getenv('FILES_DIRECTORY')
MAX_CONTENT_LENGTH = int(os.getenv('MAX_CONTENT_LENGTH'))
MAX_SIZE_AUTORIZATION = MAX_CONTENT_LENGTH * 1048576

def create_directory(name):
    """criar um diretorio em seu local atual"""
    os.mkdir(name)

def save_item(list):
    """salva os items em pastas com o nome de suas extensões"""
    for i in list:
        folders = os.listdir(f'./{FILES_DIRECTORY}')
        i_name = i[1].filename
        extension = i_name[-3::].lower()
        if extension in ALLOWED_EXTENSIONS:
            if extension not in folders:
                create_directory(f'./{FILES_DIRECTORY}/{extension}')
                i[1].save(f'./{FILES_DIRECTORY}/{extension}/{i_name}')
            else:
                i[1].save(f'./{FILES_DIRECTORY}/{extension}/{i_name}')
        else:
            return 'error'

def list_by_extension(extension):
    """lista os items por extensão"""
    out = os.listdir(f'./{FILES_DIRECTORY}/{extension}/')
    return jsonify(out)

def list_all_items():
    """lista todos os arquivos do diretorio"""
    current_dirs = os.listdir(f'./{FILES_DIRECTORY}/')
    out = []
    for folder in current_dirs:
        for items in os.listdir(f'./{FILES_DIRECTORY}/{folder}/'):
            out.append(items)
    return jsonify(out)

def donwload_by_name(file_name,local,extension):
    """solicita o download com as informações fornecidas corretamente"""
    path = os.getcwd()
    files_path = safe_join(path, local)
    all_path = safe_join(files_path, extension)
    files_list = os.listdir(all_path)

    if not file_name in files_list:
        return {'message': 'file not found.'} , 404

    out = safe_join(all_path, file_name)
    return send_file(out, as_attachment=True)    
    

def zipping(extension=None, compression_ratio=1):
    """comprime o aquivo antes de executar o download do diretorio, solicitando por paramento a extensão e o ratio da comprensão"""
    if compression_ratio < 0:
        compression_ratio = 0
    if compression_ratio > 9:
        compression_ratio = 9
    
    if extension == None:
        folders = [dir_root.split('/')[-1] for dir_root, dir_files ,files in os.walk(f"{FILES_DIRECTORY}") if len(files) > 0]
        os.system(f"cd {FILES_DIRECTORY} && zip -r {FILES_DIRECTORY}.zip {' '.join(folders)} && mv {FILES_DIRECTORY}.zip /tmp")
    else:
        os.system(f"cd {FILES_DIRECTORY}/{extension.lower()} && zip -{compression_ratio} {extension}.zip * && mv {extension}.zip /tmp")

def verification(file_name):
    """Verifica se o nome passado por paramentro ja existe no diretorio"""
    dir_father = os.listdir(f"./{FILES_DIRECTORY}")
    for i in dir_father:
        for img in os.listdir(f"./{FILES_DIRECTORY}/{i}"):
            if img == file_name:
                return True
    return False