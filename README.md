fropy
=====

Frop Social Search em Python

Bem, como o Social Search é apenas uma pequena API focada na busca, achei uma ferramenta menor e mais simples 
a mais adequada. Não criei uma estrutura em diretórios ainda, pois serão só estes arquivos. Se eu quiser aumentar
o número de arquivos, crio.

Para REST, estou utilizando o Bottle.
Para falar com o Neo4j, estou utilizando o neo4j-embedded (mudei recentemente).
Ele tem acesso direto à JVM e é mais rápido, por isso mudei. Ele tem o neo4j built-in, mas sua instalação é mais
difícil.

Instalação:

1- Primeiro, instalar o Python (não vem pro default no Mac OS X)

\# brew install python

2- Bottle

\# easy_install bottle

3- Neo4j
http://docs.neo4j.org/drivers/python-embedded/snapshot/#python-embedded-installation
Já adianto que vai dar muito problema no setup.py, por conta da localização do JAVA_HOME.
Um script que adiantou minha vida (apaga o setup.py e cola o do link que vou passar) foi esse:
https://github.com/originell/jpype/blob/master/setup.py

Pronto, tudo feito para rodar. Para deixar o servidor rodando:
\# python fro.py

Bem, só que até agora, estou fazendo o modelo de User ainda (e não criei o fro.py), logo, não tá rodando.

