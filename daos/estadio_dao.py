from models.estadio import Estadio


class EstadioDAO:
    """CRUD da tabela Estadio."""

    def __init__(self, db):
        self.db = db

    def inserir(self, estadio):
        """Insere um novo estadio (CREATE)."""
        query = """
            INSERT INTO Estadio (nome, cidade, estado, capacidade)
            VALUES (%s, %s, %s, %s)
        """
        params = (estadio.nome, estadio.cidade, estadio.estado, estadio.capacidade)
        novo_id, _ = self.db.execute(query, params)
        estadio.id_estadio = novo_id
        return novo_id

    def listar_todos(self):
        """Retorna todos os estadios (READ)."""
        linhas = self.db.fetch_all("SELECT * FROM Estadio ORDER BY id_estadio")
        return [self._mapear(l) for l in linhas]

    def buscar_por_id(self, id_estadio):
        """Retorna um estadio pelo id (READ)."""
        linha = self.db.fetch_one(
            "SELECT * FROM Estadio WHERE id_estadio = %s", (id_estadio,)
        )
        return self._mapear(linha) if linha else None

    def buscar_por_estado(self, estado):
        """Busca estadios por atributo (estado)."""
        linhas = self.db.fetch_all(
            "SELECT * FROM Estadio WHERE estado = %s ORDER BY capacidade DESC",
            (estado,)
        )
        return [self._mapear(l) for l in linhas]

    def atualizar(self, estadio):
        """Atualiza um estadio existente (UPDATE)."""
        query = """
            UPDATE Estadio
            SET nome = %s, cidade = %s, estado = %s, capacidade = %s
            WHERE id_estadio = %s
        """
        params = (estadio.nome, estadio.cidade, estadio.estado,
                  estadio.capacidade, estadio.id_estadio)
        _, afetadas = self.db.execute(query, params)
        return afetadas

    def deletar(self, id_estadio):
        """Remove um estadio (DELETE)."""
        _, afetadas = self.db.execute(
            "DELETE FROM Estadio WHERE id_estadio = %s", (id_estadio,)
        )
        return afetadas

    @staticmethod
    def _mapear(linha):
        """Converte uma tupla do banco em um objeto Estadio."""
        return Estadio(
            id_estadio=linha[0],
            nome=linha[1],
            cidade=linha[2],
            estado=linha[3],
            capacidade=linha[4],
        )
