# Deploy com Docker - Sistema de Análise de Crédito

---

## Visão Geral

Este guia explica como executar o Sistema de Análise de Crédito usando Docker e Docker Compose, facilitando o deploy em qualquer ambiente (desenvolvimento, staging, produção).

---

### Pré-requisitos

Instale Docker e Docker Compose:

**Linux (Ubuntu/Debian):**
```bash
# Instalar Docker
curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh get-docker.sh

# Instalar Docker Compose
sudo apt-get update
sudo apt-get install docker-compose-plugin

# Adicionar usuário ao grupo docker (opcional)
sudo usermod -aG docker $USER
```

**macOS:**
```bash
# Instalar Docker Desktop
# Download: https://docs.docker.com/desktop/install/mac-install/
```

**Windows:**
```bash
# Instalar Docker Desktop
# Download: https://docs.docker.com/desktop/install/windows-install/
```

### Verificar Arquivos

Certifique-se de que os seguintes arquivos estão na pasta:

```
deploy_app/
├── Dockerfile                    Definição da imagem Docker
├── docker-compose.yml            Orquestração dos containers
├── .dockerignore                 Arquivos a ignorar no build
├── docker-start.sh               Script de inicialização
├── app.py                        Aplicação Streamlit
├── requirements.txt              Dependências Python
├── lgbm_model_optimized.pkl      Modelo treinado
├── scaler.pkl                    Scaler para normalização
└── exemplo_lote.csv              Arquivo de exemplo
```

### Iniciar Aplicação

**Opção A - Script Automático (Recomendado):**
```bash
./docker-start.sh
```

**Opção B - Comandos Manuais:**
```bash
# Construir imagem
docker-compose build

# Iniciar container
docker-compose up -d

# Verificar status
docker-compose ps
```

**Acesse:** http://localhost:8501

---

## Estrutura do Docker

### Dockerfile

Define a imagem Docker baseada em Python 3.11:

- **Base:** `python:3.11-slim`
- **Porta:** 8501 (Streamlit)
- **Healthcheck:** Verifica se a aplicação está respondendo
- **Comando:** Inicia o Streamlit em modo headless

### docker-compose.yml

Orquestra os serviços:

- **Service:** `credit-analysis-app`
- **Container:** `credit-analysis-system`
- **Network:** `credit-network` (bridge)
- **Volumes:** Logs e modelos
- **Restart:** `unless-stopped` (reinicia automaticamente)

---

## Comandos Docker Úteis

### Gerenciamento Básico

```bash
# Iniciar containers
docker-compose up -d

# Parar containers
docker-compose down

# Reiniciar containers
docker-compose restart

# Ver status
docker-compose ps

# Ver logs em tempo real
docker-compose logs -f

# Ver logs de um serviço específico
docker-compose logs -f credit-analysis-app
```

### Debugging

```bash
# Entrar no container
docker exec -it credit-analysis-system bash

# Ver logs do Streamlit
docker-compose logs credit-analysis-app

# Verificar recursos do container
docker stats credit-analysis-system

# Inspecionar container
docker inspect credit-analysis-system
```

### Limpeza

```bash
# Parar e remover containers
docker-compose down

# Remover também volumes
docker-compose down -v

# Remover imagens não utilizadas
docker image prune -a

# Limpeza completa do sistema Docker
docker system prune -a --volumes
```

---

## Atualização da Aplicação

### Atualizar Código

```bash
# 1. Parar containers
docker-compose down

# 2. Fazer alterações no código

# 3. Reconstruir imagem
docker-compose build --no-cache

# 4. Iniciar novamente
docker-compose up -d
```

### Atualizar Modelo

```bash
# Opção 1: Substituir arquivo e reiniciar
cp novo_modelo.pkl lgbm_model_optimized.pkl
docker-compose restart

# Opção 2: Usar volume (já configurado)
# Basta substituir o arquivo, o volume está montado
```

---

## Deploy em Produção

