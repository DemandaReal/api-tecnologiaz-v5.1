import json
import pandas as pd


from api_versao_5.mensageria.canais import Mensageria
from api_versao_5.valores_globais import var_globais


class ProcessarDadosServidor:
    def __init__(self, request_id, timeframe):
        self.request_id = request_id
        self.timeframe = timeframe
    
    def processar_ativos_abertos(self, dados):
        try:
            print("processando dados ativos abertos --------------------------------------------------")
            var_globais.LISTA_ATIVOS_ABERTOS = None
            lista_ativos = [
                [], # 0 id
                [], # 1 name
                [], # 2 ticker
                [], # 3 is_suspended
                [], # 4 enabled
                [], # 5 padrão 30s
                [], # 6 padrão 1m
                [], # 7 mercado
            ]
            for i in dados["binary"]["actives"]:
                try:
                    id   = dados["binary"]["actives"][i]["id"]
                    name = dados["binary"]["actives"][i]["name"]
                    ticker = dados["binary"]["actives"][i]["ticker"]
                    is_suspended = dados["binary"]["actives"][i]["is_suspended"]
                    enabled = dados["binary"]["actives"][i]["enabled"]
                    # print(id, name, ticker, is_suspended, enabled)
                    
                    if enabled == True and is_suspended == False:
                        lista_ativos[0].append(id)
                        lista_ativos[1].append(name)
                        lista_ativos[2].append(ticker)
                        lista_ativos[3].append(is_suspended)
                        lista_ativos[4].append(enabled)
                        lista_ativos[5].append(f"{ticker}-30")
                        lista_ativos[6].append(f"{ticker}-60")
                        if "OTC" in ticker:
                            lista_ativos[7].append("otc")
                        else:
                            lista_ativos[7].append("aberto")
                    
                except Exception as e:
                    print(e)
            if len(lista_ativos[0]) >= 1:

                df = pd.DataFrame(list(zip(
                        lista_ativos[0],
                        lista_ativos[1],
                        lista_ativos[2],
                        lista_ativos[3],
                        lista_ativos[4],
                        lista_ativos[5], lista_ativos[6], lista_ativos[7]
                    )),
                    columns=[
                        "id", "nome", "ativo", "supenso", "status",
                        "p-30s", "p-1m", "mercado"
                    ])
                print(df)
                var_globais.LISTA_ATIVOS_ABERTOS = df
            else:
                var_globais.LISTA_ATIVOS_ABERTOS = "nenhum ativo encontrado"
        except Exception as e:
            print(e)
    
    def processar_dados_servidor_30s(self, dados, padrao):
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

    def processar_dados_servidor_1m(self, dados, padrao):
        
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
        if padrao == "padrao - 1":
            print(f"---------------------------------->>> processando: {padrao}")
            if df["fech candle"][0] != df["fech candle"][1]:
                if df["fech candle"][3] != "sem mov":
                    if df["fech candle"][3] == "alta":
                        direcao = "put"
                    elif df["fech candle"][3] == "baixa":
                        direcao = "call"
        
        elif padrao == "padrao - 3":
            print(f"---------------------------------->>> processando: {padrao}")
            if df["fech candle"][0] == df["fech candle"][1]:
                if df["fech candle"][1] != "sem mov":
                    if df["fech candle"][1] == "alta":
                        direcao = "call"
                    elif df["fech candle"][1] == "baixa":
                        direcao = "put"

        
        if direcao != "-":
            Mensageria.enviar_operacao(self.request_id, direcao, self.timeframe)
    
    




    
   
