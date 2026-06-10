class Estadio:
    """Representa a tabela Estadio do banco brasileirao2026."""

    def __init__(self, nome, cidade, estado, capacidade, id_estadio=None):
        self.id_estadio = id_estadio
        self.nome = nome
        self.cidade = cidade
        self.estado = estado
        self.capacidade = capacidade

    def __repr__(self):
        return (f"Estadio(id={self.id_estadio}, nome='{self.nome}', "
                f"cidade='{self.cidade}', estado='{self.estado}', "
                f"capacidade={self.capacidade})")
