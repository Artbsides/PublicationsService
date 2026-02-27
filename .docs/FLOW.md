# Fluxo da Aplicação

## 1. Upload

### `POST /uploads`
- Recebe arquivo `.zip`.
- Salva o arquivo no bucket (MinIO/S3).
- Cria registro em `uploads` com status `pending`.
- Retorna `upload_id`.
- Não publica mensagem diretamente.

## 2. Processamento assíncrono (ingestion worker)

- Worker faz polling em `uploads` com status `pending`.
- Seleção com lock: `FOR UPDATE SKIP LOCKED`.
- Marca upload como `processing`.
- Lê ZIP, extrai XMLs e processa metadados.
- Persiste registros em `articles`.
- Na mesma transação, cria registros em `outbox_events`.
- Finaliza upload como:
  - `completed` (sucesso), ou
  - `failed` (erro com motivo).

## 3. Publicação de eventos (outbox publisher worker)

- Worker faz polling em `outbox_events` pendentes.
- Seleção com lock: `FOR UPDATE SKIP LOCKED`.
- Publica evento no RabbitMQ.
- Em sucesso, marca `published` e `published_at`.
- Em falha, mantém pendente e incrementa tentativas (retry).

## 4. Rotas de leitura

### `GET /uploads`
- Lista uploads com status e metadados principais.

### `GET /uploads/{upload_id}`
- Retorna detalhe do upload:
  - status,
  - referência ao arquivo original,
  - resumo dos artigos processados,
  - estado dos eventos (outbox/publicação).

