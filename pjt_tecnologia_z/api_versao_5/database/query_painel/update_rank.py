
from api_versao_5.database.conn.conn_db import conexao_db_api
from api_versao_5.conversao.checar_mercado import checar_tipo_mercado
from api_versao_5.conversao.converter_tempo import expiracao_query_diaria
from api_versao_5.valores_globais import var_globais


def query_rank_painel():
    mercado = var_globais.LISTA_ATIVOS_ABERTOS[var_globais.LISTA_ATIVOS_ABERTOS.index==0]["mercado"].values[0]
    try:
        db = conexao_db_api()
        conn = db[0]
        cursor = db[1]
        print("----------------------------->>> DB CONECTADO")
        exp = expiracao_query_diaria()

        query = f'SELECT * FROM operacoes_api WHERE expiracao >= "{exp}" and tipo_mercado = "{mercado}"'
        print(query)
        cursor.execute(query)
        resultado_query = cursor.fetchall()
        cursor.close()
        conn.close()
        print("<<<----------------------- UPDATE PAINEL FINALIZADO -- DB DESCONECTADO ----------------------->>>")
        return resultado_query
    except Exception as e:
        cursor.close()
        conn.close()
        print("<<<----------------------- ERRO -- DB DESCONECTADO ----------------------->>>")
        print(e)


def update_rankings(lista_rankings):
    print("atualização rankings ------------------------------------------")
    for i in range(len(lista_rankings)):
        print(lista_rankings[i])
    print("------------------------------------------")
    
    try:
        db = conexao_db_api()
        conn = db[0]
        cursor = db[1]
        print("----------------------------->>> DB CONECTADO")

        cont = 1
        for i in range(len(lista_rankings)):
            index_df = lista_rankings[i].index.values
            for j in index_df:
                ativo = lista_rankings[i]["ativo"][j]
                tt_analisado = lista_rankings[i]["tt analisado"][j]
                tt_acertos = lista_rankings[i]["tt win"][j]
                tt_erros = lista_rankings[i]["tt loss"][j]
                perc_win = lista_rankings[i]["perc win"][j]
                padrao = lista_rankings[i]["padrao"][j]

                cmd_update = f'UPDATE rank_paridades_v5 SET par = "{ativo}", tt_analisado = {tt_analisado}, acertos = {tt_acertos}, erros = {tt_erros}, perc_win = {perc_win}, padrao = "{padrao}" WHERE id = {cont}'
                cursor.execute(cmd_update)
                conn.commit()
                cont += 1
        cursor.close()
        conn.close()
        print("<<<----------------------- REGISTROS ATUALIZADOS -- DB DESCONECTADO ----------------------->>>")

    except Exception as e:
        cursor.close()
        conn.close()
        print("<<<----------------------- ERRO -- DB DESCONECTADO - UPDATE RANKING ----------------------->>>")
        print(e)
