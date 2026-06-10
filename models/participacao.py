class Participacao:
    """Representa a tabela Participacao do banco brasileirao2026."""

    def __init__(self, id_clube, id_temporada, vitorias=0, empates=0,
                 derrotas=0, gols_pro=0, gols_contra=0, id_participacao=None):
        self.id_participacao = id_participacao
        self.id_clube = id_clube
        self.id_temporada = id_temporada
        self.vitorias = vitorias
        self.empates = empates
        self.derrotas = derrotas
        self.gols_pro = gols_pro
        self.gols_contra = gols_contra

    def __repr__(self):
        return (f"Participacao(id={self.id_participacao}, id_clube={self.id_clube}, "
                f"id_temporada={self.id_temporada}, vitorias={self.vitorias}, "
                f"empates={self.empates}, derrotas={self.derrotas}, "
                f"gols_pro={self.gols_pro}, gols_contra={self.gols_contra})")
