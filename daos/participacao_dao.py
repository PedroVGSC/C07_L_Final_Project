from models.participacao import Participacao


class ParticipacaoDAO:
    """CRUD da tabela Participacao."""

    def __init__(self, db):
        self.db = db

    def inserir(self, participacao):
        """Insere uma nova participacao (CREATE)."""
        query = """
            INSERT INTO Participacao
                (id_clube, id_temporada, vitorias, empates, derrotas,
                 gols_pro, gols_contra)
            VALUES (%s, %s, %s, %s, %s, %s, %s)
        """
        params = (participacao.id_clube, participacao.id_temporada,
                  participacao.vitorias, participacao.empates,
                  participacao.derrotas, participacao.gols_pro,
                  participacao.gols_contra)
        novo_id, _ = self.db.execute(query, params)
        participacao.id_participacao = novo_id
        return novo_id

    def listar_todos(self):
        """Retorna todas as participacoes (READ)."""
        linhas = self.db.fetch_all(
            "SELECT * FROM Participacao ORDER BY id_participacao"
        )
        return [self._mapear(l) for l in linhas]

    def buscar_por_id(self, id_participacao):
        """Retorna uma participacao pelo id (READ)."""
        linha = self.db.fetch_one(
            "SELECT * FROM Participacao WHERE id_participacao = %s",
            (id_participacao,)
        )
        return self._mapear(linha) if linha else None

    def buscar_por_clube(self, id_clube):
        """Busca participacoes por atributo (id_clube)."""
        linhas = self.db.fetch_all(
            "SELECT * FROM Participacao WHERE id_clube = %s ORDER BY id_temporada",
            (id_clube,)
        )
        return [self._mapear(l) for l in linhas]

    def atualizar(self, participacao):
        """Atualiza uma participacao existente (UPDATE)."""
        query = """
            UPDATE Participacao
            SET id_clube = %s, id_temporada = %s, vitorias = %s, empates = %s,
                derrotas = %s, gols_pro = %s, gols_contra = %s
            WHERE id_participacao = %s
        """
        params = (participacao.id_clube, participacao.id_temporada,
                  participacao.vitorias, participacao.empates,
                  participacao.derrotas, participacao.gols_pro,
                  participacao.gols_contra, participacao.id_participacao)
        _, afetadas = self.db.execute(query, params)
        return afetadas

    def deletar(self, id_participacao):
        """Remove uma participacao (DELETE)."""
        _, afetadas = self.db.execute(
            "DELETE FROM Participacao WHERE id_participacao = %s", (id_participacao,)
        )
        return afetadas

    # ----- Consultas com JOIN -----

    def classificacao(self):
        """SELECT com JOIN: classificacao (Participacao + Clube)."""
        query = """
            SELECT
                c.nome AS clube,
                (p.vitorias * 3) + p.empates AS pontos,
                p.vitorias,
                p.empates,
                p.derrotas,
                p.gols_pro,
                p.gols_contra,
                (p.gols_pro - p.gols_contra) AS saldo
            FROM Participacao p
            INNER JOIN Clube c ON p.id_clube = c.id_clube
            ORDER BY pontos DESC, saldo DESC
        """
        return self.db.fetch_all(query)

    @staticmethod
    def _mapear(linha):
        """Converte uma tupla do banco em um objeto Participacao."""
        return Participacao(
            id_participacao=linha[0],
            id_clube=linha[1],
            id_temporada=linha[2],
            vitorias=linha[3],
            empates=linha[4],
            derrotas=linha[5],
            gols_pro=linha[6],
            gols_contra=linha[7],
        )
