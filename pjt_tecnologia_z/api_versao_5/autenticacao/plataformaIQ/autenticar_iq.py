import json
import requests
from api_versao_5.valores_globais import var_globais 
from api_versao_5.valores_globais.var_globais import URL_HTTP


def autenticar_iqoption(username, password):
    
    try:
        data = {
            "identifier": username,
            "password": password
        }
        auth = json.loads(requests.post( url=URL_HTTP,  data=data).content)
        print("-----------------")
        return auth
    except Exception as e:
        print(e)

def valida_credenciais(username, password):
    try:
        auth = autenticar_iqoption(username, password)
        autenticado = False
        if auth["code"] == "success":
            autenticado = True

        return [autenticado, auth]
    except Exception as e:
        print(e)