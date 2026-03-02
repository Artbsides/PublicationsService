# publications-service

Aplicação desenvolvida em [Python 3.14.2](https://python.org), focada na ingestão e disponibilização de publicações do Diário Oficial da União a partir de arquivos comprimidos.

# Armazenamento de Dados

Esta aplicação possui armazenamento em banco de dados PostgreSQL, portanto, é necessário que o banco esteja disponível antes do seu consumo pela aplicação.

Os arquivos `.zip` enviados são armazenados no [MinIO](https://min.io), garantindo rastreabilidade com os arquivos originais. As publicações e artigos extraídos são persistidos no PostgreSQL e disponibilizados via API.

# Instalação

É necessário que o ambiente escolhido para instalação possua os recursos listados abaixo previamente instalados e configurados:

```
Make
Docker
```

A partir deste ponto, basta rodar o seguinte comando para instalar a aplicação:

```
$ make build
```

Ao final da execução, as imagens Docker serão construídas, os serviços serão inicializados e as migrações do banco de dados serão aplicadas automaticamente.

Para exibir a lista de rotinas disponíveis, execute o comando `make` ou `make help`.

# Variáveis de Ambiente

Edite o arquivo `.env` para alterar as configurações de ambiente da aplicação. Após as alterações (se necessário for) reinicialize a aplicação para que as novas configurações sejam aplicadas.

* Certifique-se de atribuir valor à variável de ambiente `JWT_SECRET` para que a aplicação possa validar a assinatura do token de acesso. Não há formato definido para a secret, porém, recomenda-se a utilização de um hash de 32 bits ou semelhante.

# Inicialização

Para inicializar a API e o worker, basta executar os comandos abaixo.

```
$ make run
$ make run-worker
```

Para execução dockerizada, utilize o parâmetro `dockerized=true`:

```
$ make run dockerized=true
$ make run-worker dockerized=true
```

Caso corra tudo conforme o esperado e nenhuma variável de ambiente tenha sido previamente modificada, os serviços estarão disponíveis nas urls abaixo:

```
http://localhost:8000       (API)
http://localhost:8000/docs  (Swagger)
http://localhost:15672      (RabbitMQ Management)
http://localhost:9001       (MinIO Console)
```

* O modo debug é indicado para fase de desenvolvimento da aplicação, permitindo o uso de breakpoints a partir do "start" das configurações `Api: Launch` ou `Api: Attach` no `VSCode`.

# Autorização

Todas as rotas da aplicação requerem o header `Authorization` preenchido com um Bearer token do tipo [JWT](https://jwt.io).

Para gerar um token válido, acesse o site do JWT, altere a data de expiração utilizando a mesma chave de segurança configurada na variável de ambiente `JWT_SECRET` e sem encodar em Base64.

```
| ----------------------------------- |
| Header                              |
| ----------------------------------- |
| {                                   |
|     "alg": "HS256",                 |
|     "typ": "JWT"                    |
| }                                   |
| ----------------------------------- |
| Payload                             |
| ----------------------------------- |
| {                                   |
|     "exp": 1916239022               |
| }                                   |
| ----------------------------------- |
| Verify Signature                    |
| ----------------------------------- |
| HMACSHA256(                         |
|     base64UrlEncode(header) + "." + |
|     base64UrlEncode(payload),       |
|     [ "secret" ]                    |
| ) [ ] secret base64 encoded         |
| ----------------------------------- |
```

# Fluxo da Aplicação

```
[POST /uploads]
    |
    ├── Valida o arquivo .zip recebido
    ├── Armazena o arquivo no MinIO
    ├── Cria um registro de Upload com status PENDING no PostgreSQL
    └── Enfileira a task de processamento no RabbitMQ
            |
            └── [Celery Worker]
                    |
                    ├── Atualiza status do Upload para PROCESSING
                    ├── Baixa o arquivo .zip do MinIO
                    ├── Cria um registro de Publication vinculado ao Upload
                    ├── Extrai e itera sobre os XMLs do .zip
                    │       |
                    │       ├── Parseia os metadados do elemento <article>
                    │       ├── Gera chave de idempotência para evitar duplicatas
                    │       ├── Persiste o Article no PostgreSQL
                    │       └── Publica evento article.created no RabbitMQ
                    │
                    └── Atualiza status do Upload para COMPLETED
                        (ou FAILED/PENDING em caso de erro, conforme retries)
```

# Estrutura

```
publications-service/
├── app/
│   ├── core/
│   │   ├── config/               # Configurações de banco, broker, storage e worker
│   │   ├── exceptions/           # Exception handler e erros customizados
│   │   ├── authorization.py      # Validação JWT
│   │   ├── database.py           # Base repository
│   │   ├── message_broker.py     # Publicação de eventos
│   │   └── storage.py            # Upload e download no MinIO
│   ├── modules/
│   │   ├── publications/         # Controller, service, repository e schemas de publications e articles
│   │   └── uploads/              # Controller, service, repository e schemas de uploads
│   ├── routers/                  # Router global com prefixo e autenticação
│   ├── utils/
│   │   └── xml.py                # Parser de XMLs do DOU
│   ├── lifespan.py               # Inicialização e encerramento da aplicação
│   ├── models.py                 # Modelos SQLAlchemy
│   └── main.py                   # Entrypoint FastAPI
├── workers/
│   └── create_publication.py     # Task Celery de processamento
├── .infrastructure/
│   ├── database/migrations/      # Migrações Alembic
│   ├── docker/                   # Dockerfiles e Docker Compose
│   └── monitoring/               # Configurações Prometheus e Grafana
├── tests/
├── .env
├── Makefile
└── pyproject.toml
```

# Utilização

O fluxo de uso da aplicação consiste no envio de um arquivo `.zip` contendo XMLs de publicações do Diário Oficial. O processamento ocorre de forma assíncrona e os dados extraídos ficam disponíveis para consulta assim que concluído.

Envio de arquivo para processamento:
```
$ curl --location --request POST 'http://localhost:8000/uploads' \
--header 'Authorization: Bearer <token>' \
--form 'file=@"/caminho/para/arquivo.zip"'
```

Consulta de status do processamento:
```
$ curl --location 'http://localhost:8000/uploads/{upload_id}' \
--header 'Authorization: Bearer <token>'
```

Listagem de publicações extraídas:
```
$ curl --location 'http://localhost:8000/publications' \
--header 'Authorization: Bearer <token>'
```

Listagem de artigos de uma publicação:
```
$ curl --location 'http://localhost:8000/publications/{publication_id}/articles' \
--header 'Authorization: Bearer <token>'
```

# Monitoramento

A rota `/metrics` foi implementada para disponibilizar dados de instrumentação monitorados pelo `Prometheus`. Para ter acesso aos dashboards pré-configurados no `Grafana`, basta executar o comando `make monitoring` e acessar as urls abaixo:

```
http://localhost:3000  (Prometheus)
http://localhost:3001  (Grafana)
```

* As urls podem levar alguns minutos para se tornarem acessíveis. O Grafana demora um pouco na primeira inicialização do container dockerizado.

# Desenvolvimento Local

Para configurar o ambiente de desenvolvimento local sem Docker, é necessário instalar as dependências abaixo previamente:

```
Pyenv
Poetry
```

Com as dependências instaladas, execute o comando abaixo:

```
$ make dependencies
```

* Certifique-se de que a versão do Python instalada corresponde à definida no arquivo `.python-version`.

# Melhorias Necessárias

* Implementar testes unitários e de integração
* Incrementar documentação levando em consideração outros cenários de uso
* Implementar versionamento de rotas
* Melhorar recursos do exception handler

# Principais Tecnologias Utilizadas

* [Poetry](https://python-poetry.org)
* [FastAPI](https://fastapi.tiangolo.com)
* [Pydantic](https://docs.pydantic.dev/latest)
* [SQLAlchemy](https://www.sqlalchemy.org)
* [Alembic](https://alembic.sqlalchemy.org)
* [Celery](https://docs.celeryq.dev)
* [RabbitMQ](https://www.rabbitmq.com)
* [MinIO](https://min.io)
* [PostgreSQL](https://www.postgresql.org)
* [Prometheus](https://prometheus.io)
* [Grafana](https://grafana.com)
* [Docker](https://docs.docker.com)
