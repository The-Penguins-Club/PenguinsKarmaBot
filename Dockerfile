FROM python:3-slim

WORKDIR /app

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD [ "python", "-m", "Karma", "&", "python", "-m", "bot" ]

RUN chmod +x /app/start.sh

CMD ["/app/start.sh"]