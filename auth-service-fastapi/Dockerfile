FROM python:3.9

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

ENV PYTHONPATH=/app

CMD sh -c "\
  if [ \"$RUN_MIGRATIONS\" = 'true' ]; then alembic upgrade head; fi && \
  if [ \"$RUN_SEED\" = 'true' ]; then python app/database/seed.py; fi && \
  uvicorn app.main:app --host 0.0.0.0 --port 8001"

