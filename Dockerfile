FROM python:3.9-slim

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

WORKDIR /src

#COPY src/ /project/src/
#COPY static/ /project/static/
#COPY
COPY .. .

RUN apt-get update && \
    apt-get install -y --no-install-recommends build-essential libpq-dev && \
    pip install --no-cache-dir -r requirements.txt && \
    pip install gunicorn && \
    apt-get remove -y build-essential && \
    apt-get autoremove -y && \
    rm -rf /var/lib/apt/lists/*

EXPOSE 8000

ENV STATIC_PATH=/app/src/static

CMD ["gunicorn", "--bind", "0.0.0.0:8000", "app.src.main:app"]