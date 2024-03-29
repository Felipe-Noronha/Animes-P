# Use a imagem oficial do Python
FROM python:3.8

# Configuração do diretório de trabalho
WORKDIR /app/animes

# Copia o arquivo requirements.txt para o contêiner
COPY requirements.txt .

# Instala o Django e outras dependências
RUN pip install --no-cache-dir -r requirements.txt

# Instala o pacote requests
RUN pip install --no-cache-dir requests

# Copia o restante do código para o contêiner
COPY . .

# Adiciona inotify-tools para monitoramento de alterações
RUN apt-get update && apt-get install -y inotify-tools

# Expõe a porta em que o aplicativo estará em execução
EXPOSE 8000

# Comando para iniciar o aplicativo com monitoramento de alterações
CMD ["bash", "-c", "python manage.py makemigrations && python manage.py migrate && python manage.py runserver 0.0.0.0:8000"]
