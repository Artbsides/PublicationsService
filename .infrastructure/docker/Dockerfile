FROM python:3.14.2-alpine AS development

WORKDIR /publications-service

COPY pyproject.toml poetry.lock ./

RUN pip install --upgrade pip && \
    pip install --no-cache-dir poetry debugpy && \
    pip install poetry-plugin-export

RUN poetry export --output requirements.txt --with-credentials --no-interaction
RUN poetry export --output requirements.development.txt --with-credentials --no-interaction --with development

RUN pip install -r requirements.development.txt --require-hashes --no-cache-dir && \
    pip uninstall poetry --yes

COPY . .

ENV PYTHONPATH=/publications-service

FROM python:3.14.2-alpine

WORKDIR /publications-service

RUN addgroup -S appgroup && \
    adduser -S appuser -G appgroup

COPY --chown=appuser --from=development /publications-service/requirements.txt .
COPY --chown=appuser --from=development /publications-service/app ./app
COPY --chown=appuser --from=development /publications-service/workers ./workers

RUN pip install --upgrade pip && \
    pip install -r requirements.txt --require-hashes --no-cache-dir

RUN rm requirements.txt

USER appuser

ENV APP_HOST=${APP_HOST:-0.0.0.0} \
    APP_PORT=${APP_PORT:-8000}

ENV PYTHONPATH=/publications-service

CMD ["sh", "-c", "uvicorn app.main:app --host=${APP_HOST} --port=${APP_PORT} --workers=4 --loop uvloop --http httptools"]
