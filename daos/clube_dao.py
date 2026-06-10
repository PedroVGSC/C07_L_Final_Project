from models.clube import Clube


class ClubeDAO:
    """CRUD da tabela Clube."""

    def __init__(self, db):
        self.db = db

    def inserir(self, clube):
        """Insere um novo clube (CREATE)."""
        query = """
            INSERT INTO Clube (nome, sigla, fundacao, id_estadio, id_treinador)
            VALUES (%s, %s, %s, %s, %s)
        """
        params = (clube.nome, clube.sigla, clube.fundacao,
                  clube.id_estadio, clube.id_treinador)
        novo_id, _ = self.db.execute(query, params)
        clube.id_clube = novo_id
        return novo_id

    def listar_todos(self):
        """Retorna todos os clubes (READ)."""
        linhas = self.db.fetch_all("SELECT * FROM Clube ORDER BY id_clube")
        return [self._mapear(l) for l in linhas]

    def buscar_por_id(self, id_clube):
        """Retorna um clube pelo id (READ)."""
        linha = self.db.fetch_one(
            "SELECT * FROM Clube WHERE id_clube = %s", (id_clube,)
        )
        return self._mapear(linha) if linha else None

    def buscar_por_nome(self, nome):
        """Busca clubes por atributo (nome, parcial e sem distincao de caixa)."""
        linhas = self.db.fetch_all(
            "SELECT * FROM Clube WHERE LOWER(nome) LIKE LOWER(%s) ORDER BY nome",
            (f"%{nome}%",)
        )
        return [self._mapear(l) for l in linhas]

    def atualizar(self, clube):
        """Atualiza um clube existente (UPDATE)."""
        query = """
            UPDATE Clube
            SET nome = %s, sigla = %s, fundacao = %s,
                id_estadio = %s, id_treinador = %s
            WHERE id_clube = %s
        """
        params = (clube.nome, clube.sigla, clube.fundacao,
                  clube.id_estadio, clube.id_treinador, clube.id_clube)
        _, afetadas = self.db.execute(query, params)
        return afetadas

    def deletar(self, id_clube):
        """Remove um clube (DELETE)."""
        _, afetadas = self.db.execute(
            "DELETE FROM Clube WHERE id_clube = %s", (id_clube,)
        )
        return afetadas

    # ----- Consultas com JOIN -----

    def listar_com_estadio_e_treinador(self):
        """SELECT com JOIN: clube + estadio + treinador."""
        query = """
            SELECT
                c.id_clube,
                c.nome        AS clube,
                c.sigla,
                e.nome        AS estadio,
                e.cidade,
                t.nome        AS treinador
            FROM Clube c
            LEFT JOIN Estadio e   ON c.id_estadio   = e.id_estadio
            LEFT JOIN Treinador t ON c.id_treinador = t.id_treinador
            ORDER BY c.nome
        """
        return self.db.fetch_all(query)

    @staticmethod
    def _mapear(linha):
        """Converte uma tupla do banco em um objeto Clube."""
        return Clube(
            id_clube=linha[0],
            nome=linha[1],
            sigla=linha[2],
            fundacao=linha[3],
            id_estadio=linha[4],
            id_treinador=linha[5],
        )
