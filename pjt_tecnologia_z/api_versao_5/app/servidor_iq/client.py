import json
import websocket
import threading
from time import sleep
from datetime import datetime
from api_versao_5.valores_globais import var_globais
from api_versao_5.mensageria.canais import Mensageria
from api_versao_5.processamento.processar_operacoes import ProcessarDadosOperacoes
from api_versao_5.processamento.processar_dados_servidor import ProcessarDadosServidor
from api_versao_5.processamento.processar_query_rank_paridades import atualizar_rank_paridades


class ClientWSS:
    def __init__(self, url_wss):
        self.url_wss = url_wss
        self.padrao_atual = "-"
        self.wss = websocket.WebSocketApp(
            url=self.url_wss,
            on_message=self.on_message,
            on_open=self.on_open,
            on_close=self.on_close,
            on_error=self.on_erro
        )
    
    def on_message(self, message):
        message = json.loads(message)
        print(message)
      
   
        if message["name"] == "timeSync":
            var_globais.CHECK_CONN = True
            segundo = datetime.now().second
            # coleta de candles e operações
            if segundo >= 1 and segundo < 2:
                self.padrao_atual = "padrao - 1"
                sleep(1)
                Mensageria.coletar_candles(60)
            elif segundo >= 27 and segundo < 28:
                self.padrao_atual = "padrao - 2"
                sleep(1)
                Mensageria.coletar_candles(30)
            
            # atualização do rank_paridades
            elif segundo >= 12 and segundo < 13:
                atualizar_rank_paridades()

        elif message["name"] == "profile":
            var_globais.CHECK_STATUS_MSG = True
            try:
                var_globais.ID_USUARIO_PRACTICE = int(message["msg"]["balances"][1]["id"])
            except Exception as e:
                print(e)
            print(var_globais.ID_USUARIO_PRACTICE, var_globais.CHECK_STATUS_MSG)
        
        elif message["name"] == "option-opened":
            ProcessarDadosOperacoes.processar_abertura_operacao(message)
        elif message["name"] == "option-closed":
            ProcessarDadosOperacoes.processar_fechamento_operacao(message)

        elif message["request_id"] in var_globais.LISTA_ANALISE_30S:
            ProcessarDadosServidor(message["request_id"].replace("-30", ""), 30).processar_dados_servidor_30s(message["msg"])
            
        elif message["request_id"] in var_globais.LISTA_ANALISE_1M:
            ProcessarDadosServidor(message["request_id"].replace("-60", ""), 60).processar_dados_servidor_1m(message["msg"])
        
        

    def on_open(self):
        print("### conexão aberta com websocket ###")
    def on_close(self):
        self.wss.close()
        var_globais.CHECK_CONN = False
        print("### conexão encerrada com websocket ###")
    def on_erro(self, erro_wss):
        print(erro_wss)