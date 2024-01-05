FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --upgrade pip
RUN pip3 install -r requirements.txt

COPY . .

EXPOSE 5000

CMD ["python3", "queryPinecone.py"]