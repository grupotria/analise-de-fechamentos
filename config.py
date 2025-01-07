from urllib.parse import quote

SECRET_KEY = "Grupo Tria - 024 - Xx170554@"

SQLALCHEMY_DATABASE_URI = '{SGBD}://{usuario}:{senha}@{servidor}/{database}'.format(
        SGBD = 'mysql+mysqlconnector',
        usuario = 'root',
        senha = quote('Xx0806@#'),
        servidor = 'localhost',
        database = 'analise_de_fechamento'
    )