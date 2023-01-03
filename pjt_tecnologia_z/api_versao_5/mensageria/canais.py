import json

from api_versao_5.valores_globais import var_globais
from api_versao_5.valores_globais.var_globais import OBJ_WSS
from api_versao_5.valores_globais.constantes import PARIDADES
from api_versao_5.conversao.checar_mercado import checar_tipo_mercado
from api_versao_5.conversao.converter_tempo import expiracao_operacoes
from api_versao_5.conversao.converter_tempo import data_hora_sao_paulo
from api_versao_5.mensageria.enviar_mensagem_wss import enviar_mensagem_wss


class Mensageria:
    def enviar_ssid(ssid):
        nome = "ssid"
        mensagem = ssid
        enviar_mensagem_wss(nome=nome, mensagem=mensagem, request_id="")
    
    def enviar_msg_config_usuario():
        lista_config = [
            {"name": "subscribeMessage", "msg": {"name": "portfolio.position-changed", "version": "2.0", "params": {"routingFilters": {"instrument_type": "cfd", "user_balance_id": var_globais.ID_USUARIO_PRACTICE}}}, "request_id": ""},
            {"name": "subscribeMessage", "msg": {"name": "portfolio.position-changed", "version": "2.0", "params": {"routingFilters": {"instrument_type": "forex", "user_balance_id": var_globais.ID_USUARIO_PRACTICE}}}, "request_id": ""},
            {"name": "subscribeMessage", "msg": {"name": "portfolio.position-changed", "version": "2.0", "params": {"routingFilters": {"instrument_type": "crypto", "user_balance_id": var_globais.ID_USUARIO_PRACTICE}}}, "request_id": ""},
            {"name": "subscribeMessage", "msg": {"name": "portfolio.position-changed", "version": "2.0", "params": {"routingFilters": {"instrument_type": "digital-option", "user_balance_id": var_globais.ID_USUARIO_PRACTICE}}}, "request_id": ""},
            {"name": "subscribeMessage", "msg": {"name": "portfolio.position-changed", "version": "2.0", "params": {"routingFilters": {"instrument_type": "turbo-option", "user_balance_id": var_globais.ID_USUARIO_PRACTICE}}}, "request_id": ""},
            {"name": "subscribeMessage", "msg": {"name": "portfolio.position-changed", "version": "2.0", "params": {"routingFilters": {"instrument_type": "binary-option", "user_balance_id": var_globais.ID_USUARIO_PRACTICE}}}, "request_id": ""},
            {"name": "subscribeMessage", "msg": {"name": "portfolio.order-changed", "version": "1.0", "params": {"routingFilters": {"instrument_type": "cfd"}}}, "request_id": ""},
            {"name": "subscribeMessage", "msg": {"name": "portfolio.order-changed", "version": "1.0", "params": {"routingFilters": {"instrument_type": "forex"}}}, "request_id": ""},
            {"name": "subscribeMessage", "msg": {"name": "portfolio.order-changed", "version": "1.0", "params": {"routingFilters": {"instrument_type": "crypto"}}}, "request_id": ""},
            {"name": "subscribeMessage", "msg": {"name": "portfolio.order-changed", "version": "1.0", "params": {"routingFilters": {"instrument_type": "digital-option"}}}, "request_id": ""},
            {"name": "subscribeMessage", "msg": {"name": "portfolio.order-changed", "version": "1.0", "params": {"routingFilters": {"instrument_type": "turbo-option"}}}, "request_id": ""},
            {"name": "subscribeMessage", "msg": {"name": "portfolio.order-changed", "version": "1.0", "params": {"routingFilters": {"instrument_type": "binary-option"}}}, "request_id": ""},
            {"name": "sendMessage", "msg": {"name": "get-initialization-data", "version": "3.0", "body": {}}, "request_id": "get-underlying-list"}
        ]
        for i in range(len(lista_config)):
            print(lista_config[i])
            var_globais.OBJ_WSS.wss.send(json.dumps(lista_config[i]).replace("'", '"'))
    
    def enviar_mensagem_ativos_abertos():
        try:
            msg = {"name": "sendMessage", "msg": {"name": "get-initialization-data", "version": "3.0", "body": {}}, "request_id": "get-underlying-list"}
            var_globais.OBJ_WSS.wss.send(json.dumps(msg).replace("'", '"'))
        except Exception as e:
            print("#########################")
            print(e)

    def enviar_operacao(ativo, direcao, timeframe):
        nome = "sendMessage"
        
        expiracao = expiracao_operacoes()[0]
        dadosMsg = {
            "body": {
                "price": 1.5,
                "active_id": PARIDADES[ativo],
                "expired": expiracao,
                "direction": direcao,
                "option_type_id": 3,
                "user_balance_id": var_globais.ID_USUARIO_PRACTICE
                },
                "name": "binary-options.open-option",
                "version": "1.0"
            }
        request_id = f"{ativo}-{direcao}-{timeframe}"
        
        enviar_mensagem_wss(nome=nome, mensagem=dadosMsg, request_id=request_id)
    
    def coletar_candles(timeframe, padrao, quantidade):

        dt = data_hora_sao_paulo()
        prosseguir_padrao = False
        if dt.minute in var_globais.LISTA_MINUTOS[0] and timeframe == 60:
            prosseguir_padrao = True
            print(">>> Analisando padrão 3 - 1 minuto")
        elif dt.minute in var_globais.LISTA_MINUTOS[1] and timeframe == 60:
            prosseguir_padrao = True
            print(">>> Analisando padrão 1 - 1 minuto")
        elif dt.minute in var_globais.LISTA_MINUTOS[2] and timeframe == 30:
            prosseguir_padrao = True
            print(">>> Analisando padrão 2 - 30 segundos")
      
        if prosseguir_padrao == False:
            print(">>> Aguardar horários das operações")
        elif prosseguir_padrao == True:
           
            lista_paridades_em_analise = []
            expiracao = expiracao_operacoes()[0]
            print(expiracao)

    
            for i in range(len(var_globais.LISTA_ATIVOS_ABERTOS)):
                id_ativo = int(var_globais.LISTA_ATIVOS_ABERTOS["id"][i])
                ativo = str(var_globais.LISTA_ATIVOS_ABERTOS["ativo"][i])
                print(f"ID: {id_ativo} | ATIVO: {ativo} | TIMEFRAME: {timeframe}")
                try:
                    msg = json.dumps({"name": "sendMessage", "msg": {"name": "get-candles", "version": "2.0", "body": {"active_id": id_ativo, "size": timeframe, "to": expiracao, "count": quantidade, "": 1}}, "request_id": f"{ativo}-{timeframe}"}).replace("'", '"')
                    lista_paridades_em_analise.append(msg)
                    print(msg)
                except Exception as e:
                    print(e)
            
            for i in range(len(lista_paridades_em_analise)):
                print(lista_paridades_em_analise[i])
                var_globais.OBJ_WSS.wss.send(lista_paridades_em_analise[i])
            



        


    

    

