-- Limpeza inicial para evitar conflitos ao reexecutar
DROP VIEW IF EXISTS predicao_evasao CASCADE;
DROP VIEW IF EXISTS log_odds CASCADE;
DROP VIEW IF EXISTS aluno_novo_discretizado CASCADE;
DROP VIEW IF EXISTS alunos_treino_discretizado CASCADE;
DROP TABLE IF EXISTS aluno_novo CASCADE;
DROP TABLE IF EXISTS alunos_treino CASCADE;


-- 1. Tabela de Treino (Recebe valores numéricos/específicos)
CREATE TABLE alunos_treino (
    id SERIAL PRIMARY KEY,
    "Frequência_nas_aulas" NUMERIC,
    "Média_das_notas" NUMERIC(4,2),
    "Disciplinas_reprovadas" INT,
    "Participação_nas_atividades" VARCHAR(50),
    "Situação_financeira" VARCHAR(50),
    "Carga_de_trabalho" INT,
    "Progresso_no_curso" INT,
    "Deslocamento" VARCHAR(50),
    "Abandona_até_o_próximo_semestre" VARCHAR(10)
);


-- 2. Tabela de Novos Alunos (Recebe valores numéricos/específicos)
CREATE TABLE aluno_novo (
    id_aluno INT PRIMARY KEY,
    frequencia NUMERIC,
    media_notas NUMERIC(4,2),
    disciplinas_reprov INT,
    participacao VARCHAR(50),
    situacao_financeira VARCHAR(50),
    carga_trabalho INT,
    progresso_curso INT,
    deslocamento VARCHAR(50)
);


-- 3. View para Discretizar a Tabela de Treino
CREATE VIEW alunos_treino_discretizado AS
SELECT
    id,
    
    CASE 
        WHEN "Frequência_nas_aulas" BETWEEN 0 AND 69 THEN 'Baixa'
        WHEN "Frequência_nas_aulas" BETWEEN 70 AND 84 THEN 'Média'
        WHEN "Frequência_nas_aulas" >= 85 THEN 'Alta'
    END AS "Frequência_nas_aulas",

    CASE 
        WHEN "Média_das_notas" < 6.0 THEN 'Baixa'
        WHEN "Média_das_notas" BETWEEN 6.0 AND 7.99 THEN 'Média'
        WHEN "Média_das_notas" >= 8.0 THEN 'Alta'
    END AS "Média_das_notas",

    CASE 
        WHEN "Disciplinas_reprovadas" IN (0, 1) THEN 'Baixa'
        WHEN "Disciplinas_reprovadas" IN (2, 3) THEN 'Média'
        WHEN "Disciplinas_reprovadas" >= 4 THEN 'Alta'
    END AS "Disciplinas_reprovadas",

    "Participação_nas_atividades",
    "Situação_financeira",

    CASE 
        WHEN "Carga_de_trabalho" = 0 THEN 'Não trabalha'
        WHEN "Carga_de_trabalho" BETWEEN 1 AND 30 THEN 'Até 30h'
        WHEN "Carga_de_trabalho" > 30 THEN 'Mais de 30h'
    END AS "Carga_de_trabalho",

    CASE 
        WHEN "Progresso_no_curso" IN (1, 2) THEN 'Inicial'
        WHEN "Progresso_no_curso" BETWEEN 3 AND 6 THEN 'Intermediário'
        WHEN "Progresso_no_curso" >= 7 THEN 'Final'
    END AS "Progresso_no_curso",

    "Deslocamento",
    "Abandona_até_o_próximo_semestre"
FROM alunos_treino;


