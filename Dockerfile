FROM python:3.10-slim as base

WORKDIR /price-analytics-platform

RUN pip install --no-cache-dir --upgrade pip
COPY ./requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 80
CMD ["./run.sh"]
