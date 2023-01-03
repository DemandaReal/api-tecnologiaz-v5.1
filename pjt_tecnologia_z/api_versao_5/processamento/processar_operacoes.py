import threading
from time import sleep
from api_versao_5.valores_globais import var_globais
from api_versao_5.database.operacoes.insert import inserir_registro_database
from api_versao_5.database.operacoes.update import atualizar_registro_database

class ProcessarDadosOperacoes:
    def processar_abertura_operacao(dados, padrao):
        print(f"********************************>>>>>> processando abertura operação: {padrao}")
        try:
            dados = dados["msg"]
            dados_db = {
                "id_operacao" : dados["option_id"],
                "index_operacao" : dados["index"],
                "user_id" : dados["user_id"],
                "abertura" : dados["open_time"],
                "expiracao" : dados["expiration_time"],
                "direcao" : dados["direction"],
                "ativo" : dados["active"],
                "padrao": padrao
            }
            inserir_registro_database(dados_db)
            
        except Exception as e:
            print(e)

    def processar_fechamento_operacao(dados):
        sleep(3)
        dados = dados["msg"]
        id_operacao = dados["option_id"]

        resultado = dados["result"]
        if resultado == "win":
            resultado = 2
        elif resultado == "loose":
            resultado = 3
        else:
            resultado = 4
        
        atualizar_registro_database(id_operacao, resultado)
        
        