-- 4. View para Discretizar os Novos Alunos
CREATE VIEW aluno_novo_discretizado AS
SELECT
    id_aluno,
    
    CASE 
        WHEN frequencia BETWEEN 0 AND 69 THEN 'Baixa'
        WHEN frequencia BETWEEN 70 AND 84 THEN 'Média'
        WHEN frequencia >= 85 THEN 'Alta'
    END AS frequencia,

    CASE 
        WHEN media_notas < 6.0 THEN 'Baixa'
        WHEN media_notas BETWEEN 6.0 AND 7.99 THEN 'Média'
        WHEN media_notas >= 8.0 THEN 'Alta'
    END AS media_notas,

    CASE 
        WHEN disciplinas_reprov IN (0, 1) THEN 'Baixa'
        WHEN disciplinas_reprov IN (2, 3) THEN 'Média'
        WHEN disciplinas_reprov >= 4 THEN 'Alta'
    END AS disciplinas_reprov,

    participacao,
    situacao_financeira,

    CASE 
        WHEN carga_trabalho = 0 THEN 'Não trabalha'
        WHEN carga_trabalho BETWEEN 1 AND 30 THEN 'Até 30h'
        WHEN carga_trabalho > 30 THEN 'Mais de 30h'
    END AS carga_trabalho,

    CASE 
        WHEN progresso_curso IN (1, 2) THEN 'Inicial'
        WHEN progresso_curso BETWEEN 3 AND 6 THEN 'Intermediário'
        WHEN progresso_curso >= 7 THEN 'Final'
    END AS progresso_curso,

    deslocamento
FROM aluno_novo;


-- 5. View Log-Odds (Calculado a partir do Treino Discretizado)
CREATE VIEW log_odds AS
WITH Totais AS (
    SELECT
        SUM(CASE WHEN "Abandona_até_o_próximo_semestre" = 'Sim' THEN 1 ELSE 0 END) AS qnt_sim,
        SUM(CASE WHEN "Abandona_até_o_próximo_semestre" = 'Não' THEN 1 ELSE 0 END) AS qnt_nao
    FROM alunos_treino_discretizado
),
UnificacaoCategorias AS (
    SELECT 'Frequência_nas_aulas' AS feature, "Frequência_nas_aulas" AS categoria, "Abandona_até_o_próximo_semestre" AS classe FROM alunos_treino_discretizado
    UNION ALL
    SELECT 'Média_das_notas', "Média_das_notas", "Abandona_até_o_próximo_semestre" FROM alunos_treino_discretizado
    UNION ALL
    SELECT 'Disciplinas_reprovadas', "Disciplinas_reprovadas", "Abandona_até_o_próximo_semestre" FROM alunos_treino_discretizado
    UNION ALL
    SELECT 'Participação_nas_atividades', "Participação_nas_atividades", "Abandona_até_o_próximo_semestre" FROM alunos_treino_discretizado
    UNION ALL
    SELECT 'Situação_financeira', "Situação_financeira", "Abandona_até_o_próximo_semestre" FROM alunos_treino_discretizado
    UNION ALL
    SELECT 'Carga_de_trabalho', "Carga_de_trabalho", "Abandona_até_o_próximo_semestre" FROM alunos_treino_discretizado
    UNION ALL
    SELECT 'Progresso_no_curso', "Progresso_no_curso", "Abandona_até_o_próximo_semestre" FROM alunos_treino_discretizado
    UNION ALL
    SELECT 'Deslocamento', "Deslocamento", "Abandona_até_o_próximo_semestre" FROM alunos_treino_discretizado
),
Contagens AS (
    SELECT
        feature,
        categoria,
        SUM(CASE WHEN classe = 'Sim' THEN 1 ELSE 0 END) AS contagem_sim,
        SUM(CASE WHEN classe = 'Não' THEN 1 ELSE 0 END) AS contagem_nao
    FROM UnificacaoCategorias
    WHERE categoria IS NOT NULL
    GROUP BY feature, categoria
),
Probabilidades AS (
    SELECT
        c.feature,
        c.categoria,
        CAST(c.contagem_sim + 1 AS FLOAT) / (t.qnt_sim + 3) AS p_cond_sim,
        CAST(c.contagem_nao + 1 AS FLOAT) / (t.qnt_nao + 3) AS p_cond_nao
    FROM Contagens c
    CROSS JOIN Totais t
)
SELECT
    feature AS "Atributo",
    categoria AS "Categoria / Valor",
    ROUND(CAST(LN(p_cond_sim / p_cond_nao) AS NUMERIC), 4) AS "Log-Odds Ratio (Peso Evasão)"
FROM Probabilidades
ORDER BY "Log-Odds Ratio (Peso Evasão)" DESC;


