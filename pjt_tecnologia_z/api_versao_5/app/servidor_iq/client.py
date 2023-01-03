import json
import websocket
from time import sleep
from datetime import datetime
from api_versao_5.valores_globais import var_globais
from api_versao_5.mensageria.canais import Mensageria
from api_versao_5.processamento.processar_operacoes import ProcessarDadosOperacoes
from api_versao_5.processamento.processar_dados_servidor import ProcessarDadosServidor


class ClientWSS:
    def __init__(self, url_wss):
        self.url_wss = url_wss
        self.padrao_atual = "-"
        self.quantidade_candles = 0
        self.lista_ativos_abertos = None
        self.wss = websocket.WebSocketApp(
            url=self.url_wss,
            on_message=self.on_message,
            on_open=self.on_open,
            on_close=self.on_close,
            on_error=self.on_erro
        )
    
    def on_message(self, message):
        message = json.loads(message)
        # print(message)
    
        if message["name"] == "timeSync":
            var_globais.CHECK_CONN = True
            horario = datetime.now()
            segundo = horario.second
            minuto =  horario.minute
            if segundo >= 12 and segundo < 13:
                sleep(1)
                Mensageria.enviar_mensagem_coleta_resultados(10)

            elif segundo >= 52 and segundo < 53:
                sleep(1)
                Mensageria.enviar_mensagem_ativos_abertos()
            
            elif segundo >= 1 and segundo < 2:
                if minuto in var_globais.LISTA_MINUTOS[1]:
                    self.padrao_atual = "padrao - 1"
                    self.quantidade_candles = 5
                    print(f">>>>>>>>>>>>>>>>>>>>>> Processando cliente: {self.padrao_atual}")
                elif minuto in var_globais.LISTA_MINUTOS[0]:
                    self.padrao_atual = "padrao - 3"
                    self.quantidade_candles = 4
                    print(f">>>>>>>>>>>>>>>>>>>>>> Processando cliente: {self.padrao_atual}")
                sleep(1)
                Mensageria.coletar_candles(60, self.padrao_atual, self.quantidade_candles)
            elif segundo >= 26 and segundo < 27:
                self.padrao_atual = "padrao - 2"
                self.quantidade_candles = 2
                print(f">>>>>>>>>>>>>>>>>>>>>> Processando cliente: {self.padrao_atual}")
                sleep(1)
                Mensageria.coletar_candles(30, self.padrao_atual, self.quantidade_candles)

        elif message["name"] == "api_game_getoptions_result":
            ProcessarDadosOperacoes.processar_resultados_operacoes(message["msg"]["result"])

        
        elif message["name"] == "initialization-data":
            ProcessarDadosServidor(message["name"], 0).processar_ativos_abertos(message["msg"])
        
        
        elif message["name"] == "profile":
            var_globais.CHECK_STATUS_MSG = True
            try:
                var_globais.ID_USUARIO_PRACTICE = int(message["msg"]["balances"][1]["id"])
            except Exception as e:
                print(e)
            print(var_globais.ID_USUARIO_PRACTICE, var_globais.CHECK_STATUS_MSG)
        
        elif message["name"] == "option-opened":
            ProcessarDadosOperacoes.processar_abertura_operacao(message, self.padrao_atual)
        # elif message["name"] == "option-closed":
        #     threading.Thread(target=ProcessarDadosOperacoes.processar_fechamento_operacao(message)).start()

        elif message["request_id"] in var_globais.LISTA_ATIVOS_ABERTOS["p-30s"].values:
            ProcessarDadosServidor(message["request_id"].replace("-30", ""), 30).processar_dados_servidor_30s(message["msg"], self.padrao_atual)
        
        elif message["request_id"] in var_globais.LISTA_ATIVOS_ABERTOS["p-1m"].values:
            ProcessarDadosServidor(message["request_id"].replace("-60", ""), 60).processar_dados_servidor_1m(message["msg"], self.padrao_atual)
       
        
            
        
        

    def on_open(self):
        print("### conexão aberta com websocket ###")
    def on_close(self):
        self.wss.close()
        var_globais.CHECK_CONN = False
        print("### conexão encerrada com websocket ###")
    def on_erro(self, erro_wss):
        print(erro_wss)