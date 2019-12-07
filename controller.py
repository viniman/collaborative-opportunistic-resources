#!/usr/bin/python
# -*- coding: utf8 -*-

import subprocess

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


def run_ubuntu():
    r = subprocess.call("docker run -it -m 512M --name app01 ubuntu", shell=True)
    return r

def runContainer(image_name, container_name="app01", options=None):
    r = subprocess.call("docker run -it " + options + " --name " + container_name + image_name, shell=True)
    return r

def remove_container(container_name):
    print("============================================================\n\
===== " + container_name + ": Stopping and removing container =====\n\
============================================================\n")
    r = subprocess.call("docker rm -f " + container_name, shell=True)
    return r