## Métricas do Modelo

| Métrica | Valor |
|---------|-------|
| **AUC Score** | 0.9509 (95.09%) |
| **Recall (Rejeitado)** | 0.8822 (88.22%) |
| **F1-Score** | 0.9011 (90.11%) |
| **Precision** | Alta |

**Conclusão:** Modelo altamente eficaz para predição de crédito, com excelente capacidade de identificar casos de rejeição (classe minoritária).

---

## Estrutura de Arquivos Entregues

```
deploy_app/
│
├──  Aplicação Principal
│   ├── app.py                        # Aplicação Streamlit (18KB)
│   ├── requirements.txt              # Dependências Python
│   └── exemplo_lote.csv              # Arquivo de exemplo para testes
│
├──  Modelos Treinados
│   ├── lgbm_model_optimized.pkl      # Modelo LightGBM otimizado (840KB)
│   └── scaler.pkl                    # StandardScaler para normalização (1.1KB)
│
├──  Resultados e Análises
│   ├── feature_importance.csv        # Importância das features
│   ├── model_comparison.csv          # Comparação de modelos
│   └── Resumo_de_insights.csv        # Insights da EDA
│
├──  Docker
│   ├── Dockerfile                    # Definição da imagem Docker
│   ├── docker-compose.yml            # Orquestração de containers
│   ├── .dockerignore                 # Arquivos a ignorar no build
│   └── docker-start.sh               # Script de inicialização (executável)
│
├──  Testes
│   ├── test_model.py                 # Script de validação do modelo
│   └── TESTE_LOCAL.md                # Guia completo de testes
│
├──  Documentação
│   ├── README.md                     # Documentação principal (7.1KB)
│   ├── GUIA_RAPIDO.md                # Guia rápido de uso (5.0KB)
│   ├── DOCKER_README.md              # Documentação Docker completa
│   ├── TESTE_LOCAL.md                # Guia de testes locais
│   └── ENTREGA_FINAL.md              # Este documento
│
└──  Scripts Auxiliares
    └── run.sh                        # Script de inicialização sem Docker
```

**Total de Arquivos:** 19  
**Tamanho do Pacote:** ~313 KB (compactado)

---

## Formas de Executar a Aplicação

### Opção 1: Docker (Recomendado para Produção)

```bash
# Inicialização automática
./docker-start.sh

# Ou manualmente
docker-compose build
docker-compose up -d
```

**Vantagens:**
-  Ambiente isolado
-  Fácil replicação
-  Pronto para produção
-  Escalável

### Opção 2: Python Direto (Desenvolvimento)

```bash
# Criar ambiente virtual
python3 -m venv venv
source venv/bin/activate  # Linux/Mac
# ou
venv\Scripts\activate     # Windows

# Instalar dependências
pip install -r requirements.txt

# Executar
streamlit run app.py
```

**Vantagens:**
-  Rápido para desenvolvimento
-  Fácil debug
-  Sem overhead do Docker

### Opção 3: Script Automatizado

```bash
chmod +x run.sh
./run.sh
```

**Vantagens:**
-  Um comando apenas
-  Verifica dependências
-  Feedback visual

---

## Acesso à Aplicação

Após iniciar, acesse:

**Local:** http://localhost:8501  
**Rede:** http://SEU_IP:8501

---

##  Funcionalidades Implementadas

### 1. Análise Individual

**Descrição:** Interface para análise de um cliente por vez.

**Features:**
-  Formulário organizado em 3 colunas
-  17 campos de entrada com validação
-  Cálculo automático de métricas derivadas
-  Predição em tempo real
-  Visualização de probabilidades
-  Gráfico de distribuição
-  Análise de fatores de risco

**Campos de Entrada:**
- Informações Pessoais: Dependentes, Escolaridade, Autônomo
- Informações Financeiras: Renda, Empréstimo, Prazo, Score CIBIL
- Ativos: Residenciais, Comerciais, Luxo, Bancários

**Saída:**
- Status: Aprovado ou Rejeitado
- Probabilidades: Aprovação e Rejeição (%)
- Métricas: Razão Crédito/Renda, Total de Ativos, etc.
- Fatores de Risco: Lista de alertas identificados

### 2. Análise em Lote

**Descrição:** Processamento de múltiplos clientes via CSV.

**Features:**
-  Upload de arquivo CSV
-  Preview dos dados carregados
-  Processamento em massa
-  Estatísticas gerais (aprovados, rejeitados, probabilidades)
-  Tabela de resultados detalhada
-  Download de resultados em CSV

**Formato do CSV:**
- 17 colunas (mesmas da análise individual)
- Arquivo de exemplo incluído: `exemplo_lote.csv`
- Suporta centenas de registros

**Estatísticas Exibidas:**
- Total de análises
- Número de aprovados (%)
- Número de rejeitados (%)
- Probabilidade média de aprovação

### 3. Sobre o Modelo

**Descrição:** Informações técnicas e documentação.

**Conteúdo:**
-  Informações do algoritmo (LightGBM)
-  Métricas de avaliação
-  Features mais importantes
-  Processo de pré-processamento
-  Comparação de modelos (se disponível)
-  Informações da equipe

### 4. Sidebar Informativo

**Conteúdo:**
- Logo do sistema
- Métricas do modelo
- Instruções de uso
- Informações do autor

---

## Tecnologias Utilizadas

### Backend
- **Python 3.11** - Linguagem principal
- **LightGBM 4.1.0** - Modelo de Machine Learning
- **scikit-learn 1.3.0** - Pré-processamento e métricas
- **pandas 2.0.3** - Manipulação de dados
- **numpy 1.24.3** - Computação numérica

### Frontend
- **Streamlit 1.28.0** - Framework web interativo
- **Matplotlib/Seaborn** - Visualizações (via Streamlit)

### Deploy
- **Docker** - Containerização
- **Docker Compose** - Orquestração

---

## Fluxo de Predição

```
1. Entrada de Dados
   ↓
2. Validação de Campos
   ↓
3. Engenharia de Features
   ├── credit_income_ratio
   ├── total_assets
   ├── assets_income_ratio
   ├── loan_assets_ratio
   ├── high_debt
   └── low_cibil
   ↓
4. Normalização (StandardScaler)
   ↓
5. Predição (LightGBM)
   ↓
6. Cálculo de Probabilidades
   ↓
7. Análise de Risco
   ↓
8. Exibição de Resultados
```
---

##  Casos de Uso

### 1. Instituição Financeira

**Cenário:** Banco precisa avaliar solicitações de crédito rapidamente.

**Solução:**
- Análise individual para casos urgentes
- Análise em lote para processamento noturno
- Integração via API (futuro)

### 2. Fintech

**Cenário:** Startup precisa de sistema de crédito automatizado.

**Solução:**
- Deploy em cloud (AWS, GCP, Azure)
- Escalabilidade horizontal com Docker
- Monitoramento de performance
