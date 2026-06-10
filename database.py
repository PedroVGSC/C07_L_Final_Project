import mysql.connector
from mysql.connector import Error


class DatabaseManager:
    """Gerencia a conexao com o banco de dados MySQL.

    Responsavel apenas por abrir/fechar a conexao e executar queries.
    As operacoes especificas de cada tabela ficam nas classes DAO.
    """

    def __init__(self, host="127.0.0.1", user="root", password="root",
                 database="brasileirao2026"):
        self.host = host
        self.user = user
        self.password = password
        self.database = database
        self.conn = None
        self.cursor = None
        self.connect()

    def connect(self):
        """Estabelece conexao com o banco de dados MySQL."""
        try:
            self.conn = mysql.connector.connect(
                host=self.host,
                user=self.user,
                password=self.password,
                database=self.database
            )
            self.cursor = self.conn.cursor()
            print(f"Conectado ao MySQL: {self.database}")
        except Error as e:
            print(f"Erro de conexao: {e}")
            raise

    def close(self):
        """Fecha a conexao com o banco de dados."""
        if self.conn:
            self.cursor.close()
            self.conn.close()
            print("Conexao fechada")

    def execute(self, query, params=None):
        """Executa uma query de escrita (INSERT, UPDATE, DELETE) e confirma.

        Retorna o id gerado (lastrowid) e o numero de linhas afetadas.
        """
        self.cursor.execute(query, params or ())
        self.conn.commit()
        return self.cursor.lastrowid, self.cursor.rowcount

    def fetch_all(self, query, params=None):
        """Executa um SELECT e retorna todas as linhas."""
        self.cursor.execute(query, params or ())
        return self.cursor.fetchall()

    def fetch_one(self, query, params=None):
        """Executa um SELECT e retorna apenas a primeira linha."""
        self.cursor.execute(query, params or ())
        return self.cursor.fetchone()
