# pull the official base image
FROM python:3.9.13-slim
ENV PYTHONUNBUFFERED True

ENV APP_HOME /app
WORKDIR $APP_HOME
COPY . ./

# install dependencies
RUN pip install --upgrade pip 
RUN pip install -r requirements.txt
RUN pip install django-cors-headers

EXPOSE 8080

WORKDIR $APP_HOME/Core

CMD ["python", "manage.py", "runserver", "0.0.0.0:8080"]