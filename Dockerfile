FROM python:3.10-slim as base

ARG DB_URL_INPUT
ENV DB_URL=$DB_URL_INPUT
RUN echo "Database url is set to $DB_URL"

WORKDIR /price-analytics-platform

RUN pip install --no-cache-dir --upgrade pip
COPY ./requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 80
CMD ["./run.sh"]
