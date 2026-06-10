class Competicao:
    """Representa a tabela Competicao do banco brasileirao2026."""

    def __init__(self, nome, organizacao=None, id_competicao=None):
        self.id_competicao = id_competicao
        self.nome = nome
        self.organizacao = organizacao

    def __repr__(self):
        return (f"Competicao(id={self.id_competicao}, nome='{self.nome}', "
                f"organizacao='{self.organizacao}')")
