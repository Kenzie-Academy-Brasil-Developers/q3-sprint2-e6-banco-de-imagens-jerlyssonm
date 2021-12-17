import os
from flask import jsonify

def criar_diretorio(name):
    os.mkdir(name)

def salvar_item(lista):
    for i in lista:
        folders = os.listdir('./bank')
        i_name = i[1].filename
        extension = i_name[-3::].lower()
        if extension not in folders:
            criar_diretorio(f'./bank/{extension}')
            i[1].save(f'./bank/{extension}/{i_name}')
        else:
            i[1].save(f'./bank/{extension}/{i_name}')

def listar_por_extensao(extension):
    out = os.listdir(f'./bank/{extension}/')
    return jsonify(out)

def listar_todos_items():
    out = os.listdir(f'./bank/')
    saida = []
    for pasta in out:
        for items in os.listdir(f'./bank/{pasta}/'):
            saida.append(items)
    return jsonify(saida)