import mysql.connector 
from mysql.connector import errorcode

def connect_db():
    """Função para conectar ao banco de dados."""
    try:
        conn = mysql.connector.connect(
            host='127.0.0.1',
            user='root',
            password='Xx0806@#',
            database='analise_de_fechamento'  # Conectar diretamente à base de dados desejada
        )
        return conn
    except mysql.connector.Error as err:
        if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
            print('Existe algo errado no nome de usuário ou senha')
        else:
            print(err)
