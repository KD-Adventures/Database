CREATE TABLE Usuario (
	Login VARCHAR(30) NOT NULL,
	Nome_Usuario VARCHAR(30) NOT NULL,
	CidadeNatal VARCHAR(30) NOT NULL,
	PRIMARY KEY(Login)
);

INSERT INTO Usuario VALUES ('joaquim', 'Joaquim da Silva', 'curitiba');
INSERT INTO Usuario VALUES ('gertrude', 'Gertrude Pereira Machado', 'sao paulo');
INSERT INTO Usuario VALUES ('constantino', 'Constantino Lima', 'moscou');


CREATE TABLE Conhece (
	Login1 VARCHAR(30) NOT NULL,
	Login2 VARCHAR(30) NOT NULL,
	PRIMARY KEY(Login1, Login2),
	FOREIGN KEY(Login1)
		REFERENCES Usuario(Login)
			ON DELETE SET NULL
			ON UPDATE NO ACTION,
	FOREIGN KEY(Login2)
		REFERENCES Usuario(Login)
			ON DELETE SET NULL
			ON UPDATE NO ACTION
);

INSERT INTO Conhece VALUES ('joaquim', 'gertrude');
INSERT INTO Conhece VALUES ('joaquim', 'constantino');
INSERT INTO Conhece VALUES ('gertrude', 'joaquim');
INSERT INTO Conhece VALUES ('gertrude', 'constantino');
INSERT INTO Conhece VALUES ('constantino', 'joaquim');
INSERT INTO Conhece VALUES ('constantino', 'gertrude');


CREATE TABLE Bloqueia (
	Login1 VARCHAR(30) NOT NULL,
	Login2 VARCHAR(30) NOT NULL,
	Motivo VARCHAR(30) NOT NULL,
	PRIMARY KEY(Login1, Login2),
	FOREIGN KEY(Login1)
		REFERENCES Usuario(Login)
			ON DELETE SET NULL
			On UPDATE NO ACTION,
	FOREIGN KEY(Login2)
		REFERENCES Usuario(Login)
			ON DELETE SET NULL
			ON UPDATE NO ACTION			
);

INSERT INTO Bloqueia VALUES ('joaquim', 'gertrude', 'nao sei');
INSERT INTO Bloqueia VALUES ('joaquim', 'constantino', 'cara chato');
INSERT INTO Bloqueia VALUES ('gertrude', 'joaquim', 'fala demais');
INSERT INTO Bloqueia VALUES ('gertrude', 'constantino', 'insuportavel');
INSERT INTO Bloqueia VALUES ('constantino', 'joaquim', 'nao sou obrigado');
INSERT INTO Bloqueia VALUES ('constantino', 'gertrude', 'quero paz');


CREATE TABLE Elenco (
	Id_Elenco VARCHAR(30) NOT NULL,
	Telefone INTEGER NOT NULL,
	Endereço VARCHAR(50) NOT NULL,
	PRIMARY KEY(Id_Elenco)
);

INSERT INTO Elenco VALUES ('john apple', 65132, 'rua margarida');
INSERT INTO Elenco VALUES ('mary orange', 156316, 'avenida das dores');
INSERT INTO Elenco VALUES ('morgan freeman', 8744, 'travessa antonio moura');


CREATE TABLE Diretor (
	Id_Elenco VARCHAR(30) NOT NULL,
	PRIMARY KEY(Id_Elenco),
	FOREIGN KEY(Id_Elenco)
		REFERENCES Elenco(Id_Elenco)
			ON DELETE CASCADE
			ON UPDATE NO ACTION
);

INSERT INTO Diretor VALUES ('john apple');


CREATE TABLE Ator (
	Id_Elenco VARCHAR(30) NOT NULL,
	PRIMARY KEY(Id_Elenco),
	FOREIGN KEY(Id_Elenco)
		REFERENCES Elenco(Id_Elenco)
			ON DELETE CASCADE
			ON UPDATE NO ACTION
);

INSERT INTO Ator VALUES ('mary orange');
INSERT INTO Ator VALUES ('morgan freeman');


CREATE TABLE Filme(
	Id_Filme VARCHAR(4) NOT NULL,
	Nome VARCHAR(30) NOT NULL,
	Lancamento VARCHAR(10) NOT NULL,
	Id_Diretor VARCHAR(30) NOT NULL,
	PRIMARY KEY(Id_Filme),
	FOREIGN KEY(Id_Diretor)
		REFERENCES Diretor(Id_Elenco)
			ON DELETE SET NULL
			ON UPDATE NO ACTION
);

INSERT INTO Filme VALUES ('abcd', 'filme ruim', '23/10/2003', 'john apple');
INSERT INTO Filme VALUES ('dfas', 'filme pessimo', '10/12/2011', 'john apple');
INSERT INTO Filme VALUES ('axdf', 'filme razoavel', '14/08/1998', 'john apple');


CREATE TABLE Atua (
	Id_Elenco VARCHAR(30) NOT NULL,
	Id_Filme VARCHAR(4) NOT NULL,
	PRIMARY KEY(Id_Elenco,Id_Filme),
	FOREIGN KEY(Id_Elenco)
		REFERENCES Ator(Id_Elenco)
			ON DELETE SET NULL
			ON UPDATE NO ACTION,
	FOREIGN KEY(Id_Filme)
		REFERENCES Filme(Id_Filme)
			ON DELETE SET NULL
			ON UPDATE NO ACTION
);

