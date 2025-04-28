FROM python:3.10-alpine
WORKDIR /app

RUN apk add --no-cache build-base libffi-dev dcron

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copia primeiro todos os arquivos de código e o start.sh
COPY . .

# Agora que o start.sh já está copiado, pode dar permissão
RUN chmod +x /app/start.sh

# Configura o cron
COPY crontab.txt /etc/crontabs/root

ENV PYTHONDONTWRITEBYTECODE=1

# E muda o CMD pra usar o caminho certo também
CMD ["/app/start.sh"]
