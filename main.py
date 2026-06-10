"""
Brasileirao 2026 - Integracao Python + MySQL
=============================================

Menu interativo que permite realizar INSERT, UPDATE, DELETE e SELECT
em todas as tabelas do banco (alteracoes no backend visiveis no banco),
alem de buscas por atributo e consultas com JOIN.

Arquitetura:
    - config.py    -> credenciais de conexao
    - database.py  -> DatabaseManager (conexao/execucao)
    - models/      -> classes Model (uma por tabela)
    - daos/        -> classes DAO com o CRUD de cada tabela
    - main.py      -> menu de interacao com o usuario
"""

from config import MYSQL_CONFIG
from database import DatabaseManager

from models import (
    Estadio, Treinador, Clube, Jogador,
    Competicao, Temporada, Participacao, Partida,
)
from daos import (
    EstadioDAO, TreinadorDAO, ClubeDAO, JogadorDAO,
    CompeticaoDAO, TemporadaDAO, ParticipacaoDAO, PartidaDAO,
)


# ---------------------------------------------------------------------------
# Funcoes auxiliares de entrada
# ---------------------------------------------------------------------------

def ler_texto(rotulo, obrigatorio=True):
    """Le um texto do usuario. Se nao obrigatorio, ENTER vazio retorna None."""
    while True:
        valor = input(rotulo).strip()
        if valor:
            return valor
        if not obrigatorio:
            return None
        print("   ! Campo obrigatorio. Tente novamente.")


def ler_inteiro(rotulo, obrigatorio=True):
    """Le um numero inteiro. Se nao obrigatorio, ENTER vazio retorna None."""
    while True:
        valor = input(rotulo).strip()
        if not valor and not obrigatorio:
            return None
        try:
            return int(valor)
        except ValueError:
            print("   ! Digite um numero inteiro valido.")


def pausar():
    input("\nPressione ENTER para continuar...")


def imprimir_tabela(titulo, cabecalho, linhas):
    """Imprime uma lista de tuplas em formato de tabela alinhada."""
    print(f"\n=== {titulo} ===")
    if not linhas:
        print("(nenhum registro encontrado)")
        return

    colunas = list(zip(*([cabecalho] + [tuple(str(c) for c in l) for l in linhas])))
    larguras = [max(len(c) for c in coluna) for coluna in colunas]

    def formatar(valores):
        return " | ".join(str(v).ljust(larguras[i]) for i, v in enumerate(valores))

    print(formatar(cabecalho))
    print("-+-".join("-" * w for w in larguras))
    for l in linhas:
        print(formatar(tuple(str(c) for c in l)))
    print(f"\nTotal: {len(linhas)} registro(s)")


# ---------------------------------------------------------------------------
# Aplicacao principal
# ---------------------------------------------------------------------------