-- 6. View Predição Naive Bayes (Compara Treino Discretizado vs Novos Alunos Discretizados)
CREATE VIEW predicao_evasao AS
WITH Totais AS (
    SELECT
        COUNT(*) AS total_geral,
        SUM(CASE WHEN "Abandona_até_o_próximo_semestre" = 'Sim' THEN 1 ELSE 0 END) AS qnt_sim,
        SUM(CASE WHEN "Abandona_até_o_próximo_semestre" = 'Não' THEN 1 ELSE 0 END) AS qnt_nao
    FROM alunos_treino_discretizado
),
Priori AS (
    SELECT
        CAST(qnt_sim AS FLOAT) / total_geral AS priori_sim,
        CAST(qnt_nao AS FLOAT) / total_geral AS priori_nao
    FROM Totais
),
ContagensFeatures AS (
    SELECT
        novo.id_aluno,
        SUM(CASE WHEN treino."Frequência_nas_aulas" = novo.frequencia AND treino."Abandona_até_o_próximo_semestre" = 'Sim' THEN 1 ELSE 0 END) AS frequencia_sim,
        SUM(CASE WHEN treino."Frequência_nas_aulas" = novo.frequencia AND treino."Abandona_até_o_próximo_semestre" = 'Não' THEN 1 ELSE 0 END) AS frequencia_nao,

        SUM(CASE WHEN treino."Média_das_notas" = novo.media_notas AND treino."Abandona_até_o_próximo_semestre" = 'Sim' THEN 1 ELSE 0 END) AS notas_sim,
        SUM(CASE WHEN treino."Média_das_notas" = novo.media_notas AND treino."Abandona_até_o_próximo_semestre" = 'Não' THEN 1 ELSE 0 END) AS notas_nao,

        SUM(CASE WHEN treino."Disciplinas_reprovadas" = novo.disciplinas_reprov AND treino."Abandona_até_o_próximo_semestre" = 'Sim' THEN 1 ELSE 0 END) AS reprovacoes_sim,
        SUM(CASE WHEN treino."Disciplinas_reprovadas" = novo.disciplinas_reprov AND treino."Abandona_até_o_próximo_semestre" = 'Não' THEN 1 ELSE 0 END) AS reprovacoes_nao,

        SUM(CASE WHEN treino."Participação_nas_atividades" = novo.participacao AND treino."Abandona_até_o_próximo_semestre" = 'Sim' THEN 1 ELSE 0 END) AS participacao_sim,
        SUM(CASE WHEN treino."Participação_nas_atividades" = novo.participacao AND treino."Abandona_até_o_próximo_semestre" = 'Não' THEN 1 ELSE 0 END) AS participacao_nao,

        SUM(CASE WHEN treino."Situação_financeira" = novo.situacao_financeira AND treino."Abandona_até_o_próximo_semestre" = 'Sim' THEN 1 ELSE 0 END) AS financeira_sim,
        SUM(CASE WHEN treino."Situação_financeira" = novo.situacao_financeira AND treino."Abandona_até_o_próximo_semestre" = 'Não' THEN 1 ELSE 0 END) AS financeira_nao,

        SUM(CASE WHEN treino."Carga_de_trabalho" = novo.carga_trabalho AND treino."Abandona_até_o_próximo_semestre" = 'Sim' THEN 1 ELSE 0 END) AS horasTrabalho_sim,
        SUM(CASE WHEN treino."Carga_de_trabalho" = novo.carga_trabalho AND treino."Abandona_até_o_próximo_semestre" = 'Não' THEN 1 ELSE 0 END) AS horasTrabalho_nao,

        SUM(CASE WHEN treino."Progresso_no_curso" = novo.progresso_curso AND treino."Abandona_até_o_próximo_semestre" = 'Sim' THEN 1 ELSE 0 END) AS progresso_sim,
        SUM(CASE WHEN treino."Progresso_no_curso" = novo.progresso_curso AND treino."Abandona_até_o_próximo_semestre" = 'Não' THEN 1 ELSE 0 END) AS progresso_nao,

        SUM(CASE WHEN treino."Deslocamento" = novo.deslocamento AND treino."Abandona_até_o_próximo_semestre" = 'Sim' THEN 1 ELSE 0 END) AS deslocamento_sim,
        SUM(CASE WHEN treino."Deslocamento" = novo.deslocamento AND treino."Abandona_até_o_próximo_semestre" = 'Não' THEN 1 ELSE 0 END) AS deslocamento_nao
    FROM aluno_novo_discretizado novo
    CROSS JOIN alunos_treino_discretizado treino
    GROUP BY novo.id_aluno
),
Verossimilhanca AS (
    SELECT
        cf.id_aluno,
        CAST(cf.frequencia_sim + 1 AS FLOAT) / (totais.qnt_sim + 3) AS p_frequencia_sim,
        CAST(cf.frequencia_nao + 1 AS FLOAT) / (totais.qnt_nao + 3) AS p_frequencia_nao,

        CAST(cf.notas_sim + 1 AS FLOAT) / (totais.qnt_sim + 3) AS p_notas_sim,
        CAST(cf.notas_nao + 1 AS FLOAT) / (totais.qnt_nao + 3) AS p_notas_nao,

        CAST(cf.reprovacoes_sim + 1 AS FLOAT) / (totais.qnt_sim + 3) AS p_reprovacoes_sim,
        CAST(cf.reprovacoes_nao + 1 AS FLOAT) / (totais.qnt_nao + 3) AS p_reprovacoes_nao,

        CAST(cf.participacao_sim + 1 AS FLOAT) / (totais.qnt_sim + 3) AS p_participacao_sim,
        CAST(cf.participacao_nao + 1 AS FLOAT) / (totais.qnt_nao + 3) AS p_participacao_nao,

        CAST(cf.financeira_sim + 1 AS FLOAT) / (totais.qnt_sim + 3) AS p_financeira_sim,
        CAST(cf.financeira_nao + 1 AS FLOAT) / (totais.qnt_nao + 3) AS p_financeira_nao,

        CAST(cf.horasTrabalho_sim + 1 AS FLOAT) / (totais.qnt_sim + 3) AS p_horasTrabalho_sim,
        CAST(cf.horasTrabalho_nao + 1 AS FLOAT) / (totais.qnt_nao + 3) AS p_horasTrabalho_nao,

        CAST(cf.progresso_sim + 1 AS FLOAT) / (totais.qnt_sim + 3) AS p_progresso_sim,
        CAST(cf.progresso_nao + 1 AS FLOAT) / (totais.qnt_nao + 3) AS p_progresso_nao,

        CAST(cf.deslocamento_sim + 1 AS FLOAT) / (totais.qnt_sim + 3) AS p_deslocamento_sim,
        CAST(cf.deslocamento_nao + 1 AS FLOAT) / (totais.qnt_nao + 3) AS p_deslocamento_nao
    FROM ContagensFeatures cf
    CROSS JOIN Priori priori
    CROSS JOIN Totais totais
),
Scores AS (
    SELECT
        vs.id_aluno,
        EXP(LN(priori.priori_sim) + LN(vs.p_frequencia_sim) + LN(vs.p_notas_sim) + LN(vs.p_reprovacoes_sim) + LN(vs.p_participacao_sim) + LN(vs.p_financeira_sim) + LN(vs.p_horasTrabalho_sim) + LN(vs.p_progresso_sim) + LN(vs.p_deslocamento_sim)) AS score_sim,
        EXP(LN(priori.priori_nao) + LN(vs.p_frequencia_nao) + LN(vs.p_notas_nao) + LN(vs.p_reprovacoes_nao) + LN(vs.p_participacao_nao) + LN(vs.p_financeira_nao) + LN(vs.p_horasTrabalho_nao) + LN(vs.p_progresso_nao) + LN(vs.p_deslocamento_nao)) AS score_nao
    FROM Verossimilhanca vs
    CROSS JOIN Priori priori
)
SELECT
    id_aluno AS "Aluno",
    ROUND(CAST((score_sim / (score_sim + score_nao)) * 100 AS NUMERIC), 2) AS "Probabilidade Evasão (%)",
    ROUND(CAST((score_nao / (score_sim + score_nao)) * 100 AS NUMERIC), 2) AS "Probabilidade Permanência (%)",
    CASE
        WHEN (score_sim / (score_sim + score_nao)) > 0.50 THEN '🚨 ALTO RISCO DE EVASÃO'
        ELSE '✅ BAIXO RISCO / PERMANÊNCIA'
    END AS "Situação Final"
FROM Scores
ORDER BY "Aluno" ASC;