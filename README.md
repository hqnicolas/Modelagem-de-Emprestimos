Sistema web interativo para análise e predição de aprovação/rejeição de crédito usando Machine Learning. 

A aplicação permite análise individual de clientes e análise em lote via upload de arquivos CSV.

## Funcionalidades

### 1. Análise Individual
- Interface intuitiva para entrada de dados do cliente
- Campos organizados por categoria (pessoal, financeiro, profissional)
- Predição em tempo real
- Visualização de probabilidades
- Métricas detalhadas da análise

### 2. Análise em Lote
- Upload de arquivo CSV com múltiplos clientes
- Processamento em massa
- Estatísticas gerais (aprovados, rejeitados, probabilidades)
- Download dos resultados em CSV

### 3. Informações do Modelo
- Detalhes técnicos do algoritmo
- Métricas de avaliação
- Features importantes
- Informações da equipe

## Como Usar

### Pré-requisitos

1. **Executar o Notebook da Etapa 5**
   - Abra `[Etapa5_Modelagem_Pedro.ipynb](https://github.com/hqnicolas/Machine-Learning/tree/main/ABP/Modelagem-de-Emprestimos)` no Google Colab
   - Execute todas as células
   - Baixe os arquivos gerados:
     - `lgbm_model_optimized.pkl`
     - `scaler.pkl`

2. **Python 3.8+** instalado no sistema

### Instalação

1. **Clone ou baixe este repositório**

2. **Coloque os arquivos do modelo na pasta do app:**
   ```bash
   ├── app.py
   ├── requirements.txt
   ├── lgbm_model_optimized.pkl  ← Arquivo do modelo
   ├── scaler.pkl                 ← Arquivo do scaler
   └── README.md
   ```

3. **Instale as dependências:**
   ```bash
   pip install -r requirements.txt
   ```

### Execução

1. **Navegue até a pasta do app:**
   ```bash
   cd deploy_app
   ```

2. **Execute o Streamlit:**
   ```bash
   streamlit run app.py
   ```

3. **Acesse no navegador:**
   - A aplicação abrirá automaticamente em `http://localhost:8501`
   - Se não abrir, acesse manualmente o endereço acima

## Estrutura de Dados

### Entrada Individual

A aplicação solicita os seguintes dados do cliente:

#### Informações Pessoais
- Gênero (M/F)
- Possui Carro? (Y/N)
- Possui Imóvel? (Y/N)
- Número de Filhos
- Membros da Família

#### Informações Financeiras
- Renda Total Anual (R$)
- Valor do Crédito Solicitado (R$)
- Valor da Anuidade (R$)
- Preço do Bem (R$)

#### Informações Profissionais
- Tipo de Renda
- Escolaridade
- Estado Civil
- Tipo de Moradia
- Ocupação

#### Informações Temporais
- Idade (anos)
- Anos de Emprego
- Anos desde Registro

### Entrada em Lote (CSV)

Para análise em lote, o arquivo CSV deve conter as seguintes colunas:

```csv
code_gender,flag_own_car,flag_own_realty,cnt_children,amt_income_total,amt_credit,amt_annuity,amt_goods_price,name_income_type,name_education_type,name_family_status,name_housing_type,occupation_type,days_birth,days_employed,days_registration,cnt_fam_members
1,0,1,0,150000,500000,25000,450000,Working,Higher education,Married,House / apartment,Laborers,-12775,-1825,-1825,2
```

**Formato dos dados:**
- `code_gender`: 1 (M) ou 0 (F)
- `flag_own_car`: 1 (Y) ou 0 (N)
- `flag_own_realty`: 1 (Y) ou 0 (N)
- `cnt_children`: número inteiro
- Valores monetários: números decimais
- `days_birth`, `days_employed`, `days_registration`: valores negativos (dias)
- Campos de texto: valores exatos conforme as opções do formulário

### Exemplo de CSV

Um arquivo de exemplo (`exemplo_lote.csv`) está incluído na pasta.

## Pré-processamento Automático

A aplicação aplica automaticamente:

1. **Engenharia de Features:**
   - `credit_income_ratio`: Razão crédito/renda
   - `income_per_family_member`: Renda por membro da família
   - `days_employed_ratio`: Razão dias empregado/idade

2. **Normalização:**
   - Aplicação do StandardScaler treinado
   - Mesma transformação usada no treinamento

3. **Codificação:**
   - Variáveis categóricas já codificadas
   - Consistência com o pré-processamento original

## Saída da Predição

### Resultado Individual
- **Status:** Aprovado ou Rejeitado
- **Probabilidade de Aprovação:** 0-100%
- **Probabilidade de Rejeição:** 0-100%
- **Métricas:** Valor solicitado, renda, razão crédito/renda
- **Gráfico:** Distribuição de probabilidades

### Resultado em Lote
- Tabela com todas as predições
- Estatísticas gerais:
  - Total de análises
  - Número de aprovados
  - Número de rejeitados
  - Probabilidade média de aprovação
- Download em CSV com resultados

## Sobre o Modelo

**Características:**
- Modelo de ensemble baseado em árvores de decisão
- Otimizado para dados tabulares
- Rápido e eficiente
- Robusto a outliers
- Captura relações não-lineares

**Tratamento de Desbalanceamento:**
- Uso de `scale_pos_weight`
- Ajuste baseado na proporção de classes (~2.0)

**Otimização:**
- GridSearchCV com validação cruzada (3-fold)
- Hiperparâmetros otimizados:
  - `n_estimators`
  - `learning_rate`
  - `max_depth`
  - `min_child_samples`
  - `subsample`

**Métricas de Avaliação:**
- AUC Score (principal)
- Recall (classe Rejeitado)
- F1-Score
- Precision
