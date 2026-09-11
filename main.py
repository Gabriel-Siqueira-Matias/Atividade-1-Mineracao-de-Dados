import pandas as pd
from sqlalchemy import create_engine, text

# Configuração da Conexão com o PostgreSQL
USER = "postgres"
PASSWORD = "1234"  # <--- Insira sua senha do PostgreSQL
HOST = "localhost"
PORT = "5432"
DB_NAME = "dados_evasao"

engine = create_engine(f"postgresql://{USER}:{PASSWORD}@{HOST}:{PORT}/{DB_NAME}")

def executar_pipeline(lista_novos_alunos):
    # 1. Cria a estrutura no PostgreSQL executando o script SQL
    with open("schema_e_view.sql", "r", encoding="utf-8") as f:
        sql_script = f.read()
    
    with engine.begin() as conn:
        conn.execute(text(sql_script))
    print("✅ Schema, tabelas e views recriados com sucesso!")

    # 2. Popula a tabela de treino a partir do CSV
    df_treino = pd.read_csv("dados_evasao_alunos.csv")
    df_treino.to_sql("alunos_treino", engine, if_exists="append", index=False)
    print("✅ Dados do CSV enviados para a tabela 'alunos_treino'!")

    # 3. Insere a lista de alunos a serem analisados
    colunas = ['id_aluno', 'frequencia', 'media_notas', 'disciplinas_reprov', 
               'participacao', 'situacao_financeira', 'carga_trabalho', 'progresso_curso']
    df_novos = pd.DataFrame(lista_novos_alunos, columns=colunas)
    df_novos.to_sql("aluno_novo", engine, if_exists="append", index=False)
    print("✅ Novos alunos cadastrados na tabela 'aluno_novo'!")

    # 4. Consulta os DataFrames respeitando as ordenações
    df_log_odds_categorias = pd.read_sql('SELECT * FROM log_odds ORDER BY "Log-Odds" DESC;', engine)
    df_resultado_predicao = pd.read_sql('SELECT * FROM predicao_evasao ORDER BY "Aluno" ASC;', engine)

    # 5. Exporta para arquivos CSV
    df_log_odds_categorias.to_csv("log_odds.csv", index=False, encoding="utf-8-sig")
    df_resultado_predicao.to_csv("predicao_evasao.csv", index=False, encoding="utf-8-sig")

    print("\n📁 Arquivos gerados com sucesso:")
    print(" - log_odds.csv (Ordenado dos maiores pesos de evasão para os menores)")
    print(" - predicao_evasao.csv (Ordenado por Aluno 1, Aluno 2, etc.)")

if __name__ == "__main__":
    novos_alunos = [
        ('Aluno 1', 'Alta',  'Média', '1-2',       'Baixa', 'Estável',              'Até 30h/semana',     'Intermediário (26-75%)'),
        ('Aluno 2', 'Baixa', 'Baixa', '3 ou mais', 'Baixa', 'Alta dificuldade',     'Mais de 30h/semana', 'Inicial (0-25%)'),
        ('Aluno 3', 'Alta',  'Alta',  'Nenhuma',   'Alta',  'Estável',              'Não trabalha',       'Final (>75%)'),
        ('Aluno 4', 'Média', 'Baixa', '1-2',       'Média', 'Dificuldade moderada', 'Até 30h/semana',     'Inicial (0-25%)')
    ]

    executar_pipeline(novos_alunos)