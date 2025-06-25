FROM python:3.9.6

WORKDIR /app

COPY . .

ENV PYTHONUNBUFFERED=1
ENV ENV_FILE_PATH=.env

RUN pip install --no-cache-dir -r requirements.txt

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8001"]
