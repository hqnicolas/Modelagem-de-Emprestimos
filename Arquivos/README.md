## Arquivos Disponíveis

### 1. `exemplo_lote.csv` (5 registros)
**Descrição:** Arquivo básico para teste rápido  
**Uso:** Validação inicial da funcionalidade de análise em lote  
**Conteúdo:** 5 casos reais do dataset de teste

### 2. `exemplo_lote_completo.csv` (20 registros)
**Descrição:** Arquivo completo com casos variados  
**Uso:** Demonstração realista do sistema  
**Conteúdo:** Mix de casos aprovados e rejeitados

---

## Perfis dos Casos

### exemplo_lote_completo.csv - Análise Detalhada

#### Casos de APROVAÇÃO Esperada (10 casos)

**Perfil 1: Cliente Premium (Linhas 1, 5, 9, 17)**
-  Renda alta (> 8M)
-  Score CIBIL excelente (> 820)
-  Ativos substanciais (> 40M)
-  Razão crédito/renda baixa (< 0.25)
-  Educação superior
-  **Resultado esperado:** APROVADO com alta probabilidade

**Perfil 2: Cliente Sólido (Linhas 3, 7, 11, 14, 16, 19)**
-  Renda boa (6M - 8M)
-  Score CIBIL bom (780 - 840)
-  Ativos consideráveis (25M - 40M)
-  Razão crédito/renda moderada (0.30 - 0.40)
-  Educação superior
-  **Resultado esperado:** APROVADO

####  Casos de REJEIÇÃO Esperada (10 casos)

**Perfil 3: Alto Risco Financeiro (Linhas 2, 4, 6, 10, 12, 15, 18)**
-  Renda baixa (< 4M)
-  Score CIBIL muito baixo (< 520)
-  Ativos insuficientes (< 7M)
-  Razão crédito/renda MUITO alta (> 2.5)
-  Muitos dependentes (3-5)
-  Flag `high_debt = 1` e `low_cibil = 1`
-  **Resultado esperado:** REJEITADO com alta probabilidade

**Perfil 4: Risco Moderado-Alto (Linhas 8, 13, 20)**
-  Renda média (4M - 6M)
-  Score CIBIL médio-baixo (520 - 680)
-  Ativos moderados (10M - 20M)
-  Razão crédito/renda alta (1.2 - 1.9)
-  Flag `low_cibil = 1` ou próximo
-  **Resultado esperado:** REJEITADO ou limítrofe

---

##  Distribuição Esperada de Resultados

### exemplo_lote_completo.csv (20 registros)

| Resultado | Quantidade | Percentual |
|-----------|------------|------------|
|  Aprovado | ~10 | ~50% |
|  Rejeitado | ~10 | ~50% |

**Nota:** Os valores exatos podem variar ligeiramente dependendo do threshold do modelo.

---

## Características dos Perfis

### Indicadores de APROVAÇÃO

1. **Score CIBIL Alto**
   - Excelente: > 800
   - Bom: 750 - 800
   - Aceitável: 700 - 750

2. **Razão Crédito/Renda Baixa**
   - Excelente: < 0.5
   - Bom: 0.5 - 1.0
   - Aceitável: 1.0 - 1.5

3. **Ativos Substanciais**
   - Excelente: > 40M
   - Bom: 25M - 40M
   - Aceitável: 15M - 25M

4. **Renda Alta**
   - Excelente: > 8M
   - Bom: 6M - 8M
   - Aceitável: 4M - 6M

5. **Flags Positivas**
   - `high_debt = 0` (sem dívida alta)
   - `low_cibil = 0` (CIBIL não é baixo)
   - `education_encoded = 1` (graduado)

### Indicadores de REJEIÇÃO

1. **Score CIBIL Baixo**
   - Crítico: < 450
   - Ruim: 450 - 550
   - Preocupante: 550 - 650

2. **Razão Crédito/Renda Alta**
   - Crítico: > 3.0
   - Ruim: 2.5 - 3.0
   - Preocupante: 1.5 - 2.5

3. **Ativos Insuficientes**
   - Crítico: < 3M
   - Ruim: 3M - 7M
   - Preocupante: 7M - 15M

4. **Renda Baixa**
   - Crítico: < 2M
   - Ruim: 2M - 3M
   - Preocupante: 3M - 4M

5. **Flags Negativas**
   - `high_debt = 1` (dívida alta)
   - `low_cibil = 1` (CIBIL baixo)
   - Muitos dependentes (> 3)

---


##  Casos de Estudo

### Caso 1: Cliente Ideal (Linha 9 do completo)
```
Renda: 9.2M | Empréstimo: 1.8M | CIBIL: 870
Ativos: 53M | Razão: 0.20 | Dependentes: 0
```
**Análise:** Todos os indicadores positivos  
**Resultado esperado:**  APROVADO (probabilidade > 95%)

### Caso 2: Alto Risco (Linha 10 do completo)
```
Renda: 1.5M | Empréstimo: 5.8M | CIBIL: 390
Ativos: 1.5M | Razão: 3.87 | Dependentes: 5
```
**Análise:** Todos os indicadores negativos  
**Resultado esperado:**  REJEITADO (probabilidade > 95%)

### Caso 3: Limítrofe (Linha 14 do completo)
```
Renda: 5.5M | Empréstimo: 6.5M | CIBIL: 680
Ativos: 18.5M | Razão: 1.18 | Dependentes: 2
```
**Análise:** Indicadores mistos  
**Resultado esperado:** Pode variar (probabilidade ~50-70%)

---

## Criando Seus Próprios Casos

### Template CSV

```csv
no_of_dependents,income_annum,loan_amount,loan_term,cibil_score,residential_assets_value,commercial_assets_value,luxury_assets_value,bank_asset_value,credit_income_ratio,total_assets,assets_income_ratio,loan_assets_ratio,high_debt,low_cibil,education_encoded,self_employed_encoded
[0-10],[200k-10M],[300k-40M],[2-20],[300-900],[0-30M],[0-20M],[0-30M],[0-15M],[calculado],[calculado],[calculado],[calculado],[0/1],[0/1],[0/1],[0/1]
```

### Cálculo das Features

```python
# Features calculadas
credit_income_ratio = loan_amount / income_annum
total_assets = residential + commercial + luxury + bank
assets_income_ratio = total_assets / income_annum
loan_assets_ratio = loan_amount / total_assets

# Flags binárias
high_debt = 1 if credit_income_ratio > 4 else 0
low_cibil = 1 if cibil_score < 650 else 0
education_encoded = 1  # Graduate
self_employed_encoded = 0  # No
```

### Dicas para Criar Casos

**Para APROVAÇÃO:**
- Use CIBIL > 750
- Mantenha razão crédito/renda < 1.0
- Adicione ativos substanciais (> 25M)
- Use renda alta (> 6M)

**Para REJEIÇÃO:**
- Use CIBIL < 550
- Mantenha razão crédito/renda > 2.5
- Use ativos baixos (< 7M)
- Use renda baixa (< 3M)

**Para LIMÍTROFE:**
- Use CIBIL 600-700
- Mantenha razão crédito/renda 1.0-2.0
- Use ativos moderados (10M-20M)
- Use renda média (4M-6M)
