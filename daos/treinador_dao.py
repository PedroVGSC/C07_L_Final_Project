from models.treinador import Treinador


class TreinadorDAO:
    """CRUD da tabela Treinador."""

    def __init__(self, db):
        self.db = db

    def inserir(self, treinador):
        """Insere um novo treinador (CREATE)."""
        query = """
            INSERT INTO Treinador (nome, nacionalidade, idade)
            VALUES (%s, %s, %s)
        """
        params = (treinador.nome, treinador.nacionalidade, treinador.idade)
        novo_id, _ = self.db.execute(query, params)
        treinador.id_treinador = novo_id
        return novo_id

    def listar_todos(self):
        """Retorna todos os treinadores (READ)."""
        linhas = self.db.fetch_all("SELECT * FROM Treinador ORDER BY id_treinador")
        return [self._mapear(l) for l in linhas]

    def buscar_por_id(self, id_treinador):
        """Retorna um treinador pelo id (READ)."""
        linha = self.db.fetch_one(
            "SELECT * FROM Treinador WHERE id_treinador = %s", (id_treinador,)
        )
        return self._mapear(linha) if linha else None

    def buscar_por_nacionalidade(self, nacionalidade):
        """Busca treinadores por atributo (nacionalidade)."""
        linhas = self.db.fetch_all(
            "SELECT * FROM Treinador WHERE nacionalidade = %s ORDER BY nome",
            (nacionalidade,)
        )
        return [self._mapear(l) for l in linhas]

    def atualizar(self, treinador):
        """Atualiza um treinador existente (UPDATE)."""
        query = """
            UPDATE Treinador
            SET nome = %s, nacionalidade = %s, idade = %s
            WHERE id_treinador = %s
        """
        params = (treinador.nome, treinador.nacionalidade,
                  treinador.idade, treinador.id_treinador)
        _, afetadas = self.db.execute(query, params)
        return afetadas

    def deletar(self, id_treinador):
        """Remove um treinador (DELETE)."""
        _, afetadas = self.db.execute(
            "DELETE FROM Treinador WHERE id_treinador = %s", (id_treinador,)
        )
        return afetadas

    @staticmethod
    def _mapear(linha):
        """Converte uma tupla do banco em um objeto Treinador."""
        return Treinador(
            id_treinador=linha[0],
            nome=linha[1],
            nacionalidade=linha[2],
            idade=linha[3],
        )
