DROP DATABASE IF EXISTS brasileirao2026;
CREATE DATABASE brasileirao2026;
USE brasileirao2026;

CREATE TABLE Estadio (
    id_estadio INT AUTO_INCREMENT PRIMARY KEY,
    nome VARCHAR(100) NOT NULL,
    cidade VARCHAR(100) NOT NULL,
    estado CHAR(2) NOT NULL,
    capacidade INT NOT NULL
);

CREATE TABLE Treinador (
    id_treinador INT AUTO_INCREMENT PRIMARY KEY,
    nome VARCHAR(100) NOT NULL,
    nacionalidade VARCHAR(50),
    idade INT
);

CREATE TABLE Clube (
    id_clube INT AUTO_INCREMENT PRIMARY KEY,
    nome VARCHAR(100) NOT NULL,
    sigla CHAR(3) NOT NULL,
    fundacao INT,
    id_estadio INT,
    id_treinador INT,

    CONSTRAINT fk_clube_estadio
        FOREIGN KEY (id_estadio)
        REFERENCES Estadio(id_estadio),

    CONSTRAINT fk_clube_treinador
        FOREIGN KEY (id_treinador)
        REFERENCES Treinador(id_treinador)
);

CREATE TABLE Jogador (
    id_jogador INT AUTO_INCREMENT PRIMARY KEY,
    nome VARCHAR(100) NOT NULL,
    nacionalidade VARCHAR(50),
    idade INT,
    posicao VARCHAR(30),
    numero_camisa INT,
    id_clube INT,

    CONSTRAINT fk_jogador_clube
        FOREIGN KEY (id_clube)
        REFERENCES Clube(id_clube)
);

CREATE TABLE Competicao (
    id_competicao INT AUTO_INCREMENT PRIMARY KEY,
    nome VARCHAR(100) NOT NULL,
    organizacao VARCHAR(100)
);

CREATE TABLE Temporada (
    id_temporada INT AUTO_INCREMENT PRIMARY KEY,
    ano YEAR NOT NULL,
    data_inicio DATE,
    data_fim DATE,
    id_competicao INT,

    CONSTRAINT fk_temporada_competicao
        FOREIGN KEY (id_competicao)
        REFERENCES Competicao(id_competicao)
);

CREATE TABLE Participacao (
    id_participacao INT AUTO_INCREMENT PRIMARY KEY,
    id_clube INT,
    id_temporada INT,
    vitorias INT DEFAULT 0,
    empates INT DEFAULT 0,
    derrotas INT DEFAULT 0,
    gols_pro INT DEFAULT 0,
    gols_contra INT DEFAULT 0,

    CONSTRAINT fk_participacao_clube
        FOREIGN KEY (id_clube)
        REFERENCES Clube(id_clube),

    CONSTRAINT fk_participacao_temporada
        FOREIGN KEY (id_temporada)
        REFERENCES Temporada(id_temporada)
);

CREATE TABLE Partida (
    id_partida INT AUTO_INCREMENT PRIMARY KEY,
    data_partida DATE NOT NULL,
    rodada INT,
    gols_mandante INT,
    gols_visitante INT,

    id_clube_mandante INT,
    id_clube_visitante INT,
    id_estadio INT,
    id_temporada INT,

    CONSTRAINT fk_partida_mandante
        FOREIGN KEY (id_clube_mandante)
        REFERENCES Clube(id_clube),

    CONSTRAINT fk_partida_visitante
        FOREIGN KEY (id_clube_visitante)
        REFERENCES Clube(id_clube),

    CONSTRAINT fk_partida_estadio
        FOREIGN KEY (id_estadio)
        REFERENCES Estadio(id_estadio),

    CONSTRAINT fk_partida_temporada
        FOREIGN KEY (id_temporada)
        REFERENCES Temporada(id_temporada)
);

