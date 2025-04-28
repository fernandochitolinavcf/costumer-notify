#!/bin/bash

set -e  # Se der erro, para o script

echo "🔵 Atualizando pacotes..."
sudo apt update && sudo apt upgrade -y

echo "🔵 Instalando dependências básicas..."
sudo apt install -y apt-transport-https ca-certificates curl software-properties-common wget unzip gnupg lsb-release

echo "🔵 Adicionando repositório Docker..."
curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo gpg --dearmor -o /usr/share/keyrings/docker-archive-keyring.gpg
echo "deb [arch=amd64 signed-by=/usr/share/keyrings/docker-archive-keyring.gpg] https://download.docker.com/linux/ubuntu $(lsb_release -cs) stable" | sudo tee /etc/apt/sources.list.d/docker.list > /dev/null

echo "🔵 Atualizando apt após adicionar Docker..."
sudo apt update

echo "🔵 Instalando Docker..."
sudo apt install -y docker-ce docker-ce-cli containerd.io

echo "🔵 Instalando Docker Compose..."
sudo curl -L "https://github.com/docker/compose/releases/download/v2.24.2/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
sudo chmod +x /usr/local/bin/docker-compose

echo "✅ Docker Compose instalado: $(docker-compose --version)"

echo "🔵 Instalando Google Chrome..."
wget https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb
sudo apt install -y ./google-chrome-stable_current_amd64.deb || sudo apt --fix-broken install -y

echo "🔵 Instalando ChromeDriver..."
CHROME_VERSION=$(google-chrome --version | awk '{print $3}' | cut -d '.' -f 1)
wget -O chromedriver.zip https://chromedriver.storage.googleapis.com/${CHROME_VERSION}.0/chromedriver_linux64.zip
unzip chromedriver.zip
sudo mv chromedriver /usr/local/bin/
sudo chmod +x /usr/local/bin/chromedriver

echo "✅ ChromeDriver instalado: $(chromedriver --version)"

echo "✅✅ Ambiente configurado com sucesso!"
