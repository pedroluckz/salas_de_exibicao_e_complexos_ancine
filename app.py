import streamlit as st
import sqlite3
import pandas as pd

# Conectar ao banco de dados
conn = sqlite3.connect("salas-de-cinema.db")

st.set_page_config(page_title="Salas de Cinema - ANCINE", layout="wide")
st.title("🎬 Visualização de Salas de Cinema - ANCINE")

st.markdown("Este painel exibe consultas SQL e estatísticas a partir dos dados da ANCINE sobre salas de cinema no Brasil.")

st.subheader("🔎 Consultas Específicas em SQL")

consultas = {
    "Consulta 1: Salas com assento para cadeirante": """
        SELECT S.NOME_SALA, E.UF_COMPLEXO
        FROM Sala S
        JOIN Cinema C ON S.REGISTRO_COMPLEXO = C.REGISTRO_COMPLEXO
        JOIN Endereco E ON C.ID_ENDERECO = E.ID_ENDERECO
        WHERE S.SITUACAO_SALA = 'EM FUNCIONAMENTO' AND S.ASSENTOS_CADEIRANTES >= 1
    """,
    "Consulta 2: Cinemas em funcionamento": """
        SELECT NOME_COMPLEXO FROM CINEMA WHERE SITUACAO_COMPLEXO = 'EM FUNCIONAMENTO'
    """,
    "Consulta 3: Cinemas ativos em Belo Horizonte (MG)": """
        SELECT C.NOME_COMPLEXO
        FROM CINEMA C NATURAL JOIN ENDERECO E
        WHERE C.SITUACAO_COMPLEXO = 'EM FUNCIONAMENTO' AND E.MUNICIPIO_COMPLEXO = 'BELO HORIZONTE'
    """,
    "Consulta 4: Cinemas da CINEMARK em funcionamento": """
        SELECT C.NOME_COMPLEXO
        FROM CINEMA C NATURAL JOIN EXIBIDORA EX
        WHERE C.SITUACAO_COMPLEXO = 'EM FUNCIONAMENTO' AND EX.NOME_GRUPO_EXIBIDOR = 'CINEMARK'
    """,
    "Consulta 5: Cinemas independentes fechados na pandemia": """
        SELECT C.NOME_COMPLEXO
        FROM CINEMA C NATURAL JOIN EXIBIDORA EX
        WHERE C.SITUACAO_COMPLEXO = 'FECHADO'
        AND EX.NOME_GRUPO_EXIBIDOR = 'NÃO PERTENCE A NENHUM GRUPO EXIBIDOR'
        AND CAST(SUBSTR(C.DATA_SITUACAO_COMPLEXO, -4, 4) AS INTEGER) BETWEEN 2020 AND 2022
    """,
    "Consulta 6: Grupos exibidores e endereços em BH": """
        SELECT DISTINCT EX.NOME_GRUPO_EXIBIDOR, EN.ENDERECO_COMPLEXO
        FROM EXIBIDORA EX NATURAL JOIN OPERACAO O NATURAL JOIN ENDERECO EN
        WHERE EN.MUNICIPIO_COMPLEXO = 'BELO HORIZONTE'
        ORDER BY EX.NOME_GRUPO_EXIBIDOR
    """,
    "Consulta 7: Qtd. de salas ativas em MG": """
        SELECT COUNT(*) AS Total_Salas
        FROM SALA S NATURAL JOIN CINEMA C NATURAL JOIN ENDERECO EN
        WHERE S.SITUACAO_SALA = 'EM FUNCIONAMENTO' AND EN.UF_COMPLEXO = 'MG'
    """,
    "Consulta 8: Salas novas após 2023 e sem grupo exibidor": """
        SELECT S.NOME_SALA
        FROM SALA S NATURAL JOIN CINEMA C NATURAL JOIN EXIBIDORA EX
        WHERE EX.NOME_GRUPO_EXIBIDOR = 'NÃO PERTENCE A NENHUM GRUPO EXIBIDOR'
        AND CAST(SUBSTR(S.DATA_INICIO_FUNCIONAMENTO_SALA, -4, 4) AS INTEGER) >= 2023
    """,
    "Consulta 9: Total de assentos da CINEMARK": """
        SELECT SUM(S.ASSENTOS_SALA) AS Total_Assentos
        FROM SALA S NATURAL JOIN CINEMA C NATURAL JOIN EXIBIDORA EX
        WHERE EX.NOME_GRUPO_EXIBIDOR = 'CINEMARK' AND S.SITUACAO_SALA = 'EM FUNCIONAMENTO'
    """,
    "Consulta 10: Média de assentos para cadeirantes em MG": """
        SELECT AVG(S.ASSENTOS_CADEIRANTES) AS Media_Cadeirantes
        FROM SALA S NATURAL JOIN CINEMA C NATURAL JOIN ENDERECO E
        WHERE S.SITUACAO_SALA = 'EM FUNCIONAMENTO' AND E.UF_COMPLEXO = 'MG'
    """
}

for titulo, sql in consultas.items():
    with st.expander(titulo, expanded=False):
        df = pd.read_sql(sql, conn)
        st.dataframe(df, use_container_width=True)

# Seção lateral com opções
st.sidebar.title("📂 Navegação")
opcao = st.sidebar.selectbox("Consultas gerais:", [
    "Visualizar Exibidoras",
    "Visualizar Cinemas",
    "Visualizar Salas",
    "Estatísticas"
])

st.subheader("📄 Resultado da Consulta Geral")

if opcao == "Visualizar Exibidoras":
    st.markdown("### 🎥 Exibidoras Registradas")
    df = pd.read_sql("SELECT * FROM Exibidora", conn)
    st.dataframe(df)

elif opcao == "Visualizar Cinemas":
    st.markdown("### 🏢 Cinemas e seus Endereços")
    df = pd.read_sql("SELECT * FROM Cinema NATURAL JOIN Endereco", conn)
    st.dataframe(df)

elif opcao == "Visualizar Salas":
    st.markdown("### 🎟️ Salas de Exibição")
    df = pd.read_sql("SELECT * FROM Sala", conn)
    st.dataframe(df)

elif opcao == "Estatísticas":
    st.markdown("### 📊 Estatísticas por UF")
    estats = pd.read_sql("""
        SELECT E.UF_COMPLEXO, COUNT(S.REGISTRO_SALA) AS Total_Salas,
               SUM(S.ASSENTOS_SALA) AS Total_Assentos
        FROM Sala S
        JOIN Cinema C ON S.REGISTRO_COMPLEXO = C.REGISTRO_COMPLEXO
        JOIN Endereco E ON C.ID_ENDERECO = E.ID_ENDERECO
        GROUP BY E.UF_COMPLEXO
        ORDER BY Total_Salas DESC
    """, conn)
    st.dataframe(estats)
    st.bar_chart(estats.set_index("UF_COMPLEXO")[["Total_Salas"]])
