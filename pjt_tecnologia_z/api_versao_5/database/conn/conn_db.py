import mysql.connector
import config_database


def conexao_db_api():
    conn = mysql.connector.connect(
        host = config_database.HOST_DB,
        user= config_database.USER_DB,
        password = config_database.PASSWORD_DB,
        database = config_database.NAME_DB,
        port = config_database.PORT_DB
    )
    cursor = conn.cursor()
    return [conn, cursor]
