class Partida:
    """Representa a tabela Partida do banco brasileirao2026."""

    def __init__(self, data_partida, rodada=None, gols_mandante=None,
                 gols_visitante=None, id_clube_mandante=None,
                 id_clube_visitante=None, id_estadio=None, id_temporada=None,
                 id_partida=None):
        self.id_partida = id_partida
        self.data_partida = data_partida
        self.rodada = rodada
        self.gols_mandante = gols_mandante
        self.gols_visitante = gols_visitante
        self.id_clube_mandante = id_clube_mandante
        self.id_clube_visitante = id_clube_visitante
        self.id_estadio = id_estadio
        self.id_temporada = id_temporada

    def __repr__(self):
        return (f"Partida(id={self.id_partida}, data={self.data_partida}, "
                f"rodada={self.rodada}, gols_mandante={self.gols_mandante}, "
                f"gols_visitante={self.gols_visitante}, "
                f"mandante={self.id_clube_mandante}, "
                f"visitante={self.id_clube_visitante}, "
                f"id_estadio={self.id_estadio}, id_temporada={self.id_temporada})")