### Configurações Recomendadas

#### 1. Usar Variáveis de Ambiente

Crie um arquivo `.env`:

```env
# .env
STREAMLIT_SERVER_PORT=8501
STREAMLIT_SERVER_ADDRESS=0.0.0.0
STREAMLIT_SERVER_HEADLESS=true
STREAMLIT_BROWSER_GATHER_USAGE_STATS=false
```

#### 2. Configurar Proxy Reverso (Nginx)

```nginx
# /etc/nginx/sites-available/credit-analysis
server {
    listen 80;
    server_name seu-dominio.com;

    location / {
        proxy_pass http://localhost:8501;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection "upgrade";
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
```

#### 3. Adicionar SSL (Let's Encrypt)

```bash
# Instalar certbot
sudo apt-get install certbot python3-certbot-nginx

# Obter certificado
sudo certbot --nginx -d seu-dominio.com
```

#### 4. Configurar Logs Persistentes

Modifique `docker-compose.yml`:

```yaml
volumes:
  - ./logs:/app/logs
  - /var/log/credit-analysis:/app/logs  # Logs persistentes
```

#### 5. Limitar Recursos

```yaml
services:
  credit-analysis-app:
    deploy:
      resources:
        limits:
          cpus: '2'
          memory: 2G
        reservations:
          cpus: '1'
          memory: 1G
```

---

## Monitoramento

### Healthcheck

O container possui healthcheck automático:

```bash
# Verificar status de saúde
docker inspect --format='{{.State.Health.Status}}' credit-analysis-system
```

### Logs

```bash
# Ver logs em tempo real
docker-compose logs -f

# Ver últimas 100 linhas
docker-compose logs --tail=100

# Salvar logs em arquivo
docker-compose logs > app.log
```

### Métricas

```bash
# Uso de recursos
docker stats credit-analysis-system

# Informações detalhadas
docker inspect credit-analysis-system
```

---

## Segurança

### Boas Práticas

1. **Não exponha portas desnecessárias**
   ```yaml
   ports:
     - "127.0.0.1:8501:8501"
   ```

2. **Use secrets para dados sensíveis**
   ```yaml
   secrets:
     - model_key
   ```

3. **Execute como usuário não-root**
   ```dockerfile
   RUN useradd -m appuser
   USER appuser
   ```

4. **Mantenha imagens atualizadas**
   ```bash
   docker-compose pull
   docker-compose up -d
   ```

5. **Escaneie vulnerabilidades**
   ```bash
   docker scan credit-analysis-system
   ```

---

## Troubleshooting

### Container não inicia

```bash
# Ver logs de erro
docker-compose logs

# Verificar se a porta está em uso
sudo lsof -i :8501

# Tentar iniciar em modo interativo
docker-compose up
```

### Erro de permissão

```bash
# Adicionar usuário ao grupo docker
sudo usermod -aG docker $USER

# Relogar ou executar
newgrp docker
```

### Modelo não encontrado

```bash
# Verificar se os arquivos estão montados
docker exec credit-analysis-system ls -la /app/*.pkl

# Verificar volumes
docker-compose config
```

### Aplicação lenta

```bash
# Verificar recursos
docker stats

# Aumentar limites de memória
# Editar docker-compose.yml e adicionar:
deploy:
  resources:
    limits:
      memory: 4G
```

### Porta já em uso

```bash
# Encontrar processo usando a porta
sudo lsof -i :8501

# Matar processo
sudo kill -9 <PID>

# Ou usar outra porta
# Editar docker-compose.yml:
ports:
  - "8502:8501"
```

---

## Referências

- [Docker Documentation](https://docs.docker.com/)
- [Docker Compose Documentation](https://docs.docker.com/compose/)
- [Streamlit Docker Guide](https://docs.streamlit.io/knowledge-base/tutorials/deploy/docker)
- [Best Practices for Writing Dockerfiles](https://docs.docker.com/develop/develop-images/dockerfile_best-practices/)
