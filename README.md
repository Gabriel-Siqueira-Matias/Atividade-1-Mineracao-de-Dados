# **Mineração de Dados - Atividade 1**

**Alunos:**
* Gabriel Siqueira Matias - `2023278440020`
* Pedro Alexandre Souza de Campos - `2023278440034`

---

## **1. Contexto**

Este trabalho consiste em uma aplicação prática do algoritmo **Naive Bayes** — uma variação do Teorema de Bayes utilizada para calcular a probabilidade de um evento com base em conhecimentos prévios e novas evidências. A principal característica do Naive Bayes é a premissa de independência condicional entre todas as *features* (atributos).

O domínio analisado é o **Educacional**, com foco em prever a **probabilidade de evasão acadêmica** (se um aluno deixará o curso até o próximo semestre).

---

## **2. Atributos do Modelo (Features)**

### **Explicação das Features**

| Feature | Explicação |
| :--- | :--- |
| **Frequência nas aulas** | Alunos com alto índice de faltas tendem a demonstrar desmotivação ou dificuldades de acompanhamento. |
| **Média das notas** | Desempenho acadêmico baixo é um indicador direto de risco de desistência. |
| **Disciplinas reprovadas** | O acúmulo de reprovações atrasa a integralização curricular e gera desmotivação. |
| **Participação nas atividades** | Baixo engajamento em trabalhos e tarefas sinaliza menor vínculo com o curso. |
| **Situação financeira** | Instabilidade financeira frequentemente exige priorização do trabalho em detrimento dos estudos. |
| **Carga de trabalho** | Horas semanais de trabalho elevadas reduzem o tempo disponível para estudo. |
| **Progresso no curso** | Alunos nos semestres iniciais possuem maior taxa de evasão comparados aos concluintes. |
| **Deslocamento** | Dificuldades de logística e transporte podem impactar a assiduidade e retenção. |

---

### **Regras de Discretização**

| Feature | Valores Brutos (Específicos) | Categorias Discretizadas |
| :--- | :--- | :--- |
| **Frequência nas aulas** | `0%` a `100%` | **Baixa:** `< 70%` <br> **Média:** `70% – 84%` <br> **Alta:** `≥ 85%` |
| **Média das notas** | `0.0` a `10.0` | **Baixa:** `< 6.0` <br> **Média:** `6.0 – 7.9` <br> **Alta:** `≥ 8.0` |
| **Disciplinas reprovadas** | `0` a `8+` | **Baixa:** `0 – 1` <br> **Média:** `2 – 3` <br> **Alta:** `≥ 4` |
| **Participação nas atividades** | *Qualitativo* | `Baixa` \| `Média` \| `Alta` |
| **Situação financeira** | *Qualitativo* | `Dificuldade alta` \| `Dificuldade moderada` \| `Estável` |
| **Carga de trabalho** | `0` a `60` horas/semana | **Não trabalha:** `0h` <br> **Até 30h:** `1 – 30h` <br> **Mais de 30h:** `> 30h` |
| **Progresso no curso** | `1º` ao `10º` semestre | **Inicial:** `1º – 2º sem.` <br> **Intermediário:** `3º – 6º sem.` <br> **Final:** `≥ 7º sem.` |
| **Deslocamento** | *Qualitativo* | `Sem impacto` \| `Impacto moderado` \| `Impacto alto` |

---

## **3. Arquitetura da Solução**

1. **Geração de Dados:** Scripts em Python (`NumPy`/`Pandas`) geram dados sintéticos com valores numéricos contínuos/específicos.
2. **Carga no PostgreSQL:** Inserção direta dos dados brutos nas tabelas `alunos_treino` e `aluno_novo`.
3. **Discretização via SQL:** Views no PostgreSQL (`alunos_treino_discretizado` e `aluno_novo_discretizado`) aplicam a lógica de categorização dinamicamente.
4. **Modelagem & Predição:** Views dedicadas calculam a matriz de **Log-Odds** e realizam a classificação por **Naive Bayes** (Laplace Smoothing).