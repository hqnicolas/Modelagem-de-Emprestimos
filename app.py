import streamlit as st
import pandas as pd
import numpy as np
import pickle
import os
from datetime import datetime

# Configuração da página
st.set_page_config(
    page_title="Sistema de Análise de Crédito",
    layout="wide",
    initial_sidebar_state="expanded"
)

# CSS customizado
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        font-weight: bold;
        color: #1f77b4;
        text-align: center;
        margin-bottom: 2rem;
    }
    .sub-header {
        font-size: 1.5rem;
        font-weight: bold;
        color: #2c3e50;
        margin-top: 2rem;
        margin-bottom: 1rem;
    }
    .result-approved {
        background-color: #d4edda;
        border-left: 5px solid #28a745;
        padding: 1.5rem;
        border-radius: 5px;
        margin: 1rem 0;
    }
    .result-rejected {
        background-color: #f8d7da;
        border-left: 5px solid #dc3545;
        padding: 1.5rem;
        border-radius: 5px;
        margin: 1rem 0;
    }
    .info-box {
        background-color: #e7f3ff;
        border-left: 5px solid #2196F3;
        padding: 1rem;
        border-radius: 5px;
        margin: 1rem 0;
    }
</style>
""", unsafe_allow_html=True)

# Funções auxiliares
@st.cache_resource
def load_model():
    """Carrega o modelo treinado"""
    try:
        with open('lgbm_model_optimized.pkl', 'rb') as f:
            model = pickle.load(f)
        return model
    except FileNotFoundError:
        st.error("Modelo não encontrado! Execute o notebook da Etapa 5 primeiro.")
        return None

@st.cache_resource
def load_scaler():
    """Carrega o scaler para normalização"""
    try:
        with open('scaler.pkl', 'rb') as f:
            scaler = pickle.load(f)
        return scaler
    except FileNotFoundError:
        st.error("Scaler não encontrado! Certifique-se de ter o arquivo scaler.pkl")
        return None

def preprocess_input(input_data, scaler):
    """
    Pré-processa os dados de entrada aplicando normalização com o scaler
    IMPORTANTE: O scaler normaliza apenas as 13 features numéricas contínuas.
    As features binárias (high_debt, low_cibil, education_encoded, self_employed_encoded)
    NÃO são normalizadas.
    """
    processed_data = input_data.copy()

    # Features que devem ser normalizadas (mesmas usadas no treinamento)
    features_to_scale = [
        'no_of_dependents',
        'income_annum',
        'loan_amount',
        'loan_term',
        'cibil_score',
        'residential_assets_value',
        'commercial_assets_value',
        'luxury_assets_value',
        'bank_asset_value',
        'credit_income_ratio',
        'total_assets',
        'assets_income_ratio',
        'loan_assets_ratio'
    ]

    return processed_data

def predict_credit(model, scaler, input_data):
    # Pré-processar dados
    processed_data = preprocess_input(input_data, scaler)
    
    # Fazer predição
    prediction = model.predict(processed_data)[0]
    probability = model.predict_proba(processed_data)[0]
    
    return prediction, probability

# Header
st.markdown('<div class="main-header">Sistema de Análise de Crédito</div>', unsafe_allow_html=True)
st.markdown("---")

# Sidebar - Informações
with st.sidebar:
    st.markdown("### Informações")
    st.info("""
    **Objetivo:** Prever aprovação ou rejeição de crédito
    """)
    
    st.markdown("---")
    st.markdown("### Como usar")
    st.markdown("""
    1. Preencha os dados do cliente
    2. Clique em "Analisar Crédito"
    3. Visualize o resultado da análise
    """)

# Carregar modelo e scaler
model = load_model()
scaler = load_scaler()

if model is None or scaler is None:
    st.markdown('<div class="info-box">', unsafe_allow_html=True)
    st.warning("""
    **Arquivos necessários não encontrados!**
    Baixar os arquivos gerados:
       - `lgbm_model_optimized.pkl`
       - `scaler.pkl`
    """)
    st.markdown('</div>', unsafe_allow_html=True)
    st.stop()

# Tabs principais
tab1, tab2, tab3 = st.tabs(["Análise Individual", "Análise em Lote", "Sobre o Modelo"])

# TAB 1: Análise Individual
with tab1:
    st.markdown('<div class="sub-header">Dados do Cliente</div>', unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("**Informações Pessoais**")
        no_of_dependents = st.number_input("Número de Dependentes", min_value=0, max_value=10, value=0)
        education = st.selectbox("Escolaridade", ["Graduate", "Not Graduate"], index=0)
        education_encoded = 1 if education == "Graduate" else 0
        self_employed = st.selectbox("Autônomo?", ["No", "Yes"], index=0)
        self_employed_encoded = 1 if self_employed == "Yes" else 0
        
    with col2:
        st.markdown("**Informações Financeiras**")
        income_annum = st.number_input("Renda Anual (R$)", min_value=0.0, value=5000000.0, step=100000.0, format="%.2f")
        loan_amount = st.number_input("Valor do Empréstimo (R$)", min_value=0.0, value=2000000.0, step=50000.0, format="%.2f")
        loan_term = st.number_input("Prazo do Empréstimo (anos)", min_value=1, max_value=30, value=10)
        cibil_score = st.number_input("Score de Crédito (CIBIL)", min_value=300, max_value=900, value=750)
        
    with col3:
        st.markdown("**Ativos**")
        residential_assets_value = st.number_input("Valor Ativos Residenciais (R$)", min_value=0.0, value=10000000.0, step=100000.0, format="%.2f")
        commercial_assets_value = st.number_input("Valor Ativos Comerciais (R$)", min_value=0.0, value=5000000.0, step=100000.0, format="%.2f")
        luxury_assets_value = st.number_input("Valor Ativos de Luxo (R$)", min_value=0.0, value=3000000.0, step=100000.0, format="%.2f")
        bank_asset_value = st.number_input("Valor Ativos Bancários (R$)", min_value=0.0, value=5000000.0, step=100000.0, format="%.2f")
    
    st.markdown("---")
    
    # Calcular features engineered (mesmas do treinamento)
    credit_income_ratio = loan_amount / income_annum if income_annum > 0 else 0
    total_assets = residential_assets_value + commercial_assets_value + luxury_assets_value + bank_asset_value
    assets_income_ratio = total_assets / income_annum if income_annum > 0 else 0
    loan_assets_ratio = loan_amount / total_assets if total_assets > 0 else 0
    high_debt = 1 if credit_income_ratio > 4 else 0
    low_cibil = 1 if cibil_score < 650 else 0
    
    # Exibir métricas calculadas
    st.markdown("**Métricas Calculadas**")
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Razão Crédito/Renda", f"{credit_income_ratio:.2f}x")
    with col2:
        st.metric("Total de Ativos", f"R$ {total_assets:,.2f}")
    with col3:
        st.metric("Razão Ativos/Renda", f"{assets_income_ratio:.2f}x")
    with col4:
        st.metric("Razão Empréstimo/Ativos", f"{loan_assets_ratio:.2f}x")
    
    st.markdown("---")
    
    # Botão de análise
    if st.button("Analisar Crédito", type="primary", use_container_width=True):
        # Criar DataFrame com os dados (ordem correta das colunas)
        input_data = pd.DataFrame({
            'no_of_dependents': [no_of_dependents],
            'income_annum': [income_annum],
            'loan_amount': [loan_amount],
            'loan_term': [loan_term],
            'cibil_score': [cibil_score],
            'residential_assets_value': [residential_assets_value],
            'commercial_assets_value': [commercial_assets_value],
            'luxury_assets_value': [luxury_assets_value],
            'bank_asset_value': [bank_asset_value],
            'credit_income_ratio': [credit_income_ratio],
            'total_assets': [total_assets],
            'assets_income_ratio': [assets_income_ratio],
            'loan_assets_ratio': [loan_assets_ratio],
            'high_debt': [high_debt],
            'low_cibil': [low_cibil],
            'education_encoded': [education_encoded],
            'self_employed_encoded': [self_employed_encoded]
        })
        
        # Fazer predição
        with st.spinner("Analisando dados..."):
            try:
                prediction, probability = predict_credit(model, scaler, input_data)
                
                # Exibir resultado
                st.markdown("---")
                st.markdown('<div class="sub-header">Resultado da Análise</div>', unsafe_allow_html=True)
                
                col1, col2 = st.columns(2)
                
                with col1:
                    if prediction == 1:
                        st.markdown('<div class="result-approved">', unsafe_allow_html=True)
                        st.markdown("### CRÉDITO APROVADO")
                        st.markdown(f"**Probabilidade de Aprovação:** {probability[1]*100:.2f}%")
                        st.markdown("</div>", unsafe_allow_html=True)
                    else:
                        st.markdown('<div class="result-rejected">', unsafe_allow_html=True)
                        st.markdown("### CRÉDITO REJEITADO")
                        st.markdown(f"**Probabilidade de Rejeição:** {probability[0]*100:.2f}%")
                        st.markdown("</div>", unsafe_allow_html=True)
                
                with col2:
                    st.markdown("**Detalhes da Análise**")
                    st.metric("Valor Solicitado", f"R$ {loan_amount:,.2f}")
                    st.metric("Renda Anual", f"R$ {income_annum:,.2f}")
                    st.metric("Score CIBIL", cibil_score)
                    st.metric("Razão Crédito/Renda", f"{credit_income_ratio:.2f}x")
                
                # Gráfico de probabilidade
                st.markdown("---")
                st.markdown("** Distribuição de Probabilidade**")
                prob_df = pd.DataFrame({
                    'Classe': ['Aprovado', 'Rejeitado'],
                    'Probabilidade': [probability[1]*100, probability[0]*100]
                })
                st.bar_chart(prob_df.set_index('Classe'))
                
                # Análise de risco
                st.markdown("---")
                st.markdown("**Análise de Risco**")
                
                risk_factors = []
                if credit_income_ratio > 4:
                    risk_factors.append(" Razão Crédito/Renda muito alta (> 4x)")
                elif credit_income_ratio > 3:
                    risk_factors.append(" Razão Crédito/Renda moderada (> 3x)")
                
                if cibil_score < 650:
                    risk_factors.append(" Score de crédito baixo (< 650)")
                elif cibil_score < 700:
                    risk_factors.append(" Score de crédito moderado (< 700)")
                
                if loan_assets_ratio > 0.8:
                    risk_factors.append(" Empréstimo muito alto em relação aos ativos (> 80%)")
                
                if total_assets < loan_amount * 0.5:
                    risk_factors.append(" Ativos totais baixos em relação ao empréstimo")
                
                if risk_factors:
                    for factor in risk_factors:
                        st.markdown(f"- {factor}")
                else:
                    st.success(" Nenhum fator de risco significativo identificado")
                
            except Exception as e:
                st.error(f"Erro ao processar dados: {str(e)}")
                st.exception(e)

# TAB 2: Análise em Lote
with tab2:
    st.markdown('<div class="sub-header">Análise em Lote</div>', unsafe_allow_html=True)
    st.info(" Faça upload de um arquivo CSV com múltiplos clientes para análise em lote")
    
    # Mostrar formato esperado
    with st.expander(" Ver formato esperado do CSV"):
        st.markdown("""
        O arquivo CSV deve conter as seguintes colunas (nesta ordem):
        
        1. `no_of_dependents` - Número de dependentes (0-10)
        2. `income_annum` - Renda anual (R$)
        3. `loan_amount` - Valor do empréstimo (R$)
        4. `loan_term` - Prazo em anos (1-30)
        5. `cibil_score` - Score de crédito (300-900)
        6. `residential_assets_value` - Valor ativos residenciais (R$)
        7. `commercial_assets_value` - Valor ativos comerciais (R$)
        8. `luxury_assets_value` - Valor ativos de luxo (R$)
        9. `bank_asset_value` - Valor ativos bancários (R$)
        10. `credit_income_ratio` - Razão crédito/renda
        11. `total_assets` - Total de ativos (R$)
        12. `assets_income_ratio` - Razão ativos/renda
        13. `loan_assets_ratio` - Razão empréstimo/ativos
        14. `high_debt` - Dívida alta (0 ou 1)
        15. `low_cibil` - CIBIL baixo (0 ou 1)
        16. `education_encoded` - Escolaridade (1=Graduate, 0=Not Graduate)
        17. `self_employed_encoded` - Autônomo (1=Yes, 0=No)
        
        **Veja o arquivo `exemplo_lote.csv` como referência.**
        """)
    
    uploaded_file = st.file_uploader("Escolha um arquivo CSV", type=['csv'])
    
    if uploaded_file is not None:
        try:
            # Ler arquivo
            batch_data = pd.read_csv(uploaded_file)
            
            st.success(f" Arquivo carregado com sucesso! {len(batch_data)} registros encontrados.")
            
            # Mostrar preview
            with st.expander("Visualizar dados carregados"):
                st.dataframe(batch_data.head(10))
            
            if st.button("Analisar Todos", type="primary"):
                with st.spinner("Processando análises..."):
                    # Pré-processar e fazer predições
                    processed_data = preprocess_input(batch_data, scaler)
                    predictions = model.predict(processed_data)
                    probabilities = model.predict_proba(processed_data)
                    
                    # Adicionar resultados ao DataFrame original
                    results_df = batch_data.copy()
                    results_df['Predição'] = ['Aprovado' if p == 1 else 'Rejeitado' for p in predictions]
                    results_df['Prob_Aprovado'] = probabilities[:, 1]
                    results_df['Prob_Rejeitado'] = probabilities[:, 0]
                    
                    # Estatísticas
                    st.markdown("---")
                    st.markdown("**Estatísticas Gerais**")
                    
                    col1, col2, col3, col4 = st.columns(4)
                    
                    with col1:
                        st.metric("Total de Análises", len(batch_data))
                    with col2:
                        aprovados = (predictions == 1).sum()
                        st.metric("Aprovados", aprovados, delta=f"{(aprovados/len(batch_data)*100):.1f}%")
                    with col3:
                        rejeitados = (predictions == 0).sum()
                        st.metric("Rejeitados", rejeitados, delta=f"{(rejeitados/len(batch_data)*100):.1f}%")
                    with col4:
                        prob_media = probabilities[:, 1].mean()
                        st.metric("Prob. Média Aprovação", f"{prob_media*100:.1f}%")
                    
                    # Mostrar resultados
                    st.markdown("---")
                    st.markdown("**Resultados Detalhados**")
                    st.dataframe(results_df)
                    
                    # Download dos resultados
                    csv = results_df.to_csv(index=False).encode('utf-8')
                    st.download_button(
                        label="Baixar Resultados (CSV)",
                        data=csv,
                        file_name=f'analise_credito_{datetime.now().strftime("%Y%m%d_%H%M%S")}.csv',
                        mime='text/csv',
                    )
                    
        except Exception as e:
            st.error(f"Erro ao processar arquivo: {str(e)}")
            st.exception(e)

# TAB 3: Sobre o Modelo
with tab3:
    st.markdown('<div class="sub-header">Sobre o Modelo</div>', unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("### Informações Técnicas")
        st.markdown("""
        **Algoritmo:** LightGBM (Light Gradient Boosting Machine)
        
        **Características:**
        - Modelo de ensemble baseado em árvores de decisão
        - Otimizado para dados tabulares
        - Rápido e eficiente
        - Robusto a outliers
        - Captura relações não-lineares
        
        **Tratamento de Desbalanceamento:**
        - Uso de `scale_pos_weight`
        - Ajuste automático baseado na proporção de classes
        
        **Otimização:**
        - GridSearchCV com validação cruzada (3-fold)
        - Múltiplos hiperparâmetros otimizados
        - Métrica de otimização: AUC Score
        """)
    
    with col2:
        st.markdown("### Métricas de Avaliação")
        st.markdown("""
        **Métricas no Conjunto de Teste:**
        - **AUC Score:** 0.9509 (95.09%)
        - **Recall (Rejeitado):** 0.8822 (88.22%)
        - **F1-Score:** 0.9011 (90.11%)
        
        **Features Mais Importantes:**
        1. Score de Crédito (CIBIL)
        2. Razão Crédito/Renda
        3. Valor do Empréstimo
        4. Renda Anual
        5. Total de Ativos
        6. Razão Empréstimo/Ativos
        
        **Pré-processamento:**
        - Engenharia de features
        - Normalização com StandardScaler
        - Codificação de variáveis categóricas
        """)
    
    st.markdown("---")
    
    # Carregar e exibir comparação de modelos
    try:
        comparison_df = pd.read_csv('model_comparison.csv')
        st.markdown("### Comparação de Modelos")
        st.dataframe(comparison_df, use_container_width=True)
    except:
        pass
    
    st.markdown("---")
    st.markdown("### Etapas do Projeto")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("""
        **Etapa 1-4:** Pré-processamento
        - Análise exploratória
        - Limpeza de dados
        - Feature engineering
        """)
    
    with col2:
        st.markdown("""
        **Etapa 5:** Modelagem
        - Treinamento e otimização
        """)
    
    with col3:
        st.markdown("""
        **Etapa 6:** Deploy
        - Interface web
        - Sistema de predição
        """)
    
    st.markdown("---")
    st.info("""
    **Nota:** Este sistema foi desenvolvido como projeto acadêmico de Machine Learning.
    Para uso em produção, recomenda-se validação adicional e monitoramento contínuo do modelo.
    """)

# Footer
st.markdown("---")
st.markdown("""
<div style='text-align: center; color: #7f8c8d; padding: 1rem;'>
    <p>Sistema de Análise de Crédito - Projeto Machine Learning</p>
</div>
""", unsafe_allow_html=True)
