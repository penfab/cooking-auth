FROM python:slim

WORKDIR /app

COPY ./api /app/api

COPY ./requirements /app/requirements

RUN pip install --no-cache-dir -U pip setuptools wheel
RUN pip install --no-cache-dir -r /app/requirements

CMD ["uvicorn", "api.main:serve_api", "--host", "0.0.0.0", "--port", "8000", "--factory", "--log-level", "debug"]
