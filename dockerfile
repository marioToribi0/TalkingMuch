FROM python:3.10.2

RUN pip install poetry

# copy all files
COPY . . 

RUN poetry install

EXPOSE 80

ENTRYPOINT ["poetry", "run", "python", "manage.py", "runserver"]

CMD ["0.0.0.0:80"]