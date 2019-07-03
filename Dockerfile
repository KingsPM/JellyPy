FROM python:3.7

COPY . /app

WORKDIR /app
RUN pip install .
WORKDIR /app/service
RUN pip install -r requirements.txt

ENTRYPOINT ["python"]

CMD ["app.py"]