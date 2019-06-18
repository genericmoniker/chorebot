FROM python:3.6

RUN useradd --create-home appuser
WORKDIR /home/appuser
USER appuser

COPY pyproject.toml .
COPY poetry.lock .

COPY . .

RUN pip install --user --upgrade pip
RUN pip install --user poetry
RUN /home/appuser/.local/bin/poetry install --no-dev -v 

CMD ["python", "./main.py"]
