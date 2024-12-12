FROM python:3.13-alpine3.20 AS builder

WORKDIR /tmp
RUN pip install pdm
COPY pyproject.toml pdm.lock /tmp/
RUN pdm export -o /tmp/project_requirements.txt

FROM python:3.13-alpine3.20

COPY --from=builder /tmp/project_requirements.txt /tmp/
RUN pip install uvicorn[standard]
RUN pip install -r /tmp/project_requirements.txt

WORKDIR /app/
COPY ./src/midaas/ /app/

CMD ["uvicorn", "--host", "0.0.0.0", "--port", "8200", "main:app"]
