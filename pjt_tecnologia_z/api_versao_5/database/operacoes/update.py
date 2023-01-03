from time import sleep
from api_versao_5.database.conn.conn_db import conexao_db_api
from api_versao_5.processamento.processar_query_rank_paridades import atualizar_rank_paridades

def atualizar_registro_database(df_resultados):
    print("fechamento operacao ------------------------------------------")
    print(df_resultados)
    print("------------------------------------------")
    
    try:
        db = conexao_db_api()
        conn = db[0]
        cursor = db[1]
    
        for i in range(len(df_resultados)):
            print("----------------------------->>> DB CONECTADO")
            id_operacao = df_resultados["id_operacao"][i]
            resultado_op = df_resultados["resultado"][i]

            try:
                cmd_update = f'UPDATE operacoes_api SET status_op = {resultado_op} WHERE id_operacao = "{id_operacao}"'
                cursor.execute(cmd_update)
                conn.commit()
                print("<<<----------------------- REGISTRO ATUALIZADO ----------------------->>>")
            except Exception as e:
                print("### Identificado divergencias no banco de dados. ###")
                print(e)
                cursor.close()
                conn.close()

        print("<<<----------------------- TODOS OS REGISTRO FORAM ATUALIZADOS -- DB DESCONECTADO ----------------------->>>")
        try:
            print("FUNÇÃO ATUALIZAR RANK PARIDADES ACIONADA ------------------->>>>")
            atualizar_rank_paridades(conexao=conn, cursor_db=cursor)
        except Exception as e:
            print(e)

    except Exception as e:
        cursor.close()
        conn.close()
        print("<<<----------------------- ERRO -- DB DESCONECTADO ----------------------->>>")
        print(e)
