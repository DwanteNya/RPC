Instruções
Criar um repositório no Github para o projeto e me adicionar como participante (daniel.bezerra@unicap.br).

O projeto da cadeira conste em criar um sistema que possua comunicação via tópicos e também RPC. O sistema utilizará o rabbitmq, que dá suporte a essas comunicações.

O sistema tem que ser composto por alguns nós que sejam publishers e/ou subscribers. No readme do Github, descrevam o conceito do sistema e criem os nos iniciais com no mínimo uma comunicação pub/sub funcionando.

Resumo: 
- criar o Github
- descrever o conceito do sistema no readme
- fazer uma comunicação pub/sub


Projeto de um jogo da velha foi excolhido para ilustrar a comunicação via topicos RPC 
o sistema utiliza RabbitMQ e a biblioteca "pika" para possiblitar a troca de turnos e 
jogadas do Usuarios X e O, o projeto usa de duas filas para a comunicação, Tabuleiro XO 
e Tabuleiro OX, sendo tabuleiro XO para o envio da jogada de Usuario X para Usuario O, e 
Tabuleiro OX para o oposto, como Usuario X começa jogando, coloquei ele como Publisher
mas ambos os jogadores tem ambas as funções.


# RPC
