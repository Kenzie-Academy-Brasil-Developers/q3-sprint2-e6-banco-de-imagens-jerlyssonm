from flask import jsonify, safe_join,send_file,request
import os

ALLOWED_EXTENSIONS = os.getenv('ALLOWED_EXTENSIONS').split(',')
FILES_DIRECTORY = os.getenv('FILES_DIRECTORY')
MAX_CONTENT_LENGTH = int(os.getenv('MAX_CONTENT_LENGTH'))

def create_directory(name):
    """create a directory in your current location with subfolders named extensions"""    
    os.mkdir(name)
    [os.mkdir(f'{name}/{i}') for i in ALLOWED_EXTENSIONS]


def save_item():
    """saves the items in folders named after their extensions"""
    
    files  = request.files
    file = files[list(files)[0]]
    file_name = file.filename
    extension = file_name[-3::].lower()


    if not extension in ALLOWED_EXTENSIONS:
        return {'message': 'This extension is not authorized by the admis.'},415

    path = safe_join(FILES_DIRECTORY, extension)


    if verification_name(file_name):
        return {'message': 'this name already exists.'},409

    file.save(safe_join(path, file_name))
    return {"message": "Saved Images"}, 201



def list_by_extension(extension):
    """lists the items by extension"""
    try:
        out = os.listdir(f'./{FILES_DIRECTORY}/{extension}/')
        return jsonify(out)
    except FileNotFoundError:
        return {'message': 'file not found.'},404

def list_all_items():
    """lists all the files in the directory"""
    current_dirs = os.listdir(f'./{FILES_DIRECTORY}/')
    out = []
    for folder in current_dirs:
        for items in os.listdir(f'./{FILES_DIRECTORY}/{folder}/'):
            out.append(items)
    return jsonify(out)


def donwload_by_name(file_name,local,extension):
    """requests the download with the correctly provided information"""
    path = os.getcwd()
    files_path = safe_join(path, local)
    all_path = safe_join(files_path, extension)
    files_list = os.listdir(all_path)

    try:        
        out = safe_join(all_path, file_name)
        return send_file(out, as_attachment=True)
    except :
        return {'message': 'file not found.'},404    

def zipping(extension=None, compression_ratio=1):
    """compresses the file before downloading it from the directory, asking for the extension and compression ratio in return"""
    if compression_ratio < 0:
        compression_ratio = 0
    if compression_ratio > 9:
        compression_ratio = 9
    
    if extension == None:
        folders = [dir_root.split('/')[-1] for dir_root, _ ,files in os.walk(f"{FILES_DIRECTORY}") if len(files) > 0]
        os.system(f"cd {FILES_DIRECTORY} && zip -r {FILES_DIRECTORY}.zip {' '.join(folders)} && mv {FILES_DIRECTORY}.zip /tmp")
    else:
        os.system(f"cd {FILES_DIRECTORY}/{extension.lower()} && zip -{compression_ratio} {extension}.zip * && mv {extension}.zip /tmp")


def verification_name(file_name):
    """Checks if the name passed by paramentro already exists in the directory"""

    dir_father = os.listdir(f"./{FILES_DIRECTORY}")
    for i in dir_father:
        for img in os.listdir(f"./{FILES_DIRECTORY}/{i}"):
            if img == file_name:
                return True
    
    return False

