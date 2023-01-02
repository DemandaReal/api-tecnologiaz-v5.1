from datetime import date
from api_versao_5.conversao.converter_tempo import expiracao_operacoes
from api_versao_5.valores_globais.var_globais import LISTA_ANALISES

def checar_tipo_mercado():
    tipo_mercado = "-"
    lista_dias_semanas = ["seg", "ter", "qua", "qui", "sex", "sab", "dom"]
    lista_dias_semanas_aberto = ["seg", "ter", "qua", "qui", "sex"]
    lista_horas_otc_dia_semana = [18, 19, 20, 21]
    lista_horas_otc_sex = [16, 17, 18, 19, 20, 21, 22, 23]

    # dataHora = datetime.now()
    dataHora = expiracao_operacoes()[1]
    dia = dataHora.day
    mes = dataHora.month
    ano = dataHora.year
    hora = dataHora.hour
    minuto = dataHora.minute
    diaSemana = lista_dias_semanas[date(year=ano, month=mes, day=dia).weekday()]
    print(diaSemana)

    if diaSemana == "sab":
        # print("otc - sab")
        tipo_mercado = "otc"
    elif diaSemana == "dom":
        if hora >= 22:
            # print("aberto - dom", hora, minuto)
            tipo_mercado = "aberto"
        else:
            # print("otc - dom", hora, minuto)
            tipo_mercado = "otc"

    elif diaSemana in lista_dias_semanas_aberto:
        if hora in lista_horas_otc_dia_semana:
            # print("otc")
            tipo_mercado = "otc"
        else:
            if diaSemana == "sex" and hora >= 16 and minuto >= 30:
                # print("otc", hora, minuto)
                tipo_mercado = "otc"
            else:
                # print("aberto", hora, minuto)
                tipo_mercado = "aberto"
    
    lista_paridades = []
    for i in range(len(LISTA_ANALISES)):
        if tipo_mercado == "otc":
            lista_paridades.append(f"{LISTA_ANALISES[i]}-OTC")
        else:
            lista_paridades.append(LISTA_ANALISES[i])
    
    return tipo_mercado, lista_paridades
