import pandas as pd
from sqlalchemy import create_engine, text

# 1. Configuração de Conexão com o PostgreSQL
USER = "postgres"
PASSWORD = "sua_senha_aqui"  # <--- Coloque sua senha do PostgreSQL
HOST = "localhost"
PORT = "5432"
DB_NAME = "dados_evasao"

engine = create_engine(f"postgresql://{USER}:{PASSWORD}@{HOST}:{PORT}/{DB_NAME}")

def carregar_dados_treino():
    # Remove a View para destravar a tabela
    with engine.begin() as conn:
        conn.execute(text("DROP VIEW IF EXISTS vw_predicao_evasao CASCADE;"))
    
    # Envia os dados de treino
    df_treino = pd.read_csv("dados_evasao_alunos_bayes_1M.csv")
    df_treino.to_sql("alunos_treino", engine, if_exists="replace", index=False)
    print("✅ Dados de treino carregados!")

def carregar_novos_alunos(lista_alunos):
    colunas = ['id_aluno', 'frequencia', 'media_notas', 'disciplinas_reprov', 
               'participacao', 'situacao_financeira', 'carga_trabalho', 'progresso_curso']
    
    df_novos = pd.DataFrame(lista_alunos, columns=colunas)
    
    # Limpa a tabela sem tentar recriar a estrutura travada
    with engine.begin() as conn:
        conn.execute(text("DROP VIEW IF EXISTS vw_predicao_evasao CASCADE;"))
        conn.execute(text("DROP TABLE IF EXISTS aluno_novo CASCADE;"))
        
    df_novos.to_sql("aluno_novo", engine, if_exists="replace", index=False)
    print("✅ Novos alunos cadastrados!")

def inicializar_view():
    # Carrega e cria a View no PostgreSQL após o envio das duas tabelas
    with open("schema_e_view.sql", "r", encoding="utf-8") as f:
        sql_script = f.read()
    
    with engine.begin() as conn:
        conn.execute(text(sql_script))
    print("✅ View de predição criada!")

def consultar_resultados():
    resultado = pd.read_sql("SELECT * FROM vw_predicao_evasao;", engine)
    return resultado

if __name__ == "__main__":
    novos_alunos = [
        ('Aluno 1', 'Alta',  'Média', '1-2',       'Baixa', 'Estável',              'Até 30h/semana',     'Intermediário (26-75%)'),
        ('Aluno 2', 'Baixa', 'Baixa', '3 ou mais', 'Baixa', 'Alta dificuldade',     'Mais de 30h/semana', 'Inicial (0-25%)'),
        ('Aluno 3', 'Alta',  'Alta',  'Nenhuma',   'Alta',  'Estável',              'Não trabalha',       'Final (>75%)'),
        ('Aluno 4', 'Média', 'Baixa', '1-2',       'Média', 'Dificuldade moderada', 'Até 30h/semana',     'Inicial (0-25%)')
    ]

    # Ordem de execução sem conflito de dependências:
    carregar_dados_treino()
    carregar_novos_alunos(novos_alunos)
    inicializar_view()

    # Exibe a consulta final da View
    df_resultado = consultar_resultados()
    print("\n--- RESULTADO DA PREDIÇÃO (POSTGRESQL) ---")
    print(df_resultado.to_string(index=False))