INSERT INTO Estadio (nome, cidade, estado, capacidade) VALUES
('Maracanã', 'Rio de Janeiro', 'RJ', 78838),
('Allianz Parque', 'São Paulo', 'SP', 43713),
('Neo Química Arena', 'São Paulo', 'SP', 49205),
('Mineirão', 'Belo Horizonte', 'MG', 61846),
('Arena do Grêmio', 'Porto Alegre', 'RS', 55662),
('Beira-Rio', 'Porto Alegre', 'RS', 50128),
('São Januário', 'Rio de Janeiro', 'RJ', 21880),
('Vila Belmiro', 'Santos', 'SP', 16068),
('Casa de Apostas Arena Fonte Nova', 'Salvador', 'BA', 47907),
('Ligga Arena', 'Curitiba', 'PR', 42372);

INSERT INTO Treinador (nome, nacionalidade, idade) VALUES
('Leonardo Jardim', 'Portugal', 51),
('Abel Ferreira', 'Portugal', 47),
('Fernando Diniz', 'Brasil', 52),
('Artur Jorge', 'Portugal', 54),
('Luís Castro', 'Portugal', 64),
('Paulo Pezzolano', 'Uruguai', 43),
('Renato Gaúcho', 'Brasil', 63),
('Cuca', 'Brasil', 60),
('Rogério Ceni', 'Brasil', 53),
('Odair Hellmann', 'Brasil', 49);

INSERT INTO Clube (nome, sigla, fundacao, id_estadio, id_treinador) VALUES
('Flamengo', 'FLA', 1895, 1, 1),
('Palmeiras', 'PAL', 1914, 2, 2),
('Corinthians', 'COR', 1910, 3, 3),
('Cruzeiro', 'CRU', 1921, 4, 4),
('Grêmio', 'GRE', 1903, 5, 5),
('Internacional', 'INT', 1909, 6, 6),
('Vasco da Gama', 'VAS', 1898, 7, 7),
('Santos', 'SAN', 1912, 8, 8),
('Bahia', 'BAH', 1931, 9, 9),
('Athletico Paranaense', 'CAP', 1924, 10, 10);

INSERT INTO Jogador (nome, nacionalidade, idade, posicao, numero_camisa, id_clube) VALUES
('Pedro', 'Brasil', 28, 'Atacante', 9, 1),
('Giorgian de Arrascaeta', 'Uruguai', 31, 'Meia', 10, 1),
('Raphael Veiga', 'Brasil', 31, 'Meia', 23, 2),
('Vitor Roque', 'Brasil', 21, 'Atacante', 9, 2),
('Yuri Alberto', 'Brasil', 25, 'Atacante', 9, 3),
('Rodrigo Garro', 'Argentina', 28, 'Meia', 8, 3),
('Matheus Pereira', 'Brasil', 30, 'Meia', 10, 4),
('Walter Kannemann', 'Argentina', 35, 'Zagueiro', 4, 5),
('Alan Patrick', 'Brasil', 35, 'Meia', 10, 6),
('Philippe Coutinho', 'Brasil', 33, 'Meia', 10, 7),
('Gabriel Barbosa', 'Brasil', 29, 'Atacante', 9, 8),
('Everton Ribeiro', 'Brasil', 36, 'Meia', 10, 9),
('Gonzalo Mastriani', 'Uruguai', 33, 'Atacante', 9, 10);

INSERT INTO Competicao (nome, organizacao) VALUES
('Campeonato Brasileiro Série A', 'CBF');

INSERT INTO Temporada (ano, data_inicio, data_fim, id_competicao) VALUES
(2026, '2026-04-12', '2026-12-06', 1);

INSERT INTO Participacao (
    id_clube,
    id_temporada,
    vitorias,
    empates,
    derrotas,
    gols_pro,
    gols_contra
) VALUES
(1, 1, 22, 6, 10, 68, 35),
(2, 1, 21, 7, 10, 61, 32),
(3, 1, 17, 9, 12, 50, 40),
(4, 1, 16, 10, 12, 48, 41),
(5, 1, 15, 10, 13, 52, 46),
(6, 1, 15, 9, 14, 49, 47),
(7, 1, 13, 11, 14, 45, 48),
(8, 1, 12, 11, 15, 44, 50),
(9, 1, 12, 10, 16, 43, 51),
(10, 1, 11, 11, 16, 42, 53);

