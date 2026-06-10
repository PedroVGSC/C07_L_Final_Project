class Jogador:
    """Representa a tabela Jogador do banco brasileirao2026."""

    def __init__(self, nome, nacionalidade=None, idade=None, posicao=None,
                 numero_camisa=None, id_clube=None, id_jogador=None):
        self.id_jogador = id_jogador
        self.nome = nome
        self.nacionalidade = nacionalidade
        self.idade = idade
        self.posicao = posicao
        self.numero_camisa = numero_camisa
        self.id_clube = id_clube

    def __repr__(self):
        return (f"Jogador(id={self.id_jogador}, nome='{self.nome}', "
                f"nacionalidade='{self.nacionalidade}', idade={self.idade}, "
                f"posicao='{self.posicao}', numero_camisa={self.numero_camisa}, "
                f"id_clube={self.id_clube})")
