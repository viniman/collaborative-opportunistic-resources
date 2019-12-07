#!/usr/bin/python
# -*- coding: utf-8 -*-
from flask import Flask
from flask import jsonify # transforma dicionario em json
from flask import abort # abor se não achar tarefa com erro 404
from flask import make_response # responder codigo erro json
from flask import request # adicionar tarefa
from flask import url_for # funcao auxiliar make_public_resource
import json # tranformar um dicionário em uma string json
import controller # arquivo controlador de containers


'''
Autor: Vinicius Carlos de Oliveira
Disciplina: Seminários em Computação VI‎ (DCC102 - 2019.3)
Professor: Marcelo Moreno
-------------------------

Gerenciador de aplicação RESTful
Registra, consulta, remove, adiciona e modifica recurso
Execução com Python 3 via terminal: $ python3 app.py

Arquivos:
"app.py": aplicação do serviço RESTful, arquivo que deve ser executação
"controller.py": controlador de aplicação, ele inicia os containers
"requistions.txt": Exemplos de execução
"container_exec.txt": Informações sobre o docker
"Dockerfile": caso queira executar essa aplicação também em um container
"images.jpg": imagens de containers utilizadas

Diretórios:
"resources": informacoes sobre os recursos
"contracts": informacoes sobre os usuarios e recursos usados

* Falta fazer a integração entre o app.py e o controller.py *

'''

app = Flask(__name__)

# Abre arquivo de recursos para leitura
with open('resources/all_resources.json') as json_file:
    resources = json.load(json_file)

# teste - imprime todos os ids dos recursos assi que é executado
[print(resource['id']) for resource in resources]

# Metodo para visualizar um recurso pelo id
@app.route('/collabopportunist/resources/<int:resource_id>', methods=['GET'])
def get_resource(resource_id):
    resource = [resource for resource in resources if resource['id'] == resource_id]
    if len(resource) == 0:
        abort(404)
    return jsonify({'resource': resource[0]})

# Cria JSON de not found caso não econtre o desejado e dê erro 404
@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not found'}), 404)


# Metodo que cria recurso
@app.route('/collabopportunist/resources', methods=['POST'])
def create_resource():
    if not request.json or not 'type' in request.json:
        abort(400)
    resource = {
        'id': resources[-1]['id'] + 1,
        'use': 0,
        'unused': request.json['unused'],
        'type': request.json['type'],
        'container_image_id': request.json['container_image_id'],
        'container_image_name': request.json['container_image_name'],
        'host': request.json['host'],
        'ip_host': request.json['ip_host']
    }
    resources.append(resource)
    with open('resources/all_resources.json', 'w') as outfile:
        json.dump(resources, outfile, indent=4)
    return jsonify({'resource': resource}), 201


@app.route('/collabopportunist/resources/<int:resource_id>', methods=['PUT'])
def update_resource(resource_id):
    resource = [resource for resource in resources if resource['id'] == resource_id]
    if len(resource) == 0:
        abort(404)
    if not request.json:
        abort(400)
    
    if 'use' in request.json:# and int(resource[0]['unused'] - request.json.get('use', resource[0]['use'])) >= 0:
        resource[0]['use'] = request.json.get('use', resource[0]['use'])
    if 'unused' in request.json:
        resource[0]['unused'] = request.json.get('unused', resource[0]['unused'])
    if 'container_image_name' in request.json:
        resource[0]['container_image_name'] = request.json.get('container_image_name', resource[0]['container_image_name'])
    if 'container_image_id' in request.json:
        resource[0]['container_image_id'] = request.json.get('container_image_id', resource[0]['container_image_id'])
    if 'deepinvm' in request.json:
        resource[0]['deepinvm'] = request.json.get('deepinvm', resource[0]['deepinvm'])
    
    with open('resources/all_resources.json', 'w') as outfile:
        json.dump(resources, outfile, indent=4)

    return jsonify({'resource': resource[0]})

@app.route('/collabopportunist/resources/<int:resource_id>', methods=['DELETE'])
def delete_resource(resource_id):
    resource = [resource for resource in resources if resource['id'] == resource_id]
    if len(resource) == 0:
        abort(404)
    resources.remove(resource[0])

    with open('resources/all_resources.json', 'w') as outfile:
        json.dump(resources, outfile, indent=4)

    return jsonify({'result': True})

# função auxiliar que gera uma versão "pública" de uma tarefa para enviar ao cliente
'''
Pega um recurso do e cria um novo recurso que possua todos os campos, 
exceto o id, que é substituído por outro campo chamado uri, gerado com o url_for do Flask
'''
def make_public_resource(resource):
    new_resource = {}
    for field in resource:
        if field == 'id':
            new_resource['uri'] = url_for('get_resource', resource_id=resource['id'], _external=True)
        else:
            new_resource[field] = resource[field]
    return new_resource

# Retorna a lista de recursos, passando por essa função antes de envir ao cliente
@app.route('/collabopportunist/resources', methods=['GET'])
def get_resources():
    return jsonify({'resources': [make_public_resource(resource) for resource in resources]})



if __name__ == "__main__":
  app.run(debug=True)