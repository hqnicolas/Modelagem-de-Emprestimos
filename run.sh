#!/bin/bash

# Script de inicialização da aplicação de Deploy
# Autor: Gabriel M. Zavarize

echo "Iniciando Sistema de Análise de Crédito..."
echo ""

# Verificar se os arquivos necessários existem
if [ ! -f "lgbm_model_optimized.pkl" ]; then
    echo "ERRO: Arquivo 'lgbm_model_optimized.pkl' não encontrado!"
    echo ""
    echo "Você precisa:"
    echo "   1. Executar o notebook Etapa5_Modelagem_Pedro.ipynb no Google Colab"
    echo "   2. Baixar o arquivo lgbm_model_optimized.pkl"
    echo "   3. Colocar o arquivo nesta pasta"
    echo ""
    exit 1
fi

if [ ! -f "scaler.pkl" ]; then
    echo "ERRO: Arquivo 'scaler.pkl' não encontrado!"
    echo ""
    echo "Você precisa:"
    echo "   1. Baixar o arquivo scaler.pkl do projeto"
    echo "   2. Colocar o arquivo nesta pasta"
    echo ""
    exit 1
fi

echo "Arquivos necessários encontrados!"
echo ""

# Verificar se o Streamlit está instalado
if ! command -v streamlit &> /dev/null; then
    echo " Streamlit não encontrado. Instalando dependências..."
    pip install -r requirements.txt
    echo ""
fi

echo "Iniciando aplicação Streamlit..."
echo "   Acesse: http://localhost:8501"
echo ""
echo "   Pressione Ctrl+C para encerrar"
echo ""

streamlit run app.py
