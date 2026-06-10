"""Pacote de DAOs (Data Access Objects) do projeto Brasileirao 2026.

Cada DAO concentra o CRUD especifico de uma tabela, operando
sobre as classes Model correspondentes.
"""

from daos.estadio_dao import EstadioDAO
from daos.treinador_dao import TreinadorDAO
from daos.clube_dao import ClubeDAO
from daos.jogador_dao import JogadorDAO
from daos.competicao_dao import CompeticaoDAO
from daos.temporada_dao import TemporadaDAO
from daos.participacao_dao import ParticipacaoDAO
from daos.partida_dao import PartidaDAO

__all__ = [
    "EstadioDAO",
    "TreinadorDAO",
    "ClubeDAO",
    "JogadorDAO",
    "CompeticaoDAO",
    "TemporadaDAO",
    "ParticipacaoDAO",
    "PartidaDAO",
]
