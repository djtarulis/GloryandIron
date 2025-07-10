FROM python:3.11

WORKDIR /code

COPY ./app /code/app
COPY requirements.txt /code/

# Install netcat and other dependencies
RUN apt-get update && apt-get install -y netcat-traditional && rm -rf /var/lib/apt/lists/*

RUN pip install --no-cache-dir -r requirements.txt


COPY wait-for-db.sh /wait-for-db.sh
RUN chmod +x /wait-for-db.sh

CMD ["/wait-for-db.sh", "db:5432", "--", "sh", "-c", "uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload"]
