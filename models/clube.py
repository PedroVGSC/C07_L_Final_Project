class Clube:
    """Representa a tabela Clube do banco brasileirao2026."""

    def __init__(self, nome, sigla, fundacao=None, id_estadio=None,
                 id_treinador=None, id_clube=None):
        self.id_clube = id_clube
        self.nome = nome
        self.sigla = sigla
        self.fundacao = fundacao
        self.id_estadio = id_estadio
        self.id_treinador = id_treinador

    def __repr__(self):
        return (f"Clube(id={self.id_clube}, nome='{self.nome}', "
                f"sigla='{self.sigla}', fundacao={self.fundacao}, "
                f"id_estadio={self.id_estadio}, id_treinador={self.id_treinador})")
