FROM python:3.9

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

ENV PYTHONPATH=/app

CMD sh -c "echo RUN_MIGRATIONS=$RUN_MIGRATIONS && \
if [ \"$RUN_MIGRATIONS\" = 'true' ]; then alembic upgrade head; \
fi && uvicorn app.main:app --host 0.0.0.0 --port 8002"

