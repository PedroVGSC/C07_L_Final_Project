"""Pacote de Models do projeto Brasileirao 2026.

Cada classe Model representa uma tabela do banco de dados,
espelhando fielmente o esquema definido em main.sql.
"""

from models.estadio import Estadio
from models.treinador import Treinador
from models.clube import Clube
from models.jogador import Jogador
from models.competicao import Competicao
from models.temporada import Temporada
from models.participacao import Participacao
from models.partida import Partida

__all__ = [
    "Estadio",
    "Treinador",
    "Clube",
    "Jogador",
    "Competicao",
    "Temporada",
    "Participacao",
    "Partida",
]