INSERT INTO Atua VALUES ('mary orange', 'abcd');
INSERT INTO Atua VALUES ('mary orange', 'dfas');
INSERT INTO Atua VALUES ('mary orange', 'axdf');
INSERT INTO Atua VALUES ('morgan freeman', 'abcd');
INSERT INTO Atua VALUES ('morgan freeman', 'dfas');
INSERT INTO Atua VALUES ('morgan freeman', 'axdf');


CREATE TABLE GostaFilme (
	Login VARCHAR(30) NOT NULL,
	Id_Filme VARCHAR(4) NOT NULL,
	PRIMARY KEY(Login, Id_Filme),
	FOREIGN KEY(Login)
		REFERENCES Usuario(Login)
			ON DELETE SET NULL
			ON UPDATE NO ACTION,
	FOREIGN KEY(Id_Filme)
		REFERENCES Filme(Id_Filme)
			ON DELETE SET NULL
			ON UPDATE NO ACTION
);

INSERT INTO GostaFilme VALUES ('joaquim', 'axdf');
INSERT INTO GostaFilme VALUES ('joaquim', 'abcd');
INSERT INTO GostaFilme VALUES ('gertrude', 'dfas');
INSERT INTO GostaFilme VALUES ('gertrude', 'abcd');
INSERT INTO GostaFilme VALUES ('constantino', 'dfas');
INSERT INTO GostaFilme VALUES ('constantino', 'axdf');


CREATE TABLE Categoria(
	Nome_Categoria VARCHAR(30) NOT NULL,
	PRIMARY KEY(Nome_Categoria)
);

CREATE TABLE Subordinada(
	Nome_Categoria VARCHAR(30) NOT NULL,
	Nome_Supercategoria VARCHAR(30) NOT NULL,
	PRIMARY KEY (Nome_Categoria, Nome_Supercategoria),
	FOREIGN KEY (Nome_Categoria)
		REFERENCES Categoria(Nome_Categoria)
			ON DELETE NO ACTION
			ON UPDATE NO ACTION,
	FOREIGN KEY(Nome_Supercategoria)
		REFERENCES Categoria(Nome_categoria)
			ON DELETE NO ACTION
			ON UPDATE NO ACTION
);

CREATE TABLE Pertence(
	Id_Filme VARCHAR(4) NOT NULL,
	Nome_Categoria VARCHAR(30) NOT NULL,
	PRIMARY KEY (Id_Filme, Nome_Categoria),
	FOREIGN KEY(Id_Filme)
		REFERENCES Filme(Id_Filme)
			ON DELETE NO ACTION
			ON UPDATE NO ACTION,
	FOREIGN KEY (Nome_Categoria)
		REFERENCES Categoria(Nome_Categoria)
			ON DELETE NO ACTION
			ON UPDATE NO ACTION
);

CREATE TABLE Artista (
	Id_Artista INTEGER NOT NULL,
	Nome_Artistico VARCHAR(30) NOT NULL,
	Pais VARCHAR(30) NOT NULL,
	Genero VARCHAR(30) NOT NULL,
	PRIMARY KEY (Id_Artista)
);

CREATE TABLE Cantor (
	Id_Artista INTEGER NULL,
	Nome_Musico VARCHAR(30) NOT NULL,
	Estilo_Musical VARCHAR(30) NOT NULL,
	Nascimento VARCHAR(30) NOT NULL,
	PRIMARY KEY (Id_Artista),
	FOREIGN KEY (Id_Artista)
		REFERENCES Artista(Id_Artista)
			ON UPDATE NO ACTION
			ON DELETE CASCADE,
);

CREATE TABLE Banda (
	Id_Artista INTEGER NOT NULL,
	PRIMARY KEY (Id_Artista),
	FOREIGN KEY (Id_Artista)
		REFERENCES Artista(Id_Artista)
			ON UPDATE NO ACTION
			ON DELETE CASCADE
);

CREATE TABLE Composta(
	Id_Artista INTEGER NOT NULL,
	Nome_Musico VARCHAR(30) NOT NULL,
	PRIMARY KEY (Id_Artista, Nome_Musico),
	FOREIGN KEY (Id_Artista)
		REFERENCES Banda(Id_Artista)
			ON UPDATE NO ACTION
			ON DELETE SET NULL,
	FOREIGN KEY (Nome_Musico)
		REFERENCES Cantor(Nome_Musico)
			ON UPDATE NO ACTION
			ON DELETE SET NULL
);

CREATE TABLE GostaArtista (
	Login VARCHAR(30) NOT NULL,
	Id_Artista INTEGER NOT NULL,
	Nota INTEGER NOT NULL,
	PRIMARY KEY(Login, Id_Artista),
	FOREIGN KEY(Login)
		REFERENCES Usuario(Login)
			ON DELETE SET NULL
			ON UPDATE NO ACTION,
	FOREIGN KEY(Id_Artista)
		REFERENCES Artista(Id_Artista)
			ON DELETE SET NULL
			ON UPDATE NO ACTION
);