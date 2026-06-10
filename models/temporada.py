class Temporada:
    """Representa a tabela Temporada do banco brasileirao2026."""

    def __init__(self, ano, data_inicio=None, data_fim=None,
                 id_competicao=None, id_temporada=None):
        self.id_temporada = id_temporada
        self.ano = ano
        self.data_inicio = data_inicio
        self.data_fim = data_fim
        self.id_competicao = id_competicao

    def __repr__(self):
        return (f"Temporada(id={self.id_temporada}, ano={self.ano}, "
                f"data_inicio={self.data_inicio}, data_fim={self.data_fim}, "
                f"id_competicao={self.id_competicao})")
