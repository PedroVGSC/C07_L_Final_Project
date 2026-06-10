class Treinador:
    """Representa a tabela Treinador do banco brasileirao2026."""

    def __init__(self, nome, nacionalidade=None, idade=None, id_treinador=None):
        self.id_treinador = id_treinador
        self.nome = nome
        self.nacionalidade = nacionalidade
        self.idade = idade

    def __repr__(self):
        return (f"Treinador(id={self.id_treinador}, nome='{self.nome}', "
                f"nacionalidade='{self.nacionalidade}', idade={self.idade})")
