FROM python:3.12.6-slim as prod

COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt

COPY . .
CMD ["python", "main.py"]