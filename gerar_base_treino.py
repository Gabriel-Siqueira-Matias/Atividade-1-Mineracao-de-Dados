import pandas as pd
import numpy as np

def gerar_massa_treino(total_registros):
    # 1. Definição das Categorias
    frequencias = ['Alta', 'Média', 'Baixa']
    notas = ['Alta', 'Média', 'Baixa']
    reprovacoes = ['Nenhuma', '1-2', '3 ou mais']
    participacoes = ['Alta', 'Média', 'Baixa']
    financeiras = ['Estável', 'Dificuldade moderada', 'Alta dificuldade']
    cargas_trabalho = ['Não trabalha', 'Até 30h/semana', 'Mais de 30h/semana']
    progressos = ['Inicial (0-25%)', 'Intermediário (26-75%)', 'Final (>75%)']

    # 2. Pesos das Categorias (Quanto maior o valor, MAIOR o risco de evasão)
    pesos = {
        'frequencia': {'Alta': -1.2, 'Média': 0.1, 'Baixa': 1.8},
        'media_notas': {'Alta': -1.5, 'Média': -0.2, 'Baixa': 1.6},
        'disciplinas_reprov': {'Nenhuma': -1.0, '1-2': 0.4, '3 ou mais': 1.9},
        'participacao': {'Alta': -0.8, 'Média': 0.0, 'Baixa': 0.9},
        'situacao_financeira': {'Estável': -0.5, 'Dificuldade moderada': 0.3, 'Alta dificuldade': 1.0},
        'carga_trabalho': {'Não trabalha': -0.3, 'Até 30h/semana': 0.2, 'Mais de 30h/semana': 0.9},
        'progresso_curso': {'Inicial (0-25%)': 0.8, 'Intermediário (26-75%)': -0.1, 'Final (>75%)': -0.7}
    }

    # 3. Geração Aleatória de Features
    df = pd.DataFrame({
        'Frequência_nas_aulas': np.random.choice(frequencias, size=total_registros, p=[0.4, 0.35, 0.25]),
        'Média_das_notas': np.random.choice(notas, size=total_registros, p=[0.35, 0.4, 0.25]),
        'Disciplinas_reprovadas': np.random.choice(reprovacoes, size=total_registros, p=[0.5, 0.35, 0.15]),
        'Participação_nas_atividades': np.random.choice(participacoes, size=total_registros, p=[0.3, 0.4, 0.3]),
        'Situação_financeira': np.random.choice(financeiras, size=total_registros, p=[0.45, 0.35, 0.2]),
        'Carga_de_trabalho': np.random.choice(cargas_trabalho, size=total_registros, p=[0.4, 0.35, 0.25]),
        'Progresso_no_curso': np.random.choice(progressos, size=total_registros, p=[0.3, 0.4, 0.3])
    })

    # 4. Cálculo do Escore Combinado por Linha
    escores = np.zeros(total_registros)
    
    escores += df['Frequência_nas_aulas'].map(pesos['frequencia'])
    escores += df['Média_das_notas'].map(pesos['media_notas'])
    escores += df['Disciplinas_reprovadas'].map(pesos['disciplinas_reprov'])
    escores += df['Participação_nas_atividades'].map(pesos['participacao'])
    escores += df['Situação_financeira'].map(pesos['situacao_financeira'])
    escores += df['Carga_de_trabalho'].map(pesos['carga_trabalho'])
    escores += df['Progresso_no_curso'].map(pesos['progresso_curso'])

    # Adiciona ruído estocástico (para que a regra não seja estritamente determinística)
    escores += np.random.normal(0, 0.5, size=total_registros)

    # 5. Conversão para Probabilidade (Função Sigmoide)
    probabilidades = 1 / (1 + np.exp(-escores))

    # 6. Definição da Target 'Abandona_até_o_próximo_semestre'
    df['Abandona_até_o_próximo_semestre'] = np.where(probabilidades > 0.5, 'Sim', 'Não')

    return df

if __name__ == "__main__":
    try:
        x = int(input("Digite o número de alunos para gerar na base de treino (X): "))
        if x <= 0:
            raise ValueError

        df_gerado = gerar_massa_treino(x)
        
        nome_arquivo = "dados_evasao_alunos.csv"
        df_gerado.to_csv(nome_arquivo, index=False, encoding='utf-8')
        
        print(f"\n✅ Arquivo '{nome_arquivo}' gerado com sucesso contendo {x} registros!")
        print("\nDistribuição da variável Alvo:")
        print(df_gerado['Abandona_até_o_próximo_semestre'].value_counts(normalize=True).round(2) * 100)

    except ValueError:
        print("❌ Por favor, digite um número inteiro válido e maior que zero.")