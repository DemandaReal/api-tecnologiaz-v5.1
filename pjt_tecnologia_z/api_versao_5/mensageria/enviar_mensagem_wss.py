import json
from api_versao_5.valores_globais import var_globais

def preparar_mensagem_wss(nome, mensagem, request_id):
    return json.dumps(dict(name=nome, msg=mensagem, request_id=request_id)).replace("'", '"')

def enviar_mensagem_wss(nome, mensagem, request_id):
    return var_globais.OBJ_WSS.wss.send(preparar_mensagem_wss(nome=nome, mensagem=mensagem, request_id=request_id))