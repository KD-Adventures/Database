 - adicionei variavel "motivo" na tabela "bloqueia"
 - adicionei a variável "id_diretor" na tabela "filme"
 - coloquei a variável "nome_categoria" como chave estrangeira na tabela "subordinada" (tem que arrumar isso na modelagem da semana passada tbm!)
 - na tabela "GostaArtista" a chave externa "Nome_Artista" tava apontando pra uma variável que não existe (nome_artista). mudei pra id_artista, mas tem que arrumar no modelo da semana passada

 além disso: tem que mudar no modelo da semana passada que na tabela "pertence", "nome_categoria" também é chave primária, pq um filme pode pertencer a várias categorias diferentes. nas tabelas isso já tá certo



 testei no squirrel e compilou. agora tem que botar os exemplos.