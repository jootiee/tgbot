FROM python:3.10.2-slim as prod

COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt

COPY . .
CMD ["python", "main.py"]


FROM python:3.10.2-slim as test

COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt pytest

COPY . .
CMD ["pytest"]
