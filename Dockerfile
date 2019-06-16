FROM python:3.6

RUN useradd --create-home appuser
WORKDIR /home/appuser
USER appuser

COPY pyproject.toml .
COPY poetry.lock .

COPY . .

RUN pip install --upgrade pip
RUN pip install poetry
RUN poetry install --no-dev -v 

CMD ["python", "./main.py"]
