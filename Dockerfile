FROM python:3.13-alpine3.20 AS builder

ARG DEV_MODE="YES"

WORKDIR /tmp
RUN pip install pdm
COPY pyproject.toml pdm.lock /tmp/
RUN if [ "${DEV_MODE}" = "YES" ] ; then pdm export --output /tmp/project_requirements.txt ; fi
RUN if [ "${DEV_MODE}" = "NO" ] ; then pdm export --prod --output /tmp/project_requirements.txt ; fi

FROM python:3.13-alpine3.20

COPY --from=builder /tmp/project_requirements.txt /tmp/
RUN pip install uvicorn[standard]
RUN pip install -r /tmp/project_requirements.txt

WORKDIR /app/
COPY ./src/midaas/ /app/

CMD ["uvicorn", "--host", "0.0.0.0", "--port", "8200", "main:app"]
