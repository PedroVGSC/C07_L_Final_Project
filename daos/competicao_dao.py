from models.competicao import Competicao


class CompeticaoDAO:
    """CRUD da tabela Competicao."""

    def __init__(self, db):
        self.db = db

    def inserir(self, competicao):
        """Insere uma nova competicao (CREATE)."""
        query = "INSERT INTO Competicao (nome, organizacao) VALUES (%s, %s)"
        params = (competicao.nome, competicao.organizacao)
        novo_id, _ = self.db.execute(query, params)
        competicao.id_competicao = novo_id
        return novo_id

    def listar_todos(self):
        """Retorna todas as competicoes (READ)."""
        linhas = self.db.fetch_all("SELECT * FROM Competicao ORDER BY id_competicao")
        return [self._mapear(l) for l in linhas]

    def buscar_por_id(self, id_competicao):
        """Retorna uma competicao pelo id (READ)."""
        linha = self.db.fetch_one(
            "SELECT * FROM Competicao WHERE id_competicao = %s", (id_competicao,)
        )
        return self._mapear(linha) if linha else None

    def buscar_por_nome(self, nome):
        """Busca competicoes por atributo (nome, parcial)."""
        linhas = self.db.fetch_all(
            "SELECT * FROM Competicao WHERE LOWER(nome) LIKE LOWER(%s) ORDER BY nome",
            (f"%{nome}%",)
        )
        return [self._mapear(l) for l in linhas]

    def atualizar(self, competicao):
        """Atualiza uma competicao existente (UPDATE)."""
        query = """
            UPDATE Competicao
            SET nome = %s, organizacao = %s
            WHERE id_competicao = %s
        """
        params = (competicao.nome, competicao.organizacao, competicao.id_competicao)
        _, afetadas = self.db.execute(query, params)
        return afetadas

    def deletar(self, id_competicao):
        """Remove uma competicao (DELETE)."""
        _, afetadas = self.db.execute(
            "DELETE FROM Competicao WHERE id_competicao = %s", (id_competicao,)
        )
        return afetadas

    @staticmethod
    def _mapear(linha):
        """Converte uma tupla do banco em um objeto Competicao."""
        return Competicao(
            id_competicao=linha[0],
            nome=linha[1],
            organizacao=linha[2],
        )
