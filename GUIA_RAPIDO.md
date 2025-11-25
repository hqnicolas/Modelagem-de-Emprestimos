# Guia Rápido - Sistema de Análise de Crédito

### Preparar Arquivos do Modelo

Execute o notebook [Etapa5_Modelagem_Pedro.ipynb](https://github.com/hqnicolas/Machine-Learning/blob/main/ABP/Modelagem-de-Emprestimos/Etapa5_Modelagem.ipynb) no Google Colab e baixe:
-  `lgbm_model_optimized.pkl`
-  `scaler.pkl`

Coloque esses arquivos na pasta `deploy_app/`

### Instalar Dependências

```bash
pip install -r requirements.txt
```

### Executar Aplicação

**Opção A - Script automático (Linux/Mac):**
```bash
./run.sh
```

**Opção B - Comando direto:**
```bash
streamlit run app.py
```

Acesse: **http://localhost:8501**

---

## Como Usar a Aplicação

### Análise Individual

1. Acesse a aba **"Análise Individual"**
2. Preencha os dados do cliente nos formulários
3. Clique em **"Analisar Crédito"**
4. Visualize o resultado: Aprovado ou Rejeitado

### Análise em Lote

1. Acesse a aba **"Análise em Lote"**
2. Faça upload de um arquivo CSV (use `exemplo_lote.csv` como referência)
3. Clique em **"Analisar Todos"**
4. Baixe os resultados em CSV

---

## Formato do CSV para Análise em Lote

### Colunas Necessárias

```
code_gender, flag_own_car, flag_own_realty, cnt_children, 
amt_income_total, amt_credit, amt_annuity, amt_goods_price, 
name_income_type, name_education_type, name_family_status, 
name_housing_type, occupation_type, days_birth, days_employed, 
days_registration, cnt_fam_members
```

### Valores Aceitos

| Campo | Tipo | Valores |
|-------|------|---------|
| `code_gender` | Numérico | 1 (M) ou 0 (F) |
| `flag_own_car` | Numérico | 1 (Sim) ou 0 (Não) |
| `flag_own_realty` | Numérico | 1 (Sim) ou 0 (Não) |
| `cnt_children` | Inteiro | 0, 1, 2, 3... |
| `amt_income_total` | Decimal | Valor em R$ (ex: 150000.0) |
| `amt_credit` | Decimal | Valor em R$ (ex: 500000.0) |
| `amt_annuity` | Decimal | Valor em R$ (ex: 25000.0) |
| `amt_goods_price` | Decimal | Valor em R$ (ex: 450000.0) |
| `name_income_type` | Texto | Working, Commercial associate, Pensioner, State servant, Student |
| `name_education_type` | Texto | Secondary / secondary special, Higher education, Incomplete higher, Lower secondary, Academic degree |
| `name_family_status` | Texto | Married, Single / not married, Civil marriage, Separated, Widow |
| `name_housing_type` | Texto | House / apartment, With parents, Municipal apartment, Rented apartment, Office apartment, Co-op apartment |
| `occupation_type` | Texto | Laborers, Core staff, Sales staff, Managers, Drivers, etc. |
| `days_birth` | Negativo | -idade_em_anos * 365 (ex: -12775 para 35 anos) |
| `days_employed` | Negativo | -anos_emprego * 365 (ex: -1825 para 5 anos) |
| `days_registration` | Negativo | -anos_registro * 365 (ex: -1825 para 5 anos) |
| `cnt_fam_members` | Inteiro | 1, 2, 3, 4... |

### Exemplo de Linha CSV

```csv
1,0,1,0,150000,500000,25000,450000,Working,Higher education,Married,House / apartment,Laborers,-12775,-1825,-1825,2
```

---

## Interpretação dos Resultados

### Status da Predição

- **CRÉDITO APROVADO**
  - Probabilidade de aprovação > 50%
  - Cliente tem perfil adequado para o crédito

- **CRÉDITO REJEITADO**
  - Probabilidade de rejeição > 50%
  - Cliente apresenta risco elevado

### Métricas Exibidas

- **Probabilidade de Aprovação:** 0-100%
- **Probabilidade de Rejeição:** 0-100%
- **Razão Crédito/Renda:** Quanto maior, maior o risco
  - < 2.0x: Baixo risco
  - 2.0x - 4.0x: Risco moderado
  - > 4.0x: Alto risco

---

## Problemas Comuns

### "Modelo não encontrado"

**Causa:** Arquivo `lgbm_model_optimized.pkl` não está na pasta

**Solução:**
1. Execute o notebook da Etapa 5
2. Baixe o arquivo `.pkl`
3. Coloque na pasta `deploy_app/`

### "Scaler não encontrado"

**Causa:** Arquivo `scaler.pkl` não está na pasta

**Solução:**
1. Baixe o arquivo `scaler.pkl`
2. Coloque na pasta `deploy_app/`

### Erro ao processar CSV

**Causa:** CSV com formato incorreto

**Solução:**
1. Use `exemplo_lote.csv` como referência
2. Verifique se todas as colunas estão presentes
3. Verifique os tipos de dados

### Streamlit não inicia

**Causa:** Dependências não instaladas

**Solução:**
```bash
pip install --upgrade -r requirements.txt
```

---

## Dicas de Uso

### Para Análise Individual
- Preencha todos os campos obrigatórios
- Use valores realistas (renda, crédito, idade)
- A razão crédito/renda é um fator importante

### Para Análise em Lote
- Prepare seu CSV com antecedência
- Use o `exemplo_lote.csv` como template
- Verifique os dados antes do upload
- Baixe os resultados para análise posterior

### Interpretação
- Probabilidades próximas de 50% indicam casos limítrofes
- Probabilidades > 80% ou < 20% indicam casos claros
- Analise a razão crédito/renda para entender o risco

---