class Aplicacao:
    def __init__(self):
        self.db = DatabaseManager(**MYSQL_CONFIG)
        self.estadio_dao = EstadioDAO(self.db)
        self.treinador_dao = TreinadorDAO(self.db)
        self.clube_dao = ClubeDAO(self.db)
        self.jogador_dao = JogadorDAO(self.db)
        self.competicao_dao = CompeticaoDAO(self.db)
        self.temporada_dao = TemporadaDAO(self.db)
        self.participacao_dao = ParticipacaoDAO(self.db)
        self.partida_dao = PartidaDAO(self.db)

    # ---------------------- Menu principal ----------------------

    def executar(self):
        print("\n==============================================")
        print(" BRASILEIRAO 2026 - PYTHON + MYSQL ")
        print("==============================================")
        opcoes = {
            "1": ("Gerenciar Estadios", self.menu_estadio),
            "2": ("Gerenciar Treinadores", self.menu_treinador),
            "3": ("Gerenciar Clubes", self.menu_clube),
            "4": ("Gerenciar Jogadores", self.menu_jogador),
            "5": ("Gerenciar Competicoes", self.menu_competicao),
            "6": ("Gerenciar Temporadas", self.menu_temporada),
            "7": ("Gerenciar Participacoes", self.menu_participacao),
            "8": ("Gerenciar Partidas", self.menu_partida),
            "9": ("Consultas com JOIN", self.menu_joins),
            "10": ("Visualizar TODAS as tabelas (SELECT *)", self.mostrar_todas_tabelas),
            "0": ("Sair", None),
        }
        while True:
            print("\n========== MENU PRINCIPAL ==========")
            for chave, (rotulo, _) in opcoes.items():
                print(f"  {chave:>2}. {rotulo}")
            escolha = input("Escolha uma opcao: ").strip()

            if escolha == "0":
                break
            acao = opcoes.get(escolha)
            if acao:
                acao[1]()
            else:
                print("   ! Opcao invalida.")

        self.db.close()
        print("\nAplicacao encerrada. Ate logo!")

    @staticmethod
    def _menu_crud(titulo, acoes):
        """Exibe um submenu CRUD generico e despacha as acoes escolhidas.

        'acoes' e um dict: chave -> (rotulo, funcao). A opcao '0' volta.
        """
        while True:
            print(f"\n----- {titulo} -----")
            for chave, (rotulo, _) in acoes.items():
                print(f"  {chave}. {rotulo}")
            print("  0. Voltar")
            escolha = input("Escolha: ").strip()
            if escolha == "0":
                return
            acao = acoes.get(escolha)
            if acao:
                acao[1]()
                pausar()
            else:
                print("   ! Opcao invalida.")

    # ---------------------- ESTADIO ----------------------

    def menu_estadio(self):
        self._menu_crud("ESTADIOS", {
            "1": ("Inserir estadio", self._estadio_inserir),
            "2": ("Listar estadios", self._estadio_listar),
            "3": ("Buscar por estado (atributo)", self._estadio_buscar),
            "4": ("Atualizar estadio", self._estadio_atualizar),
            "5": ("Deletar estadio", self._estadio_deletar),
        })

    def _estadio_listar(self):
        linhas = [(e.id_estadio, e.nome, e.cidade, e.estado, e.capacidade)
                  for e in self.estadio_dao.listar_todos()]
        imprimir_tabela("Estadios", ("ID", "Nome", "Cidade", "UF", "Capacidade"), linhas)

    def _estadio_inserir(self):
        nome = ler_texto("Nome: ")
        cidade = ler_texto("Cidade: ")
        estado = ler_texto("Estado (UF, 2 letras): ")
        capacidade = ler_inteiro("Capacidade: ")
        novo_id = self.estadio_dao.inserir(Estadio(nome, cidade, estado, capacidade))
        print(f"   > Estadio inserido com id {novo_id}.")

    def _estadio_buscar(self):
        estado = ler_texto("Estado (UF) a buscar: ")
        linhas = [(e.id_estadio, e.nome, e.cidade, e.estado, e.capacidade)
                  for e in self.estadio_dao.buscar_por_estado(estado)]
        imprimir_tabela(f"Estadios em {estado}",
                        ("ID", "Nome", "Cidade", "UF", "Capacidade"), linhas)

    def _estadio_atualizar(self):
        id_estadio = ler_inteiro("ID do estadio a atualizar: ")
        atual = self.estadio_dao.buscar_por_id(id_estadio)
        if not atual:
            print("   ! Estadio nao encontrado.")
            return
        print(f"   Atual: {atual}")
        print("   (ENTER mantem o valor atual)")
        atual.nome = ler_texto(f"Nome [{atual.nome}]: ", obrigatorio=False) or atual.nome
        atual.cidade = ler_texto(f"Cidade [{atual.cidade}]: ", obrigatorio=False) or atual.cidade
        atual.estado = ler_texto(f"Estado [{atual.estado}]: ", obrigatorio=False) or atual.estado
        nova_cap = ler_inteiro(f"Capacidade [{atual.capacidade}]: ", obrigatorio=False)
        if nova_cap is not None:
            atual.capacidade = nova_cap
        self.estadio_dao.atualizar(atual)
        print("   > Estadio atualizado.")

    def _estadio_deletar(self):
        id_estadio = ler_inteiro("ID do estadio a deletar: ")
        if self.estadio_dao.deletar(id_estadio):
            print("   > Estadio deletado.")
        else:
            print("   ! Nenhum estadio deletado (id inexistente?).")

    # ---------------------- TREINADOR ----------------------

    def menu_treinador(self):
        self._menu_crud("TREINADORES", {
            "1": ("Inserir treinador", self._treinador_inserir),
            "2": ("Listar treinadores", self._treinador_listar),
            "3": ("Buscar por nacionalidade (atributo)", self._treinador_buscar),
            "4": ("Atualizar treinador", self._treinador_atualizar),
            "5": ("Deletar treinador", self._treinador_deletar),
        })

    def _treinador_listar(self):
        linhas = [(t.id_treinador, t.nome, t.nacionalidade, t.idade)
                  for t in self.treinador_dao.listar_todos()]
        imprimir_tabela("Treinadores", ("ID", "Nome", "Nacionalidade", "Idade"), linhas)

    def _treinador_inserir(self):
        nome = ler_texto("Nome: ")
        nac = ler_texto("Nacionalidade: ", obrigatorio=False)
        idade = ler_inteiro("Idade: ", obrigatorio=False)
        novo_id = self.treinador_dao.inserir(Treinador(nome, nac, idade))
        print(f"   > Treinador inserido com id {novo_id}.")

    def _treinador_buscar(self):
        nac = ler_texto("Nacionalidade a buscar: ")
        linhas = [(t.id_treinador, t.nome, t.nacionalidade, t.idade)
                  for t in self.treinador_dao.buscar_por_nacionalidade(nac)]
        imprimir_tabela(f"Treinadores ({nac})",
                        ("ID", "Nome", "Nacionalidade", "Idade"), linhas)

    def _treinador_atualizar(self):
        tid = ler_inteiro("ID do treinador a atualizar: ")
        atual = self.treinador_dao.buscar_por_id(tid)
        if not atual:
            print("   ! Treinador nao encontrado.")
            return
        print(f"   Atual: {atual}")
        atual.nome = ler_texto(f"Nome [{atual.nome}]: ", obrigatorio=False) or atual.nome
        nac = ler_texto(f"Nacionalidade [{atual.nacionalidade}]: ", obrigatorio=False)
        if nac is not None:
            atual.nacionalidade = nac
        idade = ler_inteiro(f"Idade [{atual.idade}]: ", obrigatorio=False)
        if idade is not None:
            atual.idade = idade
        self.treinador_dao.atualizar(atual)
        print("   > Treinador atualizado.")

    def _treinador_deletar(self):
        tid = ler_inteiro("ID do treinador a deletar: ")
        if self.treinador_dao.deletar(tid):
            print("   > Treinador deletado.")
        else:
            print("   ! Nenhum treinador deletado.")

    # ---------------------- CLUBE ----------------------

    def menu_clube(self):
        self._menu_crud("CLUBES", {
            "1": ("Inserir clube", self._clube_inserir),
            "2": ("Listar clubes", self._clube_listar),
            "3": ("Buscar por nome (atributo)", self._clube_buscar),
            "4": ("Atualizar clube", self._clube_atualizar),
            "5": ("Deletar clube", self._clube_deletar),
        })

    def _clube_listar(self):
        linhas = [(c.id_clube, c.nome, c.sigla, c.fundacao, c.id_estadio, c.id_treinador)
                  for c in self.clube_dao.listar_todos()]
        imprimir_tabela("Clubes",
                        ("ID", "Nome", "Sigla", "Fundacao", "id_estadio", "id_treinador"),
                        linhas)

    def _clube_inserir(self):
        nome = ler_texto("Nome: ")
        sigla = ler_texto("Sigla (3 letras): ")
        fundacao = ler_inteiro("Ano de fundacao: ", obrigatorio=False)
        id_estadio = ler_inteiro("ID do estadio: ", obrigatorio=False)
        id_treinador = ler_inteiro("ID do treinador: ", obrigatorio=False)
        novo_id = self.clube_dao.inserir(
            Clube(nome, sigla, fundacao, id_estadio, id_treinador))
        print(f"   > Clube inserido com id {novo_id}.")

    def _clube_buscar(self):
        nome = ler_texto("Nome (ou parte) a buscar: ")
        linhas = [(c.id_clube, c.nome, c.sigla, c.fundacao)
                  for c in self.clube_dao.buscar_por_nome(nome)]
        imprimir_tabela(f"Clubes contendo '{nome}'",
                        ("ID", "Nome", "Sigla", "Fundacao"), linhas)

    def _clube_atualizar(self):
        cid = ler_inteiro("ID do clube a atualizar: ")
        atual = self.clube_dao.buscar_por_id(cid)
        if not atual:
            print("   ! Clube nao encontrado.")
            return
        print(f"   Atual: {atual}")
        atual.nome = ler_texto(f"Nome [{atual.nome}]: ", obrigatorio=False) or atual.nome
        atual.sigla = ler_texto(f"Sigla [{atual.sigla}]: ", obrigatorio=False) or atual.sigla
        fund = ler_inteiro(f"Fundacao [{atual.fundacao}]: ", obrigatorio=False)
        if fund is not None:
            atual.fundacao = fund
        ide = ler_inteiro(f"id_estadio [{atual.id_estadio}]: ", obrigatorio=False)
        if ide is not None:
            atual.id_estadio = ide
        idt = ler_inteiro(f"id_treinador [{atual.id_treinador}]: ", obrigatorio=False)
        if idt is not None:
            atual.id_treinador = idt
        self.clube_dao.atualizar(atual)
        print("   > Clube atualizado.")

    def _clube_deletar(self):
        cid = ler_inteiro("ID do clube a deletar: ")
        if self.clube_dao.deletar(cid):
            print("   > Clube deletado.")
        else:
            print("   ! Nenhum clube deletado.")

    # ---------------------- JOGADOR ----------------------

    def menu_jogador(self):
        self._menu_crud("JOGADORES", {
            "1": ("Inserir jogador", self._jogador_inserir),
            "2": ("Listar jogadores", self._jogador_listar),
            "3": ("Buscar por nome (atributo)", self._jogador_buscar_nome),
            "4": ("Buscar por posicao (atributo)", self._jogador_buscar_posicao),
            "5": ("Atualizar jogador", self._jogador_atualizar),
            "6": ("Deletar jogador", self._jogador_deletar),
        })

    def _jogador_listar(self):
        linhas = [(j.id_jogador, j.nome, j.nacionalidade, j.idade,
                   j.posicao, j.numero_camisa, j.id_clube)
                  for j in self.jogador_dao.listar_todos()]
        imprimir_tabela("Jogadores",
                        ("ID", "Nome", "Nac.", "Idade", "Posicao", "Camisa", "id_clube"),
                        linhas)

    def _jogador_inserir(self):
        nome = ler_texto("Nome: ")
        nac = ler_texto("Nacionalidade: ", obrigatorio=False)
        idade = ler_inteiro("Idade: ", obrigatorio=False)
        posicao = ler_texto("Posicao: ", obrigatorio=False)
        camisa = ler_inteiro("Numero da camisa: ", obrigatorio=False)
        id_clube = ler_inteiro("ID do clube: ", obrigatorio=False)
        novo_id = self.jogador_dao.inserir(
            Jogador(nome, nac, idade, posicao, camisa, id_clube))
        print(f"   > Jogador inserido com id {novo_id}.")

    def _jogador_buscar_nome(self):
        nome = ler_texto("Nome (ou parte) a buscar: ")
        self._jogador_exibir(self.jogador_dao.buscar_por_nome(nome),
                             f"Jogadores contendo '{nome}'")

    def _jogador_buscar_posicao(self):
        posicao = ler_texto("Posicao a buscar: ")
        self._jogador_exibir(self.jogador_dao.buscar_por_posicao(posicao),
                             f"Jogadores na posicao '{posicao}'")

    def _jogador_exibir(self, jogadores, titulo):
        linhas = [(j.id_jogador, j.nome, j.nacionalidade, j.idade,
                   j.posicao, j.numero_camisa, j.id_clube) for j in jogadores]
        imprimir_tabela(titulo,
                        ("ID", "Nome", "Nac.", "Idade", "Posicao", "Camisa", "id_clube"),
                        linhas)

    def _jogador_atualizar(self):
        jid = ler_inteiro("ID do jogador a atualizar: ")
        atual = self.jogador_dao.buscar_por_id(jid)
        if not atual:
            print("   ! Jogador nao encontrado.")
            return
        print(f"   Atual: {atual}")
        atual.nome = ler_texto(f"Nome [{atual.nome}]: ", obrigatorio=False) or atual.nome
        nac = ler_texto(f"Nacionalidade [{atual.nacionalidade}]: ", obrigatorio=False)
        if nac is not None:
            atual.nacionalidade = nac
        idade = ler_inteiro(f"Idade [{atual.idade}]: ", obrigatorio=False)
        if idade is not None:
            atual.idade = idade
        pos = ler_texto(f"Posicao [{atual.posicao}]: ", obrigatorio=False)
        if pos is not None:
            atual.posicao = pos
        camisa = ler_inteiro(f"Camisa [{atual.numero_camisa}]: ", obrigatorio=False)
        if camisa is not None:
            atual.numero_camisa = camisa
        idc = ler_inteiro(f"id_clube [{atual.id_clube}]: ", obrigatorio=False)
        if idc is not None:
            atual.id_clube = idc
        self.jogador_dao.atualizar(atual)
        print("   > Jogador atualizado.")

    def _jogador_deletar(self):
        jid = ler_inteiro("ID do jogador a deletar: ")
        if self.jogador_dao.deletar(jid):
            print("   > Jogador deletado.")
        else:
            print("   ! Nenhum jogador deletado.")

    # ---------------------- COMPETICAO ----------------------

    def menu_competicao(self):
        self._menu_crud("COMPETICOES", {
            "1": ("Inserir competicao", self._competicao_inserir),
            "2": ("Listar competicoes", self._competicao_listar),
            "3": ("Buscar por nome (atributo)", self._competicao_buscar),
            "4": ("Atualizar competicao", self._competicao_atualizar),
            "5": ("Deletar competicao", self._competicao_deletar),
        })

    def _competicao_listar(self):
        linhas = [(c.id_competicao, c.nome, c.organizacao)
                  for c in self.competicao_dao.listar_todos()]
        imprimir_tabela("Competicoes", ("ID", "Nome", "Organizacao"), linhas)

    def _competicao_inserir(self):
        nome = ler_texto("Nome: ")
        org = ler_texto("Organizacao: ", obrigatorio=False)
        novo_id = self.competicao_dao.inserir(Competicao(nome, org))
        print(f"   > Competicao inserida com id {novo_id}.")

    def _competicao_buscar(self):
        nome = ler_texto("Nome (ou parte) a buscar: ")
        linhas = [(c.id_competicao, c.nome, c.organizacao)
                  for c in self.competicao_dao.buscar_por_nome(nome)]
        imprimir_tabela(f"Competicoes contendo '{nome}'",
                        ("ID", "Nome", "Organizacao"), linhas)

    def _competicao_atualizar(self):
        cid = ler_inteiro("ID da competicao a atualizar: ")
        atual = self.competicao_dao.buscar_por_id(cid)
        if not atual:
            print("   ! Competicao nao encontrada.")
            return
        print(f"   Atual: {atual}")
        atual.nome = ler_texto(f"Nome [{atual.nome}]: ", obrigatorio=False) or atual.nome
        org = ler_texto(f"Organizacao [{atual.organizacao}]: ", obrigatorio=False)
        if org is not None:
            atual.organizacao = org
        self.competicao_dao.atualizar(atual)
        print("   > Competicao atualizada.")

    def _competicao_deletar(self):
        cid = ler_inteiro("ID da competicao a deletar: ")
        if self.competicao_dao.deletar(cid):
            print("   > Competicao deletada.")
        else:
            print("   ! Nenhuma competicao deletada.")

    # ---------------------- TEMPORADA ----------------------

    def menu_temporada(self):
        self._menu_crud("TEMPORADAS", {
            "1": ("Inserir temporada", self._temporada_inserir),
            "2": ("Listar temporadas", self._temporada_listar),
            "3": ("Buscar por ano (atributo)", self._temporada_buscar),
            "4": ("Atualizar temporada", self._temporada_atualizar),
            "5": ("Deletar temporada", self._temporada_deletar),
        })

    def _temporada_listar(self):
        linhas = [(t.id_temporada, t.ano, t.data_inicio, t.data_fim, t.id_competicao)
                  for t in self.temporada_dao.listar_todos()]
        imprimir_tabela("Temporadas",
                        ("ID", "Ano", "Inicio", "Fim", "id_competicao"), linhas)

    def _temporada_inserir(self):
        ano = ler_inteiro("Ano: ")
        inicio = ler_texto("Data inicio (AAAA-MM-DD): ", obrigatorio=False)
        fim = ler_texto("Data fim (AAAA-MM-DD): ", obrigatorio=False)
        id_comp = ler_inteiro("ID da competicao: ", obrigatorio=False)
        novo_id = self.temporada_dao.inserir(Temporada(ano, inicio, fim, id_comp))
        print(f"   > Temporada inserida com id {novo_id}.")

    def _temporada_buscar(self):
        ano = ler_inteiro("Ano a buscar: ")
        linhas = [(t.id_temporada, t.ano, t.data_inicio, t.data_fim, t.id_competicao)
                  for t in self.temporada_dao.buscar_por_ano(ano)]
        imprimir_tabela(f"Temporadas do ano {ano}",
                        ("ID", "Ano", "Inicio", "Fim", "id_competicao"), linhas)

    def _temporada_atualizar(self):
        tid = ler_inteiro("ID da temporada a atualizar: ")
        atual = self.temporada_dao.buscar_por_id(tid)
        if not atual:
            print("   ! Temporada nao encontrada.")
            return
        print(f"   Atual: {atual}")
        ano = ler_inteiro(f"Ano [{atual.ano}]: ", obrigatorio=False)
        if ano is not None:
            atual.ano = ano
        ini = ler_texto(f"Inicio [{atual.data_inicio}]: ", obrigatorio=False)
        if ini is not None:
            atual.data_inicio = ini
        fim = ler_texto(f"Fim [{atual.data_fim}]: ", obrigatorio=False)
        if fim is not None:
            atual.data_fim = fim
        idc = ler_inteiro(f"id_competicao [{atual.id_competicao}]: ", obrigatorio=False)
        if idc is not None:
            atual.id_competicao = idc
        self.temporada_dao.atualizar(atual)
        print("   > Temporada atualizada.")

    def _temporada_deletar(self):
        tid = ler_inteiro("ID da temporada a deletar: ")
        if self.temporada_dao.deletar(tid):
            print("   > Temporada deletada.")
        else:
            print("   ! Nenhuma temporada deletada.")

    # ---------------------- PARTICIPACAO ----------------------

    def menu_participacao(self):
        self._menu_crud("PARTICIPACOES", {
            "1": ("Inserir participacao", self._participacao_inserir),
            "2": ("Listar participacoes", self._participacao_listar),
            "3": ("Buscar por clube (atributo)", self._participacao_buscar),
            "4": ("Atualizar participacao", self._participacao_atualizar),
            "5": ("Deletar participacao", self._participacao_deletar),
        })

    def _participacao_listar(self):
        linhas = [(p.id_participacao, p.id_clube, p.id_temporada, p.vitorias,
                   p.empates, p.derrotas, p.gols_pro, p.gols_contra)
                  for p in self.participacao_dao.listar_todos()]
        imprimir_tabela("Participacoes",
                        ("ID", "id_clube", "id_temp", "V", "E", "D", "GP", "GC"), linhas)

    def _participacao_inserir(self):
        id_clube = ler_inteiro("ID do clube: ")
        id_temp = ler_inteiro("ID da temporada: ")
        v = ler_inteiro("Vitorias: ", obrigatorio=False) or 0
        e = ler_inteiro("Empates: ", obrigatorio=False) or 0
        d = ler_inteiro("Derrotas: ", obrigatorio=False) or 0
        gp = ler_inteiro("Gols pro: ", obrigatorio=False) or 0
        gc = ler_inteiro("Gols contra: ", obrigatorio=False) or 0
        novo_id = self.participacao_dao.inserir(
            Participacao(id_clube, id_temp, v, e, d, gp, gc))
        print(f"   > Participacao inserida com id {novo_id}.")

    def _participacao_buscar(self):
        id_clube = ler_inteiro("ID do clube a buscar: ")
        linhas = [(p.id_participacao, p.id_clube, p.id_temporada, p.vitorias,
                   p.empates, p.derrotas, p.gols_pro, p.gols_contra)
                  for p in self.participacao_dao.buscar_por_clube(id_clube)]
        imprimir_tabela(f"Participacoes do clube {id_clube}",
                        ("ID", "id_clube", "id_temp", "V", "E", "D", "GP", "GC"), linhas)

    def _participacao_atualizar(self):
        pid = ler_inteiro("ID da participacao a atualizar: ")
        atual = self.participacao_dao.buscar_por_id(pid)
        if not atual:
            print("   ! Participacao nao encontrada.")
            return
        print(f"   Atual: {atual}")
        for campo, rotulo in [("vitorias", "Vitorias"), ("empates", "Empates"),
                              ("derrotas", "Derrotas"), ("gols_pro", "Gols pro"),
                              ("gols_contra", "Gols contra")]:
            atualv = getattr(atual, campo)
            novo = ler_inteiro(f"{rotulo} [{atualv}]: ", obrigatorio=False)
            if novo is not None:
                setattr(atual, campo, novo)
        self.participacao_dao.atualizar(atual)
        print("   > Participacao atualizada.")

    def _participacao_deletar(self):
        pid = ler_inteiro("ID da participacao a deletar: ")
        if self.participacao_dao.deletar(pid):
            print("   > Participacao deletada.")
        else:
            print("   ! Nenhuma participacao deletada.")

    # ---------------------- PARTIDA ----------------------

    def menu_partida(self):
        self._menu_crud("PARTIDAS", {
            "1": ("Inserir partida", self._partida_inserir),
            "2": ("Listar partidas", self._partida_listar),
            "3": ("Buscar por rodada (atributo)", self._partida_buscar),
            "4": ("Atualizar partida", self._partida_atualizar),
            "5": ("Deletar partida", self._partida_deletar),
        })

    def _partida_listar(self):
        linhas = [(p.id_partida, p.data_partida, p.rodada, p.gols_mandante,
                   p.gols_visitante, p.id_clube_mandante, p.id_clube_visitante,
                   p.id_estadio, p.id_temporada)
                  for p in self.partida_dao.listar_todos()]
        imprimir_tabela("Partidas",
                        ("ID", "Data", "Rod", "GM", "GV", "Mand", "Visit", "Estad", "Temp"),
                        linhas)

    def _partida_inserir(self):
        data = ler_texto("Data (AAAA-MM-DD): ")
        rodada = ler_inteiro("Rodada: ", obrigatorio=False)
        gm = ler_inteiro("Gols mandante: ", obrigatorio=False)
        gv = ler_inteiro("Gols visitante: ", obrigatorio=False)
        man = ler_inteiro("ID clube mandante: ", obrigatorio=False)
        vis = ler_inteiro("ID clube visitante: ", obrigatorio=False)
        est = ler_inteiro("ID estadio: ", obrigatorio=False)
        temp = ler_inteiro("ID temporada: ", obrigatorio=False)
        novo_id = self.partida_dao.inserir(
            Partida(data, rodada, gm, gv, man, vis, est, temp))
        print(f"   > Partida inserida com id {novo_id}.")

    def _partida_buscar(self):
        rodada = ler_inteiro("Rodada a buscar: ")
        linhas = [(p.id_partida, p.data_partida, p.rodada, p.gols_mandante,
                   p.gols_visitante, p.id_clube_mandante, p.id_clube_visitante)
                  for p in self.partida_dao.buscar_por_rodada(rodada)]
        imprimir_tabela(f"Partidas da rodada {rodada}",
                        ("ID", "Data", "Rod", "GM", "GV", "Mand", "Visit"), linhas)

    def _partida_atualizar(self):
        pid = ler_inteiro("ID da partida a atualizar: ")
        atual = self.partida_dao.buscar_por_id(pid)
        if not atual:
            print("   ! Partida nao encontrada.")
            return
        print(f"   Atual: {atual}")
        data = ler_texto(f"Data [{atual.data_partida}]: ", obrigatorio=False)
        if data is not None:
            atual.data_partida = data
        for campo, rotulo in [("rodada", "Rodada"),
                              ("gols_mandante", "Gols mandante"),
                              ("gols_visitante", "Gols visitante"),
                              ("id_clube_mandante", "id_clube_mandante"),
                              ("id_clube_visitante", "id_clube_visitante"),
                              ("id_estadio", "id_estadio"),
                              ("id_temporada", "id_temporada")]:
            atualv = getattr(atual, campo)
            novo = ler_inteiro(f"{rotulo} [{atualv}]: ", obrigatorio=False)
            if novo is not None:
                setattr(atual, campo, novo)
        self.partida_dao.atualizar(atual)
        print("   > Partida atualizada.")

    def _partida_deletar(self):
        pid = ler_inteiro("ID da partida a deletar: ")
        if self.partida_dao.deletar(pid):
            print("   > Partida deletada.")
        else:
            print("   ! Nenhuma partida deletada.")

    # ---------------------- CONSULTAS COM JOIN ----------------------

    def menu_joins(self):
        self._menu_crud("CONSULTAS COM JOIN", {
            "1": ("Jogadores + Clube (JOIN)", self._join_jogadores_clube),
            "2": ("Clubes + Estadio + Treinador (JOIN)", self._join_clube_estadio_treinador),
            "3": ("Partidas + Clubes + Estadio (JOIN)", self._join_partidas),
            "4": ("Classificacao (Participacao + Clube) (JOIN)", self._join_classificacao),
        })

    def _join_jogadores_clube(self):
        linhas = self.jogador_dao.listar_com_clube()
        imprimir_tabela("Jogadores e seus Clubes (JOIN)",
                        ("ID", "Jogador", "Posicao", "Camisa", "Clube"), linhas)

    def _join_clube_estadio_treinador(self):
        linhas = self.clube_dao.listar_com_estadio_e_treinador()
        imprimir_tabela("Clubes + Estadio + Treinador (JOIN)",
                        ("ID", "Clube", "Sigla", "Estadio", "Cidade", "Treinador"),
                        linhas)

    def _join_partidas(self):
        linhas = self.partida_dao.listar_com_clubes_e_estadio()
        imprimir_tabela("Partidas + Clubes + Estadio (JOIN)",
                        ("ID", "Rod", "Data", "Mandante", "GM", "GV", "Visitante", "Estadio"),
                        linhas)

    def _join_classificacao(self):
        linhas = self.participacao_dao.classificacao()
        imprimir_tabela("Classificacao (JOIN)",
                        ("Clube", "Pts", "V", "E", "D", "GP", "GC", "Saldo"), linhas)

    # ---------------------- SELECT * EM TODAS AS TABELAS ----------------------

    def mostrar_todas_tabelas(self):
        """SELECT * em cada tabela, para registrar as mudancas no banco."""
        print("\n##################################################")
        print("#   ESTADO ATUAL DE TODAS AS TABELAS (SELECT *)  #")
        print("##################################################")
        self._estadio_listar()
        self._treinador_listar()
        self._clube_listar()
        self._jogador_listar()
        self._competicao_listar()
        self._temporada_listar()
        self._participacao_listar()
        self._partida_listar()
        pausar()


def main():
    try:
        app = Aplicacao()
    except Exception as e:
        print(f"\nNao foi possivel iniciar a aplicacao: {e}")
        print("Verifique se o MySQL esta ativo e se o script main.sql foi executado.")
        return
    app.executar()


if __name__ == "__main__":
    main()