INSERT INTO Partida (
    data_partida,
    rodada,
    gols_mandante,
    gols_visitante,
    id_clube_mandante,
    id_clube_visitante,
    id_estadio,
    id_temporada
) VALUES
('2026-04-12', 1, 2, 1, 1, 2, 1, 1),
('2026-04-13', 1, 1, 1, 3, 4, 3, 1),
('2026-04-13', 1, 3, 0, 5, 6, 5, 1),
('2026-04-14', 1, 2, 2, 7, 8, 7, 1),
('2026-04-14', 1, 1, 0, 9, 10, 9, 1),
('2026-05-01', 4, 0, 2, 2, 1, 2, 1),
('2026-05-02', 4, 3, 1, 4, 5, 4, 1),
('2026-05-02', 4, 1, 0, 6, 7, 6, 1),
('2026-05-03', 4, 2, 2, 8, 9, 8, 1),
('2026-05-03', 4, 0, 1, 10, 3, 10, 1);

DROP USER IF EXISTS 'analista'@'localhost';
DROP USER IF EXISTS 'operador'@'localhost';

CREATE USER 'analista'@'localhost' IDENTIFIED BY 'Analista2026!';
CREATE USER 'operador'@'localhost' IDENTIFIED BY 'Operador2026!';

DROP ROLE IF EXISTS 'role_analista';
DROP ROLE IF EXISTS 'role_operador';

CREATE ROLE 'role_analista';
CREATE ROLE 'role_operador';

DELIMITER $$

CREATE PROCEDURE sp_cadastrar_jogador(
    IN p_nome VARCHAR(100),
    IN p_nacionalidade VARCHAR(50),
    IN p_idade INT,
    IN p_posicao VARCHAR(30),
    IN p_numero_camisa INT,
    IN p_id_clube INT
)
BEGIN
    INSERT INTO Jogador(
        nome,
        nacionalidade,
        idade,
        posicao,
        numero_camisa,
        id_clube
    )
    VALUES(
        p_nome,
        p_nacionalidade,
        p_idade,
        p_posicao,
        p_numero_camisa,
        p_id_clube
    );
END $$

DELIMITER ;

DELIMITER $$

CREATE FUNCTION fn_saldo_gols(
    gols_pro INT,
    gols_contra INT
)
RETURNS INT
DETERMINISTIC
BEGIN
    RETURN gols_pro - gols_contra;
END $$

DELIMITER ;

DELIMITER $$

# Trigger

CREATE TRIGGER trg_validar_idade_jogador
BEFORE INSERT
ON Jogador
FOR EACH ROW
BEGIN
    IF NEW.idade < 15 THEN
        SIGNAL SQLSTATE '45000'
        SET MESSAGE_TEXT = 'Jogador deve possuir pelo menos 15 anos';
    END IF;
END $$

DELIMITER ;

CREATE VIEW classificacao_completa AS
SELECT
    c.nome AS clube,
    (p.vitorias * 3) + (p.empates * 1) AS pontos,
    p.vitorias,
    p.empates,
    p.derrotas,
    p.gols_pro,
    p.gols_contra,
    (p.gols_pro - p.gols_contra) AS saldo_gols,
    ROUND(
        (((p.vitorias * 3) + (p.empates * 1)) / ((p.vitorias + p.empates + p.derrotas) * 3)) * 100,
        2
    ) AS aproveitamento
FROM Participacao p
INNER JOIN Clube c
ON p.id_clube = c.id_clube
ORDER BY pontos DESC;

GRANT SELECT ON brasileirao2026.* TO 'role_analista';
GRANT EXECUTE ON FUNCTION brasileirao2026.fn_saldo_gols TO 'role_analista';

