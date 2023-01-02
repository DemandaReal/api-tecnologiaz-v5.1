import json
import pandas as pd
from api_versao_5.mensageria.canais import Mensageria

class ProcessarDadosServidor:
    def __init__(self, request_id, timeframe):
        self.request_id = request_id
        self.timeframe = timeframe
    
    def processar_dados_servidor_30s(self, dados):
        print(f"Processo: ProcessarDadosServidor | Sub-Processo: processar_dados_servidor_30s | {self.request_id} | timefram: {self.timeframe}")
        dados = dados["candles"]
        lista_dados = [
            [], # - 0 from
            [], # - 1 max
            [], # - 2 open
            [], # - 3 close
            [], # - 4 min
            [], # - 5 fech candle
            [], # - 6 ativo
            [], # - 7 timeframe
        ]
        for i in range(len(dados)):
            
            fech_candle = None
            if dados[i]["close"] > dados[i]["open"]:
                fech_candle = "alta"
            elif dados[i]["close"] < dados[i]["open"]:
                fech_candle = "baixa"
            else:
                fech_candle = "sem mov"
            
            lista_dados[0].append(dados[i]["from"])
            lista_dados[1].append(dados[i]["max"])
            lista_dados[2].append(dados[i]["open"])
            lista_dados[3].append(dados[i]["close"])
            lista_dados[4].append(dados[i]["min"])
            lista_dados[5].append(fech_candle)
            lista_dados[6].append(self.request_id)
            lista_dados[7].append(self.timeframe)
        
        df = pd.DataFrame(list(zip(
            lista_dados[0],
            lista_dados[1],
            lista_dados[2],
            lista_dados[3],
            lista_dados[4],
            lista_dados[5],
            lista_dados[6], lista_dados[7],
        )), columns=[
            "from", "max", "open", "close", "min", "fech candle",
            "ativo", "timeframe"
            ])
        print(df)
        direcao = "-"
       
        if df["fech candle"][1] != "sem mov":
            if df["fech candle"][1] == "alta":
                direcao = "put"
            elif df["fech candle"][1] == "baixa":
                direcao = "call"
        
        if direcao != "-":
            Mensageria.enviar_operacao(self.request_id, direcao, self.timeframe)

    def processar_dados_servidor_1m(self, dados):
        print(f"Processo: ProcessarDadosServidor | Sub-Processo: processar_dados_servidor_1m | {self.request_id} | timefram: {self.timeframe}")
        dados = dados["candles"]
        lista_dados = [
            [], # - 0 from
            [], # - 1 max
            [], # - 2 open
            [], # - 3 close
            [], # - 4 min
            [], # - 5 fech candle
            [], # - 6 ativo
            [], # - 7 timeframe
        ]
        for i in range(len(dados)):
            
            fech_candle = None
            if dados[i]["close"] > dados[i]["open"]:
                fech_candle = "alta"
            elif dados[i]["close"] < dados[i]["open"]:
                fech_candle = "baixa"
            else:
                fech_candle = "sem mov"
            
            lista_dados[0].append(dados[i]["from"])
            lista_dados[1].append(dados[i]["max"])
            lista_dados[2].append(dados[i]["open"])
            lista_dados[3].append(dados[i]["close"])
            lista_dados[4].append(dados[i]["min"])
            lista_dados[5].append(fech_candle)
            lista_dados[6].append(self.request_id)
            lista_dados[7].append(self.timeframe)
        
        df = pd.DataFrame(list(zip(
            lista_dados[0],
            lista_dados[1],
            lista_dados[2],
            lista_dados[3],
            lista_dados[4],
            lista_dados[5],
            lista_dados[6], lista_dados[7],
        )), columns=[
            "from", "max", "open", "close", "min", "fech candle",
            "ativo", "timeframe"
            ])
        print(df)
        direcao = "-"
        if df["fech candle"][0] != df["fech candle"][1]:
            if df["fech candle"][3] != "sem mov":
                if df["fech candle"][3] == "alta":
                    direcao = "put"
                elif df["fech candle"][3] == "baixa":
                    direcao = "call"
        
        if direcao != "-":
            Mensageria.enviar_operacao(self.request_id, direcao, self.timeframe)
    
    




    
   
