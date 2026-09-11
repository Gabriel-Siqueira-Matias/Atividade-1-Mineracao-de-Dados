import csv
import random

N = 100
SEED = 42
MAX_SEMESTRE = 10

random.seed(SEED)

def gerar_aluno(numero):
    return {
        "id_aluno": numero,

        # Frequência específica: 0% até 100%
        "frequencia": random.randint(0, 100),

        # Média específica: 0.0 até 10.0
        "media_notas": round(random.uniform(0, 10), 1),

        # Quantidade de reprovações
        "disciplinas_reprov": random.randint(0, 8),

        # Feature abstrata
        "participacao": random.choice([
            "Baixa",
            "Média",
            "Alta"
        ]),

        # Feature abstrata
        "situacao_financeira": random.choice([
            "Dificuldade alta",
            "Dificuldade moderada",
            "Estável"
        ]),

        # Horas trabalhadas por semana: 0 até 60
        "carga_trabalho": random.randint(0, 60),

        # Semestre atual: 1º até 10º
        "progresso_curso": random.randint(1, MAX_SEMESTRE),

        # Feature abstrata
        "deslocamento": random.choice([
            "Sem impacto",
            "Impacto moderado",
            "Impacto alto"
        ])
    }

dados = [gerar_aluno(i) for i in range(1, N + 1)]

colunas = [
    "id_aluno",
    "frequencia",
    "media_notas",
    "disciplinas_reprov",
    "participacao",
    "situacao_financeira",
    "carga_trabalho",
    "progresso_curso",
    "deslocamento"
]

# Nome do arquivo alinhado com o main.py
with open(
    "tabela_alunos_novos.csv",
    "w",
    newline="",
    encoding="utf-8-sig"
) as arquivo:
    writer = csv.DictWriter(
        arquivo,
        fieldnames=colunas
    )

    writer.writeheader()
    writer.writerows(dados)

print(f"{N} alunos gerados com sucesso no arquivo 'tabela_alunos_novos.csv'!")