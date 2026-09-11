import numpy as np
import pandas as pd

# ==========================================================
# CONFIGURAÇÕES
# ==========================================================

N = 1_000
SEED = 42
MAX_SEMESTRE = 8
rng = np.random.default_rng(SEED)


# ==========================================================
# 1. GERAÇÃO DOS VALORES ESPECÍFICOS
# ==========================================================
# Primeiro os valores brutos são gerados e só depois eles são discretizados.

# ----------------------------------------------------------
# 1. FREQUÊNCIA NAS AULAS
# Valor específico: 0 a 100 (%)
#
# Distribuição Beta para concentrar mais alunos em frequências
# intermediárias/altas, sem escolher a categoria antes.
# ----------------------------------------------------------

frequencia_percentual = np.round(rng.beta(4.5, 1.8, size=N) * 100).astype(int)
frequencia_percentual = np.clip(frequencia_percentual, 0, 100)


# ----------------------------------------------------------
# 2. MÉDIA DAS NOTAS
# Valor específico: 0.0 a 10.0
#
# Beta gera maior concentração na região central da escala,
# mas ainda permite notas muito baixas e muito altas.
# ----------------------------------------------------------

media_notas = np.round(rng.beta(3.8, 2.2, size=N) * 10, 1)
media_notas = np.clip(media_notas, 0, 10)


# ----------------------------------------------------------
# 3. DISCIPLINAS REPROVADAS
# Valor específico: 0 a 8
#
# Poisson produz muitos valores baixos e poucos valores altos,
# o que é mais natural do que todos terem a mesma chance.
# ----------------------------------------------------------

disciplinas_reprovadas = rng.poisson(lam=1.5, size=N)
disciplinas_reprovadas = np.clip(disciplinas_reprovadas, 0, 8)


# ----------------------------------------------------------
# 4. PARTICIPAÇÃO NAS ATIVIDADES
# Continua abstrata, pois não definimos uma medida numérica.
# ----------------------------------------------------------

participacao = rng.choice(["Baixa", "Média", "Alta"], size=N, p=[0.25, 0.45, 0.30])


# ----------------------------------------------------------
# 5. SITUAÇÃO FINANCEIRA
# Continua abstrata.
# ----------------------------------------------------------

situacao_financeira = rng.choice(["Dificuldade alta", "Dificuldade moderada", "Estável"], size=N, p=[0.23, 0.37, 0.40])


# ----------------------------------------------------------
# 6. CARGA DE TRABALHO
# Valor específico: 0 a 60 horas/semana
#
# A situação financeira influencia a distribuição das horas.
# Ainda assim, geramos primeiro o VALOR NUMÉRICO.
# Depois ele será discretizado.
# ----------------------------------------------------------

horas_trabalho = np.zeros(N, dtype=int)

# Dificuldade alta: maior chance de trabalhar e de possuir carga alta.
mascara = situacao_financeira == "Dificuldade alta"
qtd = mascara.sum()
trabalha = rng.random(qtd) < 0.95
valores = np.zeros(qtd, dtype=int)

# Entre quem trabalha: 32% até 30h / 68% acima de 30h.
tipo_carga = rng.random(trabalha.sum())
horas_de_quem_trabalha = np.where(tipo_carga < 0.32, rng.integers(1, 31, size=trabalha.sum()), rng.integers(31, 61, size=trabalha.sum()))
valores[trabalha] = horas_de_quem_trabalha
horas_trabalho[mascara] = valores

# Dificuldade moderada.
mascara = situacao_financeira == "Dificuldade moderada"
qtd = mascara.sum()
trabalha = rng.random(qtd) < 0.85
valores = np.zeros(qtd, dtype=int)
tipo_carga = rng.random(trabalha.sum())
horas_de_quem_trabalha = np.where(tipo_carga < 0.70, rng.integers(1, 31, size=trabalha.sum()), rng.integers(31, 61, size=trabalha.sum()))
valores[trabalha] = horas_de_quem_trabalha
horas_trabalho[mascara] = valores

# Estável.
mascara = situacao_financeira == "Estável"
qtd = mascara.sum()
trabalha = rng.random(qtd) < 0.45
valores = np.zeros(qtd, dtype=int)
tipo_carga = rng.random(trabalha.sum())
horas_de_quem_trabalha = np.where(tipo_carga < 0.78, rng.integers(1, 31, size=trabalha.sum()), rng.integers(31, 61, size=trabalha.sum()))
valores[trabalha] = horas_de_quem_trabalha
horas_trabalho[mascara] = valores


# ----------------------------------------------------------
# 7. PROGRESSO NO CURSO
# Valor específico: semestre atual
#
# Geramos diretamente o semestre com pesos próprios.
# ----------------------------------------------------------

semestres_possiveis = np.arange(1, MAX_SEMESTRE + 1)

# Pesos por semestre. A soma é normalizada automaticamente.
pesos_semestre = np.array([0.15, 0.14, 0.13, 0.12, 0.11, 0.10, 0.08, 0.07, 0.055, 0.045])
pesos_semestre = (pesos_semestre[:MAX_SEMESTRE] / pesos_semestre[:MAX_SEMESTRE].sum())
semestre_atual = rng.choice(semestres_possiveis, size=N,p=pesos_semestre)


# ----------------------------------------------------------
# 8. DESLOCAMENTO
# Continua abstrato.
# ----------------------------------------------------------

deslocamento = rng.choice(["Sem impacto", "Impacto moderado", "Impacto alto"], size=N, p=[0.45, 0.35, 0.20])


# ==========================================================
# 2. DISCRETIZAÇÃO A PARTIR DOS VALORES ESPECÍFICOS
# ==========================================================

# ----------------------------------------------------------
# FREQUÊNCIA
#
# Baixa: 0 a 69
# Média: 70 a 84
# Alta: 85 a 100
# ----------------------------------------------------------

grupo_frequencia = np.select([frequencia_percentual <= 69, frequencia_percentual <= 84], ["Baixa", "Média"], default="Alta")


# ----------------------------------------------------------
# NOTAS
#
# Baixa: 0 a 5.9
# Média: 6 a 7.9
# Alta: 8 a 10
# ----------------------------------------------------------

grupo_notas = np.select([media_notas < 6.0, media_notas < 8.0], ["Baixa", "Média"], default="Alta")


# ----------------------------------------------------------
# REPROVAÇÕES
#
# Baixa: 0 ou 1
# Média: 2 ou 3
# Alta: 4 ou mais
# ----------------------------------------------------------

grupo_reprovacoes = np.select([disciplinas_reprovadas <= 1, disciplinas_reprovadas <= 3], ["Baixa", "Média"], default="Alta")


# ----------------------------------------------------------
# CARGA DE TRABALHO
#
# Não trabalha: 0
# Até 30h: 1 a 30
# Mais de 30h: 31 a 60
# ----------------------------------------------------------

grupo_trabalho = np.select([horas_trabalho == 0, horas_trabalho <= 30], ["Não trabalha","Até 30h/semana"], default="Mais de 30h/semana")


# ----------------------------------------------------------
# PROGRESSO NO CURSO
#
# Inicial: 1º ou 2º semestre
# Intermediário: 3º ao 6º
# Final: 7º em diante
# ----------------------------------------------------------

grupo_progresso = np.select([semestre_atual <= 2, semestre_atual <= 6], ["Inicial", "Intermediário"], default="Final")


# ==========================================================
# 3. CÁLCULO DO RISCO A PARTIR DAS CATEGORIAS DISCRETIZADAS
# ==========================================================

score = np.zeros(N, dtype=float)

# Frequência
score += np.select([grupo_frequencia == "Alta", grupo_frequencia == "Média", grupo_frequencia == "Baixa"], [-1.0, 0.0, 1.0])

# Notas
score += np.select([grupo_notas == "Alta", grupo_notas == "Média", grupo_notas == "Baixa"], [-1.0, 0.0, 1.1])

# Reprovações
score += np.select([grupo_reprovacoes == "Baixa", grupo_reprovacoes == "Média", grupo_reprovacoes == "Alta"], [-0.8, 0.3, 1.2])

# Participação
score += np.select([participacao == "Alta", participacao == "Média", participacao == "Baixa"], [-1.0, 0.0, 1.0])

