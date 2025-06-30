FROM python:3.9

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

ENV PYTHONPATH=/app

CMD sh -c "alembic upgrade head && python app/database/seed.py && uvicorn app.main:app --host 0.0.0.0 --port 8001"
