import pandas as pd
from sqlalchemy import create_engine, text

# Configuração da Conexão com o PostgreSQL
USER = "postgres"
PASSWORD = "1234"
HOST = "localhost"
PORT = "5432"
DB_NAME = "dados_evasao"

engine = create_engine(
    f"postgresql://{USER}:{PASSWORD}@{HOST}:{PORT}/{DB_NAME}"
)


def perguntar_sim_nao(pergunta, padrao="n"):
    sufixo = " [S/n]: " if padrao.lower() == "s" else " [s/N]: "

    while True:
        resposta = input(pergunta + sufixo).strip().lower()

        if resposta == "":
            resposta = padrao.lower()

        if resposta in ("s", "sim"):
            return True

        if resposta in ("n", "nao", "não"):
            return False

        print("Digite 's' para Sim ou 'n' para Não.")


def tabela_existe(nome):
    with engine.connect() as conn:
        return bool(
            conn.execute(
                text("SELECT to_regclass(:nome) IS NOT NULL"),
                {"nome": nome}
            ).scalar()
        )


def criar_estrutura():
    with open("schema_e_view.sql", "r", encoding="utf-8") as f:
        sql_script = f.read()

    with engine.begin() as conn:
        conn.execute(text(sql_script))

    print("✅ Schema, tabelas e views recriados no banco de dados!")


def carregar_treino():
    df_treino = pd.read_csv("tabela_alunos_treino.csv")

    with engine.begin() as conn:
        conn.execute(
            text("TRUNCATE TABLE alunos_treino RESTART IDENTITY;")
        )

    df_treino.to_sql(
        "alunos_treino",
        engine,
        if_exists="append",
        index=False,
        chunksize=10000
    )

    print(
        f"✅ Treino atualizado com {len(df_treino):,} registros."
    )


def carregar_alunos_novos():
    df_novos = pd.read_csv("tabela_alunos_novos.csv")

    # Limpa apenas a tabela de alunos novos.
    # Assim não ficam registros antigos misturados com o CSV.
    with engine.begin() as conn:
        conn.execute(text("TRUNCATE TABLE aluno_novo;"))

    df_novos.to_sql(
        "aluno_novo",
        engine,
        if_exists="append",
        index=False,
        chunksize=5000
    )

    print(
        f"✅ aluno_novo atualizado com {len(df_novos):,} registros do CSV."
    )


def exportar_resultados():
    print("\n⏳ Calculando Log-Odds...")

    df_log_odds_categorias = pd.read_sql(
        '''
        SELECT *
        FROM log_odds
        ORDER BY "Log-Odds Ratio (Peso Evasão)" DESC;
        ''',
        engine
    )

    print("⏳ Calculando predições...")

    df_resultado_predicao = pd.read_sql(
        '''
        SELECT *
        FROM predicao_evasao
        ORDER BY "Aluno" ASC;
        ''',
        engine
    )

    df_log_odds_categorias.to_csv(
        "log_odds.csv",
        index=False,
        encoding="utf-8-sig"
    )

    df_resultado_predicao.to_csv(
        "predicao_evasao.csv",
        index=False,
        encoding="utf-8-sig"
    )

    print("\n📁 Arquivos finais gerados com sucesso:")
    print(" - log_odds.csv")
    print(" - predicao_evasao.csv")


def executar_pipeline():

    estrutura_existe = (
        tabela_existe("alunos_treino")
        and tabela_existe("aluno_novo")
        and tabela_existe("log_odds")
        and tabela_existe("predicao_evasao")
    )

    # Primeira execução: precisa montar o banco.
    if not estrutura_existe:
        print("⚠️ Estrutura não encontrada no PostgreSQL.")
        print("Criando banco e carregando os CSVs pela primeira vez...\n")

        criar_estrutura()
        carregar_treino()
        carregar_alunos_novos()

    else:
        print("\n✅ Estrutura já existe no PostgreSQL.")
        print(
            "Se você alterou aluno_novo manualmente pelo pgAdmin, "
            "responda NÃO à atualização dessa tabela para preservar "
            "as alterações.\n"
        )

        atualizar_treino = perguntar_sim_nao(
            "Deseja atualizar a tabela alunos_treino pelo CSV?"
        )

        if atualizar_treino:
            carregar_treino()
        else:
            print("➡️ alunos_treino mantida como está no PostgreSQL.")

        print()

        atualizar_novos = perguntar_sim_nao(
            "Deseja atualizar a tabela aluno_novo pelo CSV?"
        )

        if atualizar_novos:
            carregar_alunos_novos()
        else:
            print(
                "➡️ aluno_novo mantida como está no PostgreSQL. "
                "As alterações feitas no pgAdmin serão utilizadas."
            )

    # As views usam os dados atuais das tabelas.
    exportar_resultados()


if __name__ == "__main__":
    executar_pipeline()
