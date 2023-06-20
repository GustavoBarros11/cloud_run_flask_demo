# Use Python37
FROM python:3.9

# Allow statements and log messages to immediately appear in the logs
ENV PYTHONUNBUFFERED True

# Define o diretório de trabalho dentro do contêiner
# Copy local code to the container image.
ENV APP_HOME /
WORKDIR $APP_HOME

# Copy requirements.txt to the docker image and install packages
COPY requirements.txt .

# Instale as dependências
RUN pip install --no-cache-dir -r requirements.txt

# Copie todo o conteúdo atual para o diretório de trabalho
COPY . .

# Expose port 5000
EXPOSE $PORT

# Use gunicorn as the entrypoint
CMD exec gunicorn --bind :$PORT --workers 1 --threads 1 --timeout 60 main_v1:app