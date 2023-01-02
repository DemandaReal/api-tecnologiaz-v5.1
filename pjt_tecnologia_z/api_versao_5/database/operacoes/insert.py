from api_versao_5.valores_globais import var_globais
from api_versao_5.database.conn.conn_db import conexao_db_api

def inserir_registro_database(dados):
    print("abertura operacao ------------------------------------------")
    print(dados)
    print("------------------------------------------")
    try:
        db = conexao_db_api()
        conn = db[0]
        cursor = db[1]
        print("----------------------------->>> DB CONECTADO")
        id_operacao = dados["id_operacao"]
        index_operacao = dados["index_operacao"]
        user_id = dados["user_id"]
        abertura = dados["abertura"]
        expiracao = dados["expiracao"]
        direcao = dados["direcao"]
        ativo = dados["ativo"]
        padrao = dados["padrao"]
        status_op = 1
        tipo_mercado = var_globais.TIPO_MERCADO
        
        query = f'SELECT * FROM operacoes_api WHERE id_operacao = "{id_operacao}"'
        cursor.execute(query)
        resultado = cursor.fetchall()
        print(f"TT REGISTROS DB: {len(resultado)}")
        
        if len(resultado) == 0:
            print(" -------------------INICIO PROCESSO INSERT DATABASE -------------------")
            cmd_insert = f'INSERT INTO operacoes_api (id_operacao, index_operacao, user_id, abertura, expiracao, direcao, par, padrao, status_op, tipo_mercado) VALUES ("{id_operacao}", "{index_operacao}", "{user_id}", "{abertura}", "{expiracao}", "{direcao}", "{ativo}", "{padrao}", {status_op}, "{tipo_mercado}")'
            cursor.execute(cmd_insert)
            conn.commit()
            cursor.close()
            conn.close()
            print("<<<----------------------- REGISTRO INSERIDO -- DB DESCONECTADO ----------------------->>>")
        else:
            cursor.close()
            conn.close()
            print("### Este registro já está inserido no banco de dados. ###")
            print("<<<----------------------- REGISTRO INSERIDO -- DB DESCONECTADO ----------------------->>>")
    except Exception as e:
        cursor.close()
        conn.close()
        print("<<<----------------------- ERRO -- DB DESCONECTADO ----------------------->>>")
        print(e)