# Situação financeira
score += np.select([situacao_financeira == "Estável", situacao_financeira == "Dificuldade moderada", situacao_financeira == "Dificuldade alta"], [-0.6, 0.15, 0.9])

# Carga de trabalho
score += np.select([grupo_trabalho == "Não trabalha", grupo_trabalho == "Até 30h/semana", grupo_trabalho == "Mais de 30h/semana"], [-0.5, 0.0, 0.75])

# Progresso
score += np.select([grupo_progresso == "Inicial", grupo_progresso == "Intermediário", grupo_progresso == "Final"], [0.6, 0.0, -0.6])

# Deslocamento
score += np.select([deslocamento == "Sem impacto", deslocamento == "Impacto moderado", deslocamento == "Impacto alto"], [-0.4, 0.1, 0.6])


# ==========================================================
# 4. INTERAÇÕES ENTRE FEATURES
# ==========================================================

# Frequência baixa + notas baixas
score += ((grupo_frequencia == "Baixa") & (grupo_notas == "Baixa")) * 0.40

# Muitas reprovações no início do curso
score += ((grupo_reprovacoes == "Alta") & (grupo_progresso == "Inicial")) * 0.35

# Dificuldade financeira + alta carga de trabalho
score += ((situacao_financeira == "Dificuldade alta") & (grupo_trabalho == "Mais de 30h/semana")) * 0.35

# Impacto alto no deslocamento + alta carga de trabalho
score += ((deslocamento == "Impacto alto") & (grupo_trabalho == "Mais de 30h/semana")) * 0.25

# Frequência, nota e participação altas reduzem o risco
score -= ((grupo_frequencia == "Alta") & (grupo_notas == "Alta") & (participacao == "Alta")) * 0.35


# ==========================================================
# 5. PROBABILIDADE DE EVASÃO
# ==========================================================

prob_evasao = 1 / (1 + np.exp(-(-0.35 + 0.58 * score)))


# ==========================================================
# 6. CLASSE FINAL
# ==========================================================

abandona = np.where(rng.random(N) < prob_evasao, "Sim", "Não")


# ==========================================================
# 7. DATAFRAME COM VALORES ESPECÍFICOS
# ==========================================================

dados_especificos = pd.DataFrame({
    "Frequência_nas_aulas": frequencia_percentual,
    "Média_das_notas": media_notas,
    "Disciplinas_reprovadas": disciplinas_reprovadas,
    "Participação_nas_atividades": participacao,
    "Situação_financeira": situacao_financeira,
    "Carga_de_trabalho": horas_trabalho,
    "Progresso_no_curso": semestre_atual,
    "Deslocamento": deslocamento,
    "Abandona_até_o_próximo_semestre": abandona
})


# ==========================================================
# 8. DATAFRAME DISCRETIZADO
# ==========================================================

grupo_trabalho_sql = np.select([horas_trabalho == 0, horas_trabalho <= 30], ["Não trabalha", "Até 30h"], default="Mais de 30h")

dados_discretizados = pd.DataFrame({
    "Frequência_nas_aulas": grupo_frequencia,
    "Média_das_notas": grupo_notas,
    "Disciplinas_reprovadas": grupo_reprovacoes,
    "Participação_nas_atividades": participacao,
    "Situação_financeira": situacao_financeira,
    "Carga_de_trabalho": grupo_trabalho_sql,
    "Progresso_no_curso": grupo_progresso,
    "Deslocamento": deslocamento,
    "Abandona_até_o_próximo_semestre": abandona
})


# ==========================================================
# 9. SALVA OS CSVs
# ==========================================================

dados_especificos.to_csv("tabela_alunos_treino.csv", index=False, encoding="utf-8")
#dados_discretizados.to_csv("tabela_alunos_treino_discretizados.csv", index=False, encoding="utf-8")


# ==========================================================
# 10. VERIFICAÇÃO
# ==========================================================

print("Quantidade de registros:", N)
print("\nDistribuição da classe final:")
print((dados_discretizados["Abandona_até_o_próximo_semestre"].value_counts(normalize=True) * 100).round(2))