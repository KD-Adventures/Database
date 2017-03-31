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
INSERT INTO Elenco VALUES ('gilberto Almeida', 8794, 'travessa dos caipiras');
INSERT INTO Elenco VALUES ('will Smith', 9244, 'rua dos mortos');
INSERT INTO Elenco VALUES ('rubens Leite', 8654, 'rua solidao');


CREATE TABLE Diretor (
	Id_Elenco VARCHAR(30) NOT NULL,
	PRIMARY KEY(Id_Elenco),
	FOREIGN KEY(Id_Elenco)
		REFERENCES Elenco(Id_Elenco)
			ON DELETE CASCADE
			ON UPDATE NO ACTION
);

INSERT INTO Diretor VALUES ('john apple');
INSERT INTO Diretor VALUES ('gilberto Almeida');
INSERT INTO Diretor VALUES ('rubens Leite');



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
INSERT INTO Ator VALUES ('will Smith');


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
);


INSERT INTO Categoria VALUES ('Terror');
INSERT INTO Categoria VALUES ('Ficcao');
INSERT INTO Categoria VALUES ('Comedia');
INSERT INTO Categoria VALUES ('Romance');
INSERT INTO Categoria VALUES ('Fantasia');
INSERT INTO Categoria VALUES ('Suspense');


CREATE TABLE Subordinada(
	Nome_Categoria VARCHAR(30) NOT NULL,
	Nome_Supercategoria VARCHAR(30) NOT NULL,
	PRIMARY KEY (Nome_Categoria),
	FOREIGN KEY (Nome_Supercategoria)
		REFERENCES Categoria(Nome_Categoria)
			ON DELETE NO ACTION
			ON UPDATE NO ACTION,
);

INSERT INTO Subordinada VALUES ('Romance', 'Comedia');
INSERT INTO Subordinada VALUES ('Ficcao', 'Terror');
INSERT INTO Subordinada VALUES ('Suspense', 'Fantasia');



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

INSERT INTO Pertence VALUES ('abcd', 'Fantasia');
INSERT INTO Pertence VALUES ('abcd', 'Terror');
INSERT INTO Pertence VALUES ('dfas', 'Comedia');
INSERT INTO Pertence VALUES ('dfas', 'Fantasia');
INSERT INTO Pertence VALUES ('axdf', 'Comedia');
INSERT INTO Pertence VALUES ('axdf', 'Ficcao');


CREATE TABLE Artista (
	Id_Artista INTEGER NOT NULL,
	Nome_Artistico VARCHAR(30) NOT NULL,
	Pais VARCHAR(30) NOT NULL,
	Genero VARCHAR(30) NOT NULL,
	PRIMARY KEY (Id_Artista)
);

INSERT INTO Artista VALUES ('1','FranCisco','Brasil','Sertanejo');
INSERT INTO Artista VALUES ('2','Ivan','Russia','Rock');
INSERT INTO Artista VALUES ('3','Tres Menos Um','Argentina','Pop');
INSERT INTO Artista VALUES ('4', 'Os malditos', 'Estados Unidos', 'Funk');
INSERT INTO Artista VALUES ('5', 'Sono', 'India', 'Gospel');
INSERT INTO Artista VALUES ('6', 'Geraldo', 'Argentina', 'Rock');
INSERT INTO Artista VALUES ('7', 'Caio', 'Argentina', 'Rock');
INSERT INTO Artista VALUES ('8', 'Mike', 'Estados Unidos', 'Funk', );
INSERT INTO Artista VALUES ('9', 'Pedro', 'Estados Unidos', 'Funk', );
INSERT INTO Artista VALUES ('10', 'Ricardo', 'India', 'Gospel', );
INSERT INTO Artista VALUES ('11', 'Daniel', 'India', 'Gospel', );



CREATE TABLE Cantor (
	Id_Artista INTEGER NOT NULL,
	Nome_Musico VARCHAR(30) NOT NULL,
	Estilo_Musical VARCHAR(30) NOT NULL,
	Nascimento VARCHAR(30) NOT NULL,
	PRIMARY KEY (Id_Artista),
	FOREIGN KEY (Id_Artista)
		REFERENCES Artista(Id_Artista)
			ON UPDATE NO ACTION
			ON DELETE CASCADE,
);

INSERT INTO Cantor VALUES ('1', 'Francisco da Silva','Sertanejo','22/12/1980');
INSERT INTO Cantor VALUES ('2', 'Ivanilson', 'Rock', '02/02/1982');
INSERT INTO Cantor VALUES ('6', 'Geraldo', 'Rock', '17/07/1987');
INSERT INTO Cantor VALUES ('7', 'Caio', 'Rock', '30/06/1979');
INSERT INTO Cantor VALUES ('8', 'Mike', 'Funk', '12/09/1983');
INSERT INTO Cantor VALUES ('9', 'Pedro', 'Funk', '01/01/1981');
INSERT INTO Cantor VALUES ('10', 'Ricardo', 'Gospel', '03/06/1989');
INSERT INTO Cantor VALUES ('11', 'Daniel', 'Gospel', '4/08/1982');

CREATE TABLE Banda (
	Id_Artista INTEGER NOT NULL,
	PRIMARY KEY (Id_Artista),
	FOREIGN KEY (Id_Artista)
		REFERENCES Artista(Id_Artista)
			ON UPDATE NO ACTION
			ON DELETE CASCADE
);

INSERT INTO Banda VALUES ('3');
INSERT INTO Banda VALUES ('4');
INSERT INTO Banda VALUES ('5');

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

INSERT INTO Composta VALUES ('3','Geraldo');
INSERT INTO Composta VALUES ('3','Caio');
INSERT INTO Composta VALUES ('4','Mike');
INSERT INTO Composta VALUES ('4','Pedro');
INSERT INTO Composta VALUES ('5','Ricardo');
INSERT INTO Composta VALUES ('5','Daniel');

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

INSERT INTO GostaArtista VALUES ('joaquim', '1', '5');
INSERT INTO GostaArtista VALUES ('joaquim', '5', '4');
INSERT INTO GostaArtista VALUES ('constantino', '2', '5');
INSERT INTO GostaArtista VALUES ('constantino', '1', '5');
INSERT INTO GostaArtista VALUES ('gertrude', '4', '3');
INSERT INTO GostaArtista VALUES ('gertrude', '3', '5');