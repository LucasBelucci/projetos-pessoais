# projetos-pessoais
 
Esse módulo do GitHub é focado em projetos desenvolvidos além dos encontrados em cursos realizados, portanto, são projetos pensando em colocar em prática o conhecimento adquirido,
direcionado em conteúdos adequados e que possuo interesse. Alguns ainda estão em estágios iniciais

# Anime-dataset

Projeto focado em realizar requests utilizando a API pública fornecida pelo site MyAnimeList com o objetivo de acompanhar a evolução do Top 100 animes de acordo com a média de notas
dos usuários, além disso, com a base de dados obtida, foram observados alguns possíveis insights relacionados ao tópico.
De modo geral, o request se encontra ajustado para realizar a consulta do top rank e extrair algumas informações iniciais, com todos o rank sequenciado, salvamos o resultado em um json,
que posteriormente consultamos o ID do anime de cada posição obtendo arquivos json individuais com detalhes de cada um, formando um diretório com 100 diferentes arquivos, por fim,
através de outro código as informações são unificadas em um arquivo json único capaz de tratar os dados e fornecer possíveis insights, o processo de análise está documentado dentro
do próprio arquivo ipynb.

Os próximos passos pensados para esse projeto são o de inserir o json em um banco de dados e criar uma rotina de coleta mensal dentro de um servidor AWS, além de aprimorar a análise
inicial


# Event-finder

Projeto com o objetivo de realizar a detecção de novos torneios e envio da informação via Chatbot para whatsapp e/ou discord, porém ainda se encontra em estágio inicial.