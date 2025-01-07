from main import db

class Funcionario(db.Model):
    __tablename__ = 'funcionario'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nome = db.Column(db.String(100), nullable=False)
    senha = db.Column(db.TEXT, nullable=False)
    funcao = db.Column(db.String(45), nullable=False)

    # empresas = db.relationship('Empresa', secondary='acesso', back_populates='usuario')
