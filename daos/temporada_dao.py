from models.temporada import Temporada


class TemporadaDAO:
    """CRUD da tabela Temporada."""

    def __init__(self, db):
        self.db = db

    def inserir(self, temporada):
        """Insere uma nova temporada (CREATE)."""
        query = """
            INSERT INTO Temporada (ano, data_inicio, data_fim, id_competicao)
            VALUES (%s, %s, %s, %s)
        """
        params = (temporada.ano, temporada.data_inicio,
                  temporada.data_fim, temporada.id_competicao)
        novo_id, _ = self.db.execute(query, params)
        temporada.id_temporada = novo_id
        return novo_id

    def listar_todos(self):
        """Retorna todas as temporadas (READ)."""
        linhas = self.db.fetch_all("SELECT * FROM Temporada ORDER BY id_temporada")
        return [self._mapear(l) for l in linhas]

    def buscar_por_id(self, id_temporada):
        """Retorna uma temporada pelo id (READ)."""
        linha = self.db.fetch_one(
            "SELECT * FROM Temporada WHERE id_temporada = %s", (id_temporada,)
        )
        return self._mapear(linha) if linha else None

    def buscar_por_ano(self, ano):
        """Busca temporadas por atributo (ano)."""
        linhas = self.db.fetch_all(
            "SELECT * FROM Temporada WHERE ano = %s ORDER BY id_temporada", (ano,)
        )
        return [self._mapear(l) for l in linhas]

    def atualizar(self, temporada):
        """Atualiza uma temporada existente (UPDATE)."""
        query = """
            UPDATE Temporada
            SET ano = %s, data_inicio = %s, data_fim = %s, id_competicao = %s
            WHERE id_temporada = %s
        """
        params = (temporada.ano, temporada.data_inicio, temporada.data_fim,
                  temporada.id_competicao, temporada.id_temporada)
        _, afetadas = self.db.execute(query, params)
        return afetadas

    def deletar(self, id_temporada):
        """Remove uma temporada (DELETE)."""
        _, afetadas = self.db.execute(
            "DELETE FROM Temporada WHERE id_temporada = %s", (id_temporada,)
        )
        return afetadas

    @staticmethod
    def _mapear(linha):
        """Converte uma tupla do banco em um objeto Temporada."""
        return Temporada(
            id_temporada=linha[0],
            ano=linha[1],
            data_inicio=linha[2],
            data_fim=linha[3],
            id_competicao=linha[4],
        )
