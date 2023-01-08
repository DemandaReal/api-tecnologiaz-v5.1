from datetime import datetime, timedelta
from pytz import timezone
from time import time

def timestamp_server():
    tmst = datetime.fromtimestamp(time(), tz=timezone("UTC")).timestamp()
    return tmst

def converter_timestamp(timestamp):
    dataHora = datetime.fromtimestamp(timestamp, tz=timezone("America/Sao_Paulo"))
    return dataHora

def data_hora_sao_paulo():
    tmst = timestamp_server()
    horaSP = converter_timestamp(tmst)
    return horaSP

def expiracao_query_diaria():
    dataHoraSP = data_hora_sao_paulo()
    dia = dataHoraSP.day
    mes = dataHoraSP.month
    ano = dataHoraSP.year
    hora = 0
    minuto = 0
    expiracao_query = int(datetime(year=ano, month=mes, day=dia, hour=hora, minute=minuto).timestamp())
    return expiracao_query

def expiracao_query_diaria_2():
    tDelta = timedelta(hours=3)
    dataHoraSP = data_hora_sao_paulo() + tDelta
    dia = dataHoraSP.day
    mes = dataHoraSP.month
    ano = dataHoraSP.year
    hora = 6
    minuto = 0
    expiracao_query = int(datetime(year=ano, month=mes, day=dia, hour=hora, minute=minuto).timestamp())
    expiracao_query = int(datetime(year=ano, month=mes, day=dia, hour=hora, minute=minuto).timestamp())
    return expiracao_query






def expiracao_operacoes():
    tmst = timestamp_server()
    horaSP = datetime.now()
    timestamp = datetime.fromtimestamp(tmst, tz=timezone("UTC"))
    
    if horaSP.hour == timestamp.hour:
        pass
    else:
        timestamp = datetime.fromtimestamp(tmst, tz=timezone("America/Sao_Paulo"))

    minuto = timestamp.minute
    if timestamp.second < 30:
        minuto = minuto + 1
    else:
        minuto = minuto + 2  
    expiracao = datetime(
        year=timestamp.year,
        month=timestamp.month,
        day=timestamp.day,
        hour=timestamp.hour,
        minute=minuto
        )
    print(f">> Expiracao: {int(expiracao.timestamp())}")
    return int(expiracao.timestamp()), expiracao

