FROM python:3.8.5-alpine

COPY . /app
WORKDIR /app

ENV PYTHONUNBUFFERED 1
ENV SECRET_KEY=&mpg&n&hsgr8m)bg$lm9srk$+d75$yaphj5_r)0i6f^z89gynt

RUN pip3 install --no-cache-dir -r requirements.txt
WORKDIR /app/eternity
RUN python3 manage.py makemigrations
RUN python3 manage.py migrate

ENTRYPOINT [ "python3", "manage.py", "runserver" ]

EXPOSE 8000
