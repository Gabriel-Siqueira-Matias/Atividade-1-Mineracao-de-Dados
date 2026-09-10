# **Mineração de Dados - Atividade 1**

&nbsp;&nbsp;&nbsp;**Alunos:**  
&nbsp;&nbsp;&nbsp;&nbsp; Gabriel Siqueira Matias - 2023278440020  
&nbsp;&nbsp;&nbsp;&nbsp; Pedro Alexandre Souza de Campos - 2023278440034  
<br>
<br>
# **1 - Contexto**

&nbsp;&nbsp;&nbsp;&nbsp;Esse trabalho se trata de uma aplicação prática do algoritmo Naive Bayes, o qual se trata de uma variação do Teorema de Bayes, o qual é uma fórmula matemática usada para calcular a probabilidade de um evento acontecer com base em conhecimentos prévios e novas evidências, a diferença entre o Teorema de Bayes e o algoritmo Naive Bayes, é que o algoritmo trata cada feature como independente entre elas.

&nbsp;&nbsp;&nbsp;&nbsp;O domínio usado foi educação, no caso, analisar a possibilidade de um aluno de um determinado curso deixar o mesmo até o próximo semestre.

---
**As features e sua explicação:**

| Feature | Explicação |
| :--- | :--- |
| **Participação nas atividades** | Um aluno que entrega poucos trabalhos ou participa pouco tende a demonstrar menor envolvimento com o curso. |
| **Situação financeira** | Problemas financeiros podem fazer com que o aluno precise trabalhar mais ou até abandonar os estudos. |
| **Carga de trabalho do aluno** | Quanto maior a carga de trabalho, menor pode ser o tempo disponível para estudar e frequentar as aulas. |
| **Progresso no curso** | Alunos no início do curso podem ter maior facilidade para desistir, enquanto quem está próximo de concluir tende a permanecer. |
| **Frequência nas aulas** | Alunos que começam a faltar muito podem estar desmotivados ou com dificuldades para continuar o curso. |
| **Média das notas** | Notas muito baixas podem indicar dificuldade acadêmica, aumentando a chance de desistência. |
| **Quantidade de disciplinas reprovadas** | Muitas reprovações atrasam a formação e podem causar desmotivação. |

---
**As features e sua discretização:**
| Feature | Discretização |
| :--- | :--- |
| **Participação nas atividades** | Alta &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;/ Média &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;/ Baixa |
| **Situação financeira** | Estável &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;/ Dificuldade moderada &nbsp;&nbsp;&nbsp;/ Alta dificuldade |
| **Carga de trabalho do aluno** | Não trabalha &nbsp;&nbsp;&nbsp;&nbsp;/ Até 30h/semana &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;/ Mais de 30h/semana |
| **Progresso no curso** | Inicial (0–25%) / Intermediário (26–75%) &nbsp;/ Final (>75%) |
| **Frequência nas aulas** | Alta: ≥ 85% &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;/ Média: 70–84% &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;/ Baixa: &lt; 70% |
| **Média das notas** | Alta: ≥ 8 &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;/ Média: 6–7,9 &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;/ Baixa: &lt; 6 |
| **Quantidade de disciplinas reprovadas** | Nenhuma &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;/ 1–2 &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;/ 3 ou mais |