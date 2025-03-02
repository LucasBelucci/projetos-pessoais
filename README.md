# projetos-pessoais
 
Esse módulo do GitHub é focado em projetos desenvolvidos além dos encontrados em cursos realizados, portanto, são projetos pensando em colocar em prática o conhecimento adquirido,
direcionado em conteúdos adequados e que possuo interesse. Alguns ainda estão em estágios iniciais

# Anime-dataset

Projeto focado em realizar requests utilizando a API pública fornecida pelo site MyAnimeList com o objetivo de acompanhar a evolução do Top 500 animes de acordo com a média de notas
dos usuários, além disso, com a base de dados obtida, serão obtidos alguns insights que favorecem a obtenção de maiores notas.

O código de coleta faz o request diretamente na API, obtem o índice de cada um dos animes dentro do top500, armazena a informação desses índices temporiariamente e faz uma nova consulta,
mas dessa vez solicitando os detalhes de cada um dos indicados utilizando o ID, com as informações específicas de cada pertencente ao top500, um novo código é executado para realizar 
a unificação das informações, gerando um arquivo detalhado que é então inserido dentro do banco de dados, além disso, salvo como um json, permitindo portanto que se inicie o processo de 
tratamento e análise de dados, que foi melhor explorado dentro do notebook específico, trazendo várias informações importantes e gerando insights interessantes tanto para as empresas, quanto
para os usários da plataforma

Para melhorias futuras, como sugestão, fica o aprimoramento do algoritmo de coleta e unificação dos dados, já que do modo que foi feito atualmente, não foi tratado de maneira adequada
animes que apresentam mais de uma temporada, fazendo com que alguns resultados pudessem ser alterados, causando prejuízo ao algoritmo de regressão utilizado, que também se mostra como um fator
que permite melhorias, fazendo com que os resultados obtidos sejam ainda mais assertivos, além da inserção da rotina de coleta via API em um serviço de nuvem automatizado, criando uma rotina trimestral de coleta,
promovendo então o surgimento de um histórico atualizado constantemente, identificando fatores adicionais, tais como sazonalizadade e velocidade em que um anime se destaca.



# Event-finder

Projeto com o objetivo de realizar a detecção de novos torneios através de um web-scrapping, para então a geração de um arquivo e o posterior envio via Chatbot para whatsapp e/ou discord, porém,
apenas o escopo dos requisitos necessários foi gerado, portanto se encontra em um estado bem inicial.