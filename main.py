import pandas as pd
from sqlalchemy import create_engine, text

# Configuração da Conexão com o PostgreSQL
USER = "postgres"
PASSWORD = "1234"  # <--- Insira sua senha do PostgreSQL
HOST = "localhost"
PORT = "5432"
DB_NAME = "dados_evasao"

engine = create_engine(f"postgresql://{USER}:{PASSWORD}@{HOST}:{PORT}/{DB_NAME}")

def executar_pipeline():
    # 1. Cria a estrutura no PostgreSQL (Tabelas e Views com discretização)
    with open("schema_e_view.sql", "r", encoding="utf-8") as f:
        sql_script = f.read()
    
    with engine.begin() as conn:
        conn.execute(text(sql_script))
    print("✅ Schema, tabelas e views recriados no banco de dados!")

    # 2. Carrega a tabela de treino bruta a partir de 'tabela_alunos_treino.csv'
    df_treino = pd.read_csv("tabela_alunos_treino.csv")
    df_treino.to_sql("alunos_treino", engine, if_exists="append", index=False)
    print("✅ Treino 'tabela_alunos_treino.csv' inserido no PostgreSQL!")

    # 3. Carrega a tabela de novos alunos bruta a partir de 'tabela_alunos_novos.csv'
    df_novos = pd.read_csv("tabela_alunos_novos.csv")
    df_novos.to_sql("aluno_novo", engine, if_exists="append", index=False)
    print("✅ Novos alunos 'tabela_alunos_novos.csv' inseridos no PostgreSQL!")

    # 4. Lê os resultados calculados pelas Views
    df_log_odds_categorias = pd.read_sql('SELECT * FROM log_odds ORDER BY "Log-Odds Ratio (Peso Evasão)" DESC;', engine)
    df_resultado_predicao = pd.read_sql('SELECT * FROM predicao_evasao ORDER BY "Aluno" ASC;', engine)

    # 5. Salva os relatórios em CSV
    df_log_odds_categorias.to_csv("log_odds.csv", index=False, encoding="utf-8-sig")
    df_resultado_predicao.to_csv("predicao_evasao.csv", index=False, encoding="utf-8-sig")

    print("\n📁 Arquivos finais gerados com sucesso:")
    print(" - log_odds.csv (Pesos de cada categoria ordenados)")
    print(" - predicao_evasao.csv (Predições para os alunos novos em ordem)")

if __name__ == "__main__":
    executar_pipeline()