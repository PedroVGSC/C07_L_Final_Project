from models.jogador import Jogador


class JogadorDAO:
    """CRUD da tabela Jogador."""

    def __init__(self, db):
        self.db = db

    def inserir(self, jogador):
        """Insere um novo jogador (CREATE)."""
        query = """
            INSERT INTO Jogador
                (nome, nacionalidade, idade, posicao, numero_camisa, id_clube)
            VALUES (%s, %s, %s, %s, %s, %s)
        """
        params = (jogador.nome, jogador.nacionalidade, jogador.idade,
                  jogador.posicao, jogador.numero_camisa, jogador.id_clube)
        novo_id, _ = self.db.execute(query, params)
        jogador.id_jogador = novo_id
        return novo_id

    def listar_todos(self):
        """Retorna todos os jogadores (READ)."""
        linhas = self.db.fetch_all("SELECT * FROM Jogador ORDER BY id_jogador")
        return [self._mapear(l) for l in linhas]

    def buscar_por_id(self, id_jogador):
        """Retorna um jogador pelo id (READ)."""
        linha = self.db.fetch_one(
            "SELECT * FROM Jogador WHERE id_jogador = %s", (id_jogador,)
        )
        return self._mapear(linha) if linha else None

    def buscar_por_nome(self, nome):
        """Busca jogadores por atributo (nome, parcial e sem distincao de caixa)."""
        linhas = self.db.fetch_all(
            "SELECT * FROM Jogador WHERE LOWER(nome) LIKE LOWER(%s) ORDER BY nome",
            (f"%{nome}%",)
        )
        return [self._mapear(l) for l in linhas]

    def buscar_por_posicao(self, posicao):
        """Busca jogadores por atributo (posicao)."""
        linhas = self.db.fetch_all(
            "SELECT * FROM Jogador WHERE posicao = %s ORDER BY nome", (posicao,)
        )
        return [self._mapear(l) for l in linhas]

    def atualizar(self, jogador):
        """Atualiza um jogador existente (UPDATE)."""
        query = """
            UPDATE Jogador
            SET nome = %s, nacionalidade = %s, idade = %s,
                posicao = %s, numero_camisa = %s, id_clube = %s
            WHERE id_jogador = %s
        """
        params = (jogador.nome, jogador.nacionalidade, jogador.idade,
                  jogador.posicao, jogador.numero_camisa, jogador.id_clube,
                  jogador.id_jogador)
        _, afetadas = self.db.execute(query, params)
        return afetadas

    def deletar(self, id_jogador):
        """Remove um jogador (DELETE)."""
        _, afetadas = self.db.execute(
            "DELETE FROM Jogador WHERE id_jogador = %s", (id_jogador,)
        )
        return afetadas

    # ----- Consultas com JOIN -----

    def listar_com_clube(self):
        """SELECT com JOIN: jogador + clube."""
        query = """
            SELECT
                j.id_jogador,
                j.nome          AS jogador,
                j.posicao,
                j.numero_camisa,
                c.nome          AS clube
            FROM Jogador j
            INNER JOIN Clube c ON j.id_clube = c.id_clube
            ORDER BY c.nome, j.nome
        """
        return self.db.fetch_all(query)

    @staticmethod
    def _mapear(linha):
        """Converte uma tupla do banco em um objeto Jogador."""
        return Jogador(
            id_jogador=linha[0],
            nome=linha[1],
            nacionalidade=linha[2],
            idade=linha[3],
            posicao=linha[4],
            numero_camisa=linha[5],
            id_clube=linha[6],
        )
