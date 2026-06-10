from models.partida import Partida


class PartidaDAO:
    """CRUD da tabela Partida."""

    def __init__(self, db):
        self.db = db

    def inserir(self, partida):
        """Insere uma nova partida (CREATE)."""
        query = """
            INSERT INTO Partida
                (data_partida, rodada, gols_mandante, gols_visitante,
                 id_clube_mandante, id_clube_visitante, id_estadio, id_temporada)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
        """
        params = (partida.data_partida, partida.rodada, partida.gols_mandante,
                  partida.gols_visitante, partida.id_clube_mandante,
                  partida.id_clube_visitante, partida.id_estadio,
                  partida.id_temporada)
        novo_id, _ = self.db.execute(query, params)
        partida.id_partida = novo_id
        return novo_id

    def listar_todos(self):
        """Retorna todas as partidas (READ)."""
        linhas = self.db.fetch_all("SELECT * FROM Partida ORDER BY id_partida")
        return [self._mapear(l) for l in linhas]

    def buscar_por_id(self, id_partida):
        """Retorna uma partida pelo id (READ)."""
        linha = self.db.fetch_one(
            "SELECT * FROM Partida WHERE id_partida = %s", (id_partida,)
        )
        return self._mapear(linha) if linha else None

    def buscar_por_rodada(self, rodada):
        """Busca partidas por atributo (rodada)."""
        linhas = self.db.fetch_all(
            "SELECT * FROM Partida WHERE rodada = %s ORDER BY data_partida",
            (rodada,)
        )
        return [self._mapear(l) for l in linhas]

    def atualizar(self, partida):
        """Atualiza uma partida existente (UPDATE)."""
        query = """
            UPDATE Partida
            SET data_partida = %s, rodada = %s, gols_mandante = %s,
                gols_visitante = %s, id_clube_mandante = %s,
                id_clube_visitante = %s, id_estadio = %s, id_temporada = %s
            WHERE id_partida = %s
        """
        params = (partida.data_partida, partida.rodada, partida.gols_mandante,
                  partida.gols_visitante, partida.id_clube_mandante,
                  partida.id_clube_visitante, partida.id_estadio,
                  partida.id_temporada, partida.id_partida)
        _, afetadas = self.db.execute(query, params)
        return afetadas

    def deletar(self, id_partida):
        """Remove uma partida (DELETE)."""
        _, afetadas = self.db.execute(
            "DELETE FROM Partida WHERE id_partida = %s", (id_partida,)
        )
        return afetadas

    # ----- Consultas com JOIN -----

    def listar_com_clubes_e_estadio(self):
        """SELECT com JOIN multiplo: partida + clubes (mandante/visitante) + estadio."""
        query = """
            SELECT
                p.id_partida,
                p.rodada,
                p.data_partida,
                cm.nome AS mandante,
                p.gols_mandante,
                p.gols_visitante,
                cv.nome AS visitante,
                e.nome  AS estadio
            FROM Partida p
            INNER JOIN Clube cm  ON p.id_clube_mandante  = cm.id_clube
            INNER JOIN Clube cv  ON p.id_clube_visitante = cv.id_clube
            LEFT  JOIN Estadio e ON p.id_estadio         = e.id_estadio
            ORDER BY p.rodada, p.data_partida
        """
        return self.db.fetch_all(query)

    @staticmethod
    def _mapear(linha):
        """Converte uma tupla do banco em um objeto Partida."""
        return Partida(
            id_partida=linha[0],
            data_partida=linha[1],
            rodada=linha[2],
            gols_mandante=linha[3],
            gols_visitante=linha[4],
            id_clube_mandante=linha[5],
            id_clube_visitante=linha[6],
            id_estadio=linha[7],
            id_temporada=linha[8],
        )
