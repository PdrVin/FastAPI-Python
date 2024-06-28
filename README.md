# Workout API
## Descrição do Projeto
A **Workout API** é uma aplicação desenvolvida em Python para gerenciar informações relacionadas a atletas, categorias e centros de treinamento.
A API permite o cadastro, atualização, remoção e consulta dessas entidades, facilitando a gestão de dados para aplicativos de treinamento e academias.

## Bibliotecas Python e Tecnologias Utilizadas
- **FastAPI**: Framework para construção de APIs rápidas e eficientes.
- **SQLAlchemy**: Biblioteca ORM para manipulação do banco de dados.
- **Pydantic**: Utilizado para validação de dados e definição de schemas.
- **Alembic**: Ferramenta para gerenciamento de migrações de banco de dados.
- **Docker**: Plataforma para criação de contêineres, facilitando a execução e implantação da aplicação.
- **DBeaver**: Ferramenta gratuita e universal que permite gerenciar e consultar bancos de dados de forma eficiente. 

## Estrutura de Pastas
- `alembic/`: Contém as configurações e versões de migração do banco de dados.
  - `versions/`: Armazena os scripts de migração.
- `workout_api/`: Diretório principal do código-fonte da aplicação.
  - `atleta/`: Módulo responsável pelas operações relacionadas aos atletas.
  - `base/`: Contém as definições básicas de repositórios, modelos e dependências.
  - `categoria/`: Módulo responsável pelas operações relacionadas às categorias.
  - `centro_treinamento/`: Módulo responsável pelas operações relacionadas aos centros de treinamento.
  - `configs/`: Contém as configurações da aplicação, como banco de dados e settings.
  - `main.py`: Ponto de entrada da aplicação.
  - `routers.py`: Define as rotas da API.
  - `requirements.txt`: Define as bibliotecas necessárias para executar apropriadamente a aplicação.

## Principais Comandos
1. Iniciar o Contâiner Docker para Criar o Banco de Dados.
   ```
   docker-compose up -d
   ```
2. Criar o Ambiente de Migração do Alembic
   ```
   alembic init alembic
   ``` 
3. Gerar uma Revisão de Migração para Iniciar o Banco de Dados
   ```
   alembic revision --autogenerate -m init_db
   ```
4. Executar o Servidor Local da API pelo Uvicorn
   ```
   uvicorn workout_api.main:app --reload
   ```
5. Conferir os EndPoints do API Docs
   -> [http://127.0.0.1:8000/docs]


## Endpoints Principais
### Atletas
- ```GET /atletas```: Lista todos os atletas.
- ```POST /atletas```: Cria um novo atleta.
- ```GET /atletas/{id}```: Obtém detalhes de um atleta específico.
- ```PATCH /atletas/{id}```: Atualiza informações de um atleta.
- ```DELETE /atletas/{id}```: Remove um atleta.
### Categorias
- ```GET /categorias```: Lista todas as categorias.
- ```POST /categorias```: Cria uma nova categoria.
- ```GET /categorias/{id}```: Obtém detalhes de uma categoria específica.
### Centros de Treinamento
- ```GET /centros_treinamento```: Lista todos os centros de treinamento.
- ```POST /centros_treinamento```: Cria um novo centro de treinamento.
- ```GET /centros_treinamento/{id}```: Obtém detalhes de um centro de treinamento específico.
