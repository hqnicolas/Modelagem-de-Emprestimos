# Guia de Teste Local - Sistema de Análise de Crédito

---

## Objetivo

Este guia ajuda você a testar a aplicação localmente na sua máquina, tanto com Docker quanto sem Docker.

---

## Opção 1: Teste com Docker (Recomendado)

### Pré-requisitos

1. **Docker instalado**
   - Windows/Mac: [Docker Desktop](https://www.docker.com/products/docker-desktop/)
   - Linux: `curl -fsSL https://get.docker.com -o get-docker.sh && sudo sh get-docker.sh`

2. **Docker Compose instalado**
   - Geralmente vem com Docker Desktop
   - Linux: `sudo apt-get install docker-compose-plugin`

### Passo a Passo

#### 1. Baixar todos os arquivos

Certifique-se de ter todos os arquivos na pasta `deploy_app/`:


#### 2. Abrir terminal na pasta

```bash
cd caminho/para/deploy_app
```

#### 3. Executar script de inicialização

**Linux/Mac:**
```bash
chmod +x docker-start.sh
./docker-start.sh
```

**Windows (PowerShell):**
```powershell
docker-compose build
docker-compose up -d
```

#### 4. Acessar aplicação

Abra o navegador em: **http://localhost:8501**

#### 5. Testar funcionalidades

- **Análise Individual:** Preencha dados e clique em "Analisar Crédito"
- **Análise em Lote:** Faça upload do `exemplo_lote.csv`
- **Visualizações:** Verifique gráficos e métricas
- **Download:** Baixe resultados em CSV

#### 6. Verificar logs

```bash
docker-compose logs -f
```

#### 7. Parar aplicação

```bash
docker-compose down
```

---

## Opção 2: Teste sem Docker (Python Direto)

### Pré-requisitos

1. **Python 3.8+** instalado
2. **pip** atualizado

### Passo a Passo

#### 1. Criar ambiente virtual

**Linux/Mac:**
```bash
cd deploy_app
python3 -m venv venv
source venv/bin/activate
```

**Windows:**
```cmd
cd deploy_app
python -m venv venv
venv\Scripts\activate
```

#### 2. Instalar dependências

```bash
pip install -r requirements.txt
```

#### 3. Executar aplicação

```bash
streamlit run app.py
```

#### 4. Acessar aplicação

Abra o navegador em: **http://localhost:8501**

#### 5. Parar aplicação

Pressione `Ctrl+C` no terminal

---

## Casos de Teste

### Caso 1: Cliente de Baixo Risco

**Entrada:**
- Dependentes: 0
- Renda Anual: R$ 1.000.000
- Empréstimo: R$ 500.000
- Prazo: 10 anos
- Score CIBIL: 800
- Ativos Residenciais: R$ 2.000.000
- Ativos Comerciais: R$ 500.000
- Ativos de Luxo: R$ 200.000
- Ativos Bancários: R$ 300.000
- Escolaridade: Graduate
- Autônomo: No

**Resultado Esperado:** **APROVADO** (alta probabilidade)

### Caso 2: Cliente de Alto Risco

**Entrada:**
- Dependentes: 3
- Renda Anual: R$ 200.000
- Empréstimo: R$ 2.000.000
- Prazo: 20 anos
- Score CIBIL: 400
- Ativos Residenciais: R$ 0
- Ativos Comerciais: R$ 0
- Ativos de Luxo: R$ 0
- Ativos Bancários: R$ 50.000
- Escolaridade: Not Graduate
- Autônomo: Yes

**Resultado Esperado:** **REJEITADO** (alta probabilidade)

### Caso 3: Cliente Limítrofe

**Entrada:**
- Dependentes: 1
- Renda Anual: R$ 500.000
- Empréstimo: R$ 1.500.000
- Prazo: 15 anos
- Score CIBIL: 650
- Ativos Residenciais: R$ 800.000
- Ativos Comerciais: R$ 200.000
- Ativos de Luxo: R$ 100.000
- Ativos Bancários: R$ 200.000
- Escolaridade: Graduate
- Autônomo: No

**Resultado Esperado:** Probabilidades próximas de 50%

### Caso 4: Análise em Lote

**Arquivo:** `exemplo_lote.csv`

**Resultado Esperado:**
- 5 registros processados
- Mix de aprovados e rejeitados
- Estatísticas gerais calculadas
- Download de CSV funciona

---

## Problemas Comuns

### Erro: "Modelo não encontrado"

**Solução:**
```bash
# Verificar se os arquivos estão presentes
ls -la *.pkl

# Se não estiverem, copie-os para a pasta
cp /caminho/para/lgbm_model_optimized.pkl .
cp /caminho/para/scaler.pkl .
```

### Erro: "Porta 8501 já em uso"

**Solução:**
```bash
# Linux/Mac
lsof -ti:8501 | xargs kill -9

# Windows
netstat -ano | findstr :8501
taskkill /PID <PID> /F
```

### Erro: "Módulo não encontrado"

**Solução:**
```bash
# Reinstalar dependências
pip install --upgrade -r requirements.txt
```

### Erro Docker: "Cannot connect to Docker daemon"

**Solução:**
```bash
# Iniciar Docker
sudo systemctl start docker

# Ou no Windows/Mac, abrir Docker Desktop
```

---

## Validação de Métricas

### Métricas Esperadas do Modelo

- **AUC Score:** ~0.95 (95%)
- **Recall (Rejeitado):** ~0.88 (88%)
- **F1-Score:** ~0.90 (90%)

### Como Verificar

1. Execute o script de teste:
   ```bash
   python test_model.py
   ```

2. Verifique as métricas exibidas

---
