# **Mineração de Dados - Atividade 1**

**Alunos:**
* Gabriel Siqueira Matias - `2023278440020`
* Pedro Alexandre Souza de Campos - `2023278440034`

---

## **1. Contexto**

Este trabalho consiste em uma aplicação prática do algoritmo **Naive Bayes**, uma variação do Teorema de Bayes utilizada para calcular a probabilidade de um evento com base em conhecimentos prévios e novas evidências. A principal característica do Naive Bayes é a independência condicional entre todas as *features*.

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

# 🎓 Sistema de Predição de Evasão Acadêmica (Naive Bayes no PostgreSQL)

Este projeto implementa um modelo preditivo de evasão escolar baseado no algoritmo **Naive Bayes** totalmente processado dentro do **PostgreSQL** através de **SQL Views**. O Python é utilizado para a geração dos dados sintéticos, carga no banco e exportação dos relatórios finais em CSV.

---

## 🚀 Como Executar o Projeto

### 1. Criar e Ativar o Ambiente Virtual (venv)

Recomenda-se utilizar um ambiente virtual para isolar as dependências do projeto.

#### **No Windows:**
```bash
# Criar o ambiente virtual
python -m venv venv

# Ativar o ambiente virtual
.\venv\Scripts\activate
```

#### **No Linux/macOS:**
```bash
# Criar o ambiente virtual
python3 -m venv venv

# Ativar o ambiente virtual
source venv/bin/activate
```

---

### 2. Instalar as Dependências

Com o ambiente virtual ativado, instale as bibliotecas necessárias:

```bash
pip install pandas numpy sqlalchemy psycopg2-binary
```

* **pandas**: Manipulação de dados e leitura/gravação de arquivos CSV.
* **numpy**: Geração de distribuições estatísticas para os dados de treino.
* **sqlalchemy**: Abstração de conexão com o banco de dados SQL.
* **psycopg2-binary**: Driver de comunicação entre Python e PostgreSQL.

---

### 3. Configurar a Conexão com o PostgreSQL

Antes de rodar o script principal, certifique-se de ter o **PostgreSQL** instalado e em execução na sua máquina.

1. Crie um banco de dados no PostgreSQL chamado **`dados_evasao`** (pode ser feito via `pgAdmin` ou SQL: `CREATE DATABASE dados_evasao;`).
2. Abra o arquivo **`main.py`** e ajuste as credenciais de conexão nas linhas iniciais conforme seu ambiente local:

```python
USER = "postgres"        # Seu usuário do PostgreSQL
PASSWORD = "1234"        # Sua senha do PostgreSQL
HOST = "localhost"       # Host onde o banco está rodando
PORT = "5432"            # Porta do PostgreSQL (padrão 5432)
DB_NAME = "dados_evasao" # Nome do banco de dados criado
```

---

### 4. Execução do Projeto

Siga a ordem abaixo para executar a geração de dados e o pipeline de predição:

```bash
# 1. Gerar os dados sintéticos de treino (1.000 alunos)
python gerador_alunos_treino.py

# 2. Gerar os dados sintéticos dos novos alunos a serem avaliados (100 alunos)
python gerador_alunos_novos.py

# 3. Executar o pipeline de carga, processamento SQL e exportação dos resultados
python main.py
```

---

## 📂 Estrutura dos Arquivos do Projeto

* **`gerador_alunos_treino.py`**:
  Gera a base histórica com 1.000 registros de alunos (`tabela_alunos_treino.csv`). Utiliza distribuições estatísticas como *Beta* (para notas e frequência) e *Poisson* (para reprovações) para criar cenários realistas e calcular probabilisticamente qual aluno abandona ou permanece no curso.

* **`gerador_alunos_novos.py`**:
  Gera a lista de novos alunos sem rótulo de evasão (`tabela_alunos_novos.csv`) que servirão de entrada para o modelo fazer as predições de risco.

* **`schema_e_view.sql`**:
  Arquivo contendo os scripts SQL de criação e modelagem do banco de dados:
  * **Tabelas**: `alunos_treino` e `aluno_novo` (criada com `CREATE TABLE IF NOT EXISTS` para preservar dados salvos quando não houver sobrescrita).
  * **Views de Discretização**: `alunos_treino_discretizado` e `aluno_novo_discretizado`, que categorizam variáveis contínuas em intervalos (*Baixa*, *Média*, *Alta*, etc.).
  * **View `log_odds`**: Calcula o peso de cada característica na probabilidade de evasão.
  * **View `predicao_evasao`**: Implementa o cálculo otimizado do Naive Bayes (usando probabilidades condicionais com suavização de Laplace e *Log-Scores*) para prever a probabilidade de evasão de cada novo aluno.

* **`main.py`**:
  Script central que gerencia o fluxo de trabalho. Ele verifica se o banco já está estruturado, pergunta ao usuário se deseja atualizar os dados mantendo ou sobrescrevendo tabelas (preservando `aluno_novo` quando a resposta for 'Não'), executa o script SQL e exporta os relatórios finais (`log_odds.csv` e `predicao_evasao.csv`).