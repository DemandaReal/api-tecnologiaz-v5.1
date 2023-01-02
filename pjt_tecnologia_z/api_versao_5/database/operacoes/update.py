from api_versao_5.database.conn.conn_db import conexao_db_api

def atualizar_registro_database(id_operacao, resultado):
    print("fechamento operacao ------------------------------------------")
    print(id_operacao, resultado)
    print("------------------------------------------")
    
    try:
        db = conexao_db_api()
        conn = db[0]
        cursor = db[1]
        print("----------------------------->>> DB CONECTADO")
        query = f'SELECT * FROM operacoes_api WHERE id_operacao = "{id_operacao}"'
        cursor.execute(query)
        resultado_query = cursor.fetchall()
        print(f"TT REGISTROS DB: {len(resultado_query)}")
        
        if len(resultado_query) == 0:
            print(f"!! ERRO DB: ID {id_operacao} não foi encontrado na tabela para ser atualizado. DB Desconectado")
            cursor.close()
            conn.close()
        elif len(resultado_query) == 1:
            print(" -------------------INICIO PROCESSO UPDATE DATABASE -------------------")
            cmd_update = f'UPDATE operacoes_api SET status_op = {resultado} WHERE id_operacao = "{id_operacao}"'
            cursor.execute(cmd_update)
            conn.commit()
            cursor.close()
            conn.close()
            print("<<<----------------------- REGISTRO ATUALIZADO -- DB DESCONECTADO ----------------------->>>")
        else:
            print("### Identificado divergencias no banco de dados. Mais de um registro com o mesmo id_operacao encontrado. ###")
            cursor.close()
            conn.close()

    except Exception as e:
        cursor.close()
        conn.close()
        print("<<<----------------------- ERRO -- DB DESCONECTADO ----------------------->>>")
        print(e)
