FROM python:3.10

WORKDIR /app

RUN apt-get install -y libpq-dev 
COPY requirements.txt .
RUN pip install psycopg2-binary
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8000

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]

