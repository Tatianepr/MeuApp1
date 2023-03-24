from sqlalchemy import Column, String, Integer, DateTime, ForeignKey
from datetime import datetime
from typing import Union

from  model import Base


class Comentario(Base):
    __tablename__ = 'comentario'

    id = Column(Integer, primary_key=True)
    autor = Column(String(4000))
    texto = Column(String(4000))
    n_estrelas = Column(Integer)
    data_insercao = Column(DateTime, default=datetime.now())

    # Definição do relacionamento entre o comentário e um produto.
    # Aqui está sendo definido a coluna 'produto' que vai guardar
    # a referencia ao produto, a chave estrangeira que relaciona
    # um produto ao comentário.
    produto = Column(Integer, ForeignKey("produto.pk_produto"), nullable=False)

    def __init__(self, autor: str, texto:str, n_estrelas: int, data_insercao:Union[DateTime, None] = None):
        """
        Cria um Comentário

        Arguments:
            texto: o texto de um comentário.
            data_insercao: data de quando o comentário foi feito ou inserido
                           à base
        """
        self.autor = autor
        self.texto = texto
        self.n_estrelas = n_estrelas
        if data_insercao:
            self.data_insercao = data_insercao
