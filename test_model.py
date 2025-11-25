import pandas as pd
import numpy as np
import pickle
import sys

def test_model_loading():
    print("TESTE 1: Carregamento do Modelo")
    
    try:
        with open('lgbm_model_optimized.pkl', 'rb') as f:
            model = pickle.load(f)
        print("Modelo carregado com sucesso!")
        print(f"   Tipo: {type(model).__name__}")
        return model
    except Exception as e:
        print(f"Erro ao carregar modelo: {e}")
        return None

def test_scaler_loading():
    print("TESTE 2: Carregamento do Scaler")
    
    try:
        with open('scaler.pkl', 'rb') as f:
            scaler = pickle.load(f)
        print("Scaler carregado com sucesso!")
        print(f"   Tipo: {type(scaler).__name__}")
        return scaler
    except Exception as e:
        print(f"Erro ao carregar scaler: {e}")
        return None

def test_data_loading():
    print("TESTE 3: Carregamento dos Dados de Teste")
    
    try:
        X_test = pd.read_csv('X_test.csv')
        y_test = pd.read_csv('y_test.csv').squeeze()
        
        print("Dados carregados com sucesso!")
        print(f"   X_test shape: {X_test.shape}")
        print(f"   y_test shape: {y_test.shape}")
        print(f"\n   Colunas de X_test:")
        for i, col in enumerate(X_test.columns, 1):
            print(f"      {i}. {col}")
        
        return X_test, y_test
    except Exception as e:
        print(f"Erro ao carregar dados: {e}")
        return None, None

def test_prediction(model, X_test, y_test):
    print("\n" + "=" * 60)
    print("TESTE 4: Predição do Modelo")
    print("=" * 60)
    
    try:
        # Fazer predição em uma amostra
        sample = X_test.head(5)
        predictions = model.predict(sample)
        probabilities = model.predict_proba(sample)
        
        print("Predições realizadas com sucesso!")
        print(f"\n   Amostra de 5 predições:")
        for i in range(5):
            status = "Aprovado" if predictions[i] == 0 else "Rejeitado"
            prob_aprovado = probabilities[i][0] * 100
            prob_rejeitado = probabilities[i][1] * 100
            print(f"      {i+1}. {status} (Aprovado: {prob_aprovado:.2f}%, Rejeitado: {prob_rejeitado:.2f}%)")
        
        # Calcular métricas no conjunto de teste completo
        from sklearn.metrics import roc_auc_score, recall_score, f1_score
        
        y_pred = model.predict(X_test)
        y_proba = model.predict_proba(X_test)[:, 1]
        
        auc = roc_auc_score(y_test, y_proba)
        recall = recall_score(y_test, y_pred)
        f1 = f1_score(y_test, y_pred)
        
        print(f"\n   Métricas no conjunto de teste:")
        print(f"      AUC Score: {auc:.4f}")
        print(f"      Recall (Rejeitado): {recall:.4f}")
        print(f"      F1-Score: {f1:.4f}")
        
        return True
    except Exception as e:
        print(f"Erro ao fazer predição: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_feature_engineering():
    print("\n" + "=" * 60)
    print("TESTE 5: Engenharia de Features")
    print("=" * 60)
    
    try:
        # Criar dados de exemplo
        data = pd.DataFrame({
            'amt_credit': [500000],
            'amt_income_total': [150000],
            'cnt_fam_members': [2],
            'days_employed': [-1825],
            'days_birth': [-12775]
        })
        
        # Aplicar engenharia de features
        data['credit_income_ratio'] = data['amt_credit'] / (data['amt_income_total'] + 1)
        data['income_per_family_member'] = data['amt_income_total'] / (data['cnt_fam_members'] + 1)
        data['days_employed_ratio'] = data['days_employed'] / (data['days_birth'] + 1)
        
        print("Engenharia de features aplicada com sucesso!")
        print(f"\n   Features criadas:")
        print(f"      credit_income_ratio: {data['credit_income_ratio'].values[0]:.4f}")
        print(f"      income_per_family_member: {data['income_per_family_member'].values[0]:.2f}")
        print(f"      days_employed_ratio: {data['days_employed_ratio'].values[0]:.4f}")
        
        return True
    except Exception as e:
        print(f"Erro na engenharia de features: {e}")
        return False

def test_csv_example():
    """Testa o arquivo CSV de exemplo"""
    print("TESTE 6: Arquivo CSV de Exemplo")
    
    try:
        exemplo = pd.read_csv('exemplo_lote.csv')
        print("Arquivo de exemplo carregado com sucesso!")
        print(f"   Número de registros: {len(exemplo)}")
        print(f"   Número de colunas: {len(exemplo.columns)}")
        print(f"\n   Primeiras linhas:")
        print(exemplo.head().to_string())
        
        return True
    except Exception as e:
        print(f"Erro ao carregar exemplo: {e}")
        return False

def main():
    print("\n")
    print("|" + " " * 10 + "TESTE DE VALIDAÇÃO DO SISTEMA" + " " * 18 + "|")
    print("|" + " " * 12 + "Sistema de Análise de Crédito" + " " * 17 + "|")
    print("\n")
    
    # Executar testes
    model = test_model_loading()
    scaler = test_scaler_loading()
    X_test, y_test = test_data_loading()
    
    if model is None or scaler is None or X_test is None:
        print("\nTestes falharam! Verifique os arquivos necessários.")
        sys.exit(1)
    
    success = test_prediction(model, X_test, y_test)
    test_feature_engineering()
    test_csv_example()
    
    # Resumo final
    print("RESUMO DOS TESTES")
    print("=" * 60)
    
    if success:
        print("Todos os testes passaram com sucesso!")
    else:
        print("Alguns testes falharam. Verifique os erros acima.")
        sys.exit(1)

if __name__ == "__main__":
    main()