GRANT SELECT ON brasileirao2026.Estadio TO 'role_operador';
GRANT SELECT ON brasileirao2026.Clube TO 'role_operador';
GRANT SELECT ON brasileirao2026.Jogador TO 'role_operador';
GRANT EXECUTE ON PROCEDURE brasileirao2026.sp_cadastrar_jogador TO 'role_operador';

GRANT 'role_analista' TO 'analista'@'localhost';
GRANT 'role_operador' TO 'operador'@'localhost';

SET DEFAULT ROLE 'role_analista' TO 'analista'@'localhost';
SET DEFAULT ROLE 'role_operador' TO 'operador'@'localhost';

# Cadastro de jogador para testar proceudre e trigger

SET @id_santos = (
    SELECT id_clube
    FROM Clube
    WHERE nome = 'Santos'
    LIMIT 1
);

CALL sp_cadastrar_jogador(
    'Neymar',
    'Brasil',
    34,
    'Atacante',
    10,
    @id_santos
);


#Teste do trigger

CALL sp_cadastrar_jogador(
    'Joazindo da Silva',
    'Brasil',
    21,
    'Atacante',
    10,
    (
        SELECT id_clube
        FROM Clube
        WHERE nome = 'Palmeiras'
        LIMIT 1
    )
);

# Verificacao de adicao de jogador

SELECT
    j.nome AS jogador,
    j.nacionalidade,
    j.idade,
    j.posicao,
    j.numero_camisa,
    c.nome AS clube
FROM Jogador j
INNER JOIN Clube c
ON j.id_clube = c.id_clube
WHERE j.nome = 'Neymar';

# Select com Function Saldo de gols

SELECT
    p.id_partida,
    cm.nome AS mandante,
    p.gols_mandante,
    p.gols_visitante,
    cv.nome AS visitante,
    fn_saldo_gols(p.gols_mandante, p.gols_visitante) AS saldo_gols_mandante,
    fn_saldo_gols(p.gols_visitante, p.gols_mandante) AS saldo_gols_visitante
FROM Partida p
INNER JOIN Clube cm
ON p.id_clube_mandante = cm.id_clube
INNER JOIN Clube cv
ON p.id_clube_visitante = cv.id_clube
WHERE p.id_partida = 3;


SELECT * FROM Clube;

# Select jogador e clube

SELECT
    Jogador.nome AS jogador,
    Clube.nome AS clube
FROM Jogador
INNER JOIN Clube
ON Jogador.id_clube = Clube.id_clube;

# Select parcial da tabela 

SELECT
    Clube.nome,
    (Participacao.vitorias * 3) + (Participacao.empates * 1) AS pontos,
    Participacao.vitorias,
    Participacao.empates,
    Participacao.derrotas
FROM Participacao
INNER JOIN Clube
ON Participacao.id_clube = Clube.id_clube
ORDER BY pontos DESC;

# Select das partidas

SELECT
    p.id_partida,
    cm.nome AS mandante,
    p.gols_mandante,
    p.gols_visitante,
    cv.nome AS visitante,
    p.data_partida
FROM Partida p
INNER JOIN Clube cm
ON p.id_clube_mandante = cm.id_clube
INNER JOIN Clube cv
ON p.id_clube_visitante = cv.id_clube;

# Select completo da tabela com view

SELECT * FROM classificacao_completa;

# ---------------------------------------------------------------------------
# SELECT * de TODAS as tabelas
# Permite visualizar o estado completo do banco e acompanhar, em tempo real,
# as mudancas feitas pelo backend Python (INSERT/UPDATE/DELETE) acontecendo
# simultaneamente. Basta reexecutar este bloco apos cada alteracao.
# ---------------------------------------------------------------------------

SELECT * FROM Estadio;
SELECT * FROM Treinador;
SELECT * FROM Clube;
SELECT * FROM Jogador;
SELECT * FROM Competicao;
SELECT * FROM Temporada;
SELECT * FROM Participacao;
SELECT * FROM Partida;
