import pandas as pd
from sqlalchemy import create_engine, text

USER = "postgres"
PASSWORD = "1234"  # <--- Insira sua senha
HOST = "localhost"
PORT = "5432"
DB_NAME = "dados_evasao"

engine = create_engine(f"postgresql://{USER}:{PASSWORD}@{HOST}:{PORT}/{DB_NAME}")

def executar_projeto(lista_novos_alunos):
    # 1. Executa o SQL para limpar e criar a estrutura das tabelas e a View
    with open("schema_e_view.sql", "r", encoding="utf-8") as f:
        sql_script = f.read()
    
    with engine.begin() as conn:
        conn.execute(text(sql_script))
    print("✅ Estrutura de tabelas e View criadas no PostgreSQL!")

    # 2. Carrega a base principal do CSV para a tabela de treino
    df_treino = pd.read_csv("dados_evasao_alunos_bayes_1M.csv")
    df_treino.to_sql("alunos_treino", engine, if_exists="append", index=False)
    print("✅ Dados do CSV enviados para o banco!")

    # 3. Preenche a tabela de novos alunos
    colunas = ['id_aluno', 'frequencia', 'media_notas', 'disciplinas_reprov', 
               'participacao', 'situacao_financeira', 'carga_trabalho', 'progresso_curso']
    df_novos = pd.DataFrame(lista_novos_alunos, columns=colunas)
    df_novos.to_sql("aluno_novo", engine, if_exists="append", index=False)
    print("✅ Novos alunos cadastrados!")

    # 4. Executa a leitura direto da View
    df_resultado = pd.read_sql("SELECT * FROM vw_predicao_evasao;", engine)
    return df_resultado

if __name__ == "__main__":
    novos_alunos = [
        ('Aluno 1', 'Alta',  'Média', '1-2',       'Baixa', 'Estável',              'Até 30h/semana',     'Intermediário (26-75%)'),
        ('Aluno 2', 'Baixa', 'Baixa', '3 ou mais', 'Baixa', 'Alta dificuldade',     'Mais de 30h/semana', 'Inicial (0-25%)'),
        ('Aluno 3', 'Alta',  'Alta',  'Nenhuma',   'Alta',  'Estável',              'Não trabalha',       'Final (>75%)'),
        ('Aluno 4', 'Média', 'Baixa', '1-2',       'Média', 'Dificuldade moderada', 'Até 30h/semana',     'Inicial (0-25%)')
    ]

    resultado = executar_projeto(novos_alunos)
    print("\n--- RESULTADO DA PREDIÇÃO ---")
    print(resultado.to_string(index=False))