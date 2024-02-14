FROM python:3.11

WORKDIR /usr/src/service

COPY distribution_service .

ENV DJANGO_SETTINGS_MODULE='frozen_dessert.settings.prod'
ENV DEBUG=False
# Database credentials
ENV POSTGRES_USER="postgres"
ENV POSTGRES_PASSWORD="postgres"
ENV POSTGRES_DB="postgres"

# install the requirements
RUN pip install -r requirements.txt

COPY run.sh .

RUN chmod +x run.sh

# CMD ["./run.sh"]
CMD chmod +x ./run.sh && ./run.sh