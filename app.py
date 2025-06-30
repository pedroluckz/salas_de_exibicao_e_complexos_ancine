import streamlit as st
import sqlite3
import pandas as pd

conn = sqlite3.connect("salas-de-cinema.db")
st.set_page_config(page_title="Dashboard ANCINE", layout="wide")

st.title("🎬 Painel de Salas de Cinema - ANCINE")

# Sidebar com seções distintas
st.sidebar.header("📌 Consultas com SQL")
consulta_escolhida = st.sidebar.selectbox("Escolha:", [
    "Consulta 1: Salas com assento para cadeirante",
    "Consulta 2: Cinemas em funcionamento",
    "Consulta 3: Cinemas ativos em BH",
    "Consulta 4: Cinemas CINEMARK ativos",
    "Consulta 5: Cinemas independentes fechados na pandemia",
    "Consulta 6: Exibidores e endereços em BH",
    "Consulta 7: Quantidade de salas ativas em MG",
    "Consulta 8: Salas novas após 2023 e sem exibidor",
    "Consulta 9: Total de assentos CINEMARK",
    "Consulta 10: Média assentos de cadeirantes em MG"
])

if consulta_escolhida == "Consulta 1: Salas com assento para cadeirante":
    st.subheader("Consulta 1: Nome das salas em funcionamento que possuem pelo menos um assento para cadeirante")
    df = pd.read_sql("""
        SELECT S.NOME_SALA, E.UF_COMPLEXO
        FROM Sala S
        JOIN Cinema C ON S.REGISTRO_COMPLEXO = C.REGISTRO_COMPLEXO
        JOIN Endereco E ON C.ID_ENDERECO = E.ID_ENDERECO
        WHERE S.SITUACAO_SALA = "EM FUNCIONAMENTO" AND S.ASSENTOS_CADEIRANTES >= 1
    """, conn)
    st.dataframe(df, use_container_width=True)

elif consulta_escolhida == "Consulta 2: Cinemas em funcionamento":
    st.subheader("Consulta 2: Nome dos cinemas que estão funcionando")
    df = pd.read_sql("""
        SELECT NOME_COMPLEXO FROM CINEMA WHERE SITUACAO_COMPLEXO = "EM FUNCIONAMENTO"
    """, conn)
    st.dataframe(df, use_container_width=True)

elif consulta_escolhida == "Consulta 3: Cinemas ativos em BH":
    st.subheader("Consulta 3: Nome dos cinemas que estão em funcionamento na cidade de Belo Horizonte (MG)")
    df = pd.read_sql("""
        SELECT C.NOME_COMPLEXO
        FROM CINEMA C
        NATURAL JOIN ENDERECO E
        WHERE C.SITUACAO_COMPLEXO = "EM FUNCIONAMENTO" AND E.MUNICIPIO_COMPLEXO = "BELO HORIZONTE"
    """, conn)
    st.dataframe(df, use_container_width=True)

elif consulta_escolhida == "Consulta 4: Cinemas CINEMARK ativos":
    st.subheader("Consulta 4: Nome dos cinemas da exibidora CINEMARK que estão em funcionamento")
    df = pd.read_sql("""
        SELECT C.NOME_COMPLEXO
        FROM CINEMA C
        NATURAL JOIN EXIBIDORA EX
        WHERE C.SITUACAO_COMPLEXO = "EM FUNCIONAMENTO" AND EX.NOME_GRUPO_EXIBIDOR = "CINEMARK"
    """, conn)
    st.dataframe(df, use_container_width=True)

elif consulta_escolhida == "Consulta 5: Cinemas independentes fechados na pandemia":
    st.subheader("Consulta 5: Nome dos cinemas que 'NÃO PERTENCEM A NENHUM GRUPO EXIBIDOR'(ou seja a Exibidora não é uma franquia) que fecharam no período da pandemia ou no período imediatamente após (ou seja, fecharam no ano 2020, no ano 2021 ou no ano 2022)")
    df = pd.read_sql("""
        SELECT C.NOME_COMPLEXO
        FROM CINEMA C
        NATURAL JOIN EXIBIDORA EX
        WHERE C.SITUACAO_COMPLEXO = "FECHADO"
          AND EX.NOME_GRUPO_EXIBIDOR = "NÃO PERTENCE A NENHUM GRUPO EXIBIDOR"
          AND CAST(SUBSTR(C.DATA_SITUACAO_COMPLEXO, -4, 4) AS INTEGER) BETWEEN 2020 AND 2022
    """, conn)
    st.dataframe(df, use_container_width=True)

elif consulta_escolhida == "Consulta 6: Exibidores e endereços em BH":
    st.subheader("Consulta 6: Nome do grupo exibidor e Endereço dos cinemas que já operaram em Belo Horizinte (MG)")
    df = pd.read_sql("""
        SELECT DISTINCT EX.NOME_GRUPO_EXIBIDOR, EN.ENDERECO_COMPLEXO
        FROM EXIBIDORA EX
        NATURAL JOIN OPERACAO O
        NATURAL JOIN ENDERECO EN
        WHERE EN.MUNICIPIO_COMPLEXO = "BELO HORIZONTE"
        ORDER BY EX.NOME_GRUPO_EXIBIDOR
    """, conn)
    st.dataframe(df, use_container_width=True)

elif consulta_escolhida == "Consulta 7: Quantidade de salas ativas em MG":
    st.subheader("Consulta 7: Quantidade de salas de cinema em funcionamento em Minas Gerais")
    df = pd.read_sql("""
        SELECT COUNT(*) AS Total_Salas
        FROM SALA S
        NATURAL JOIN CINEMA C
        NATURAL JOIN ENDERECO EN
        WHERE S.SITUACAO_SALA = "EM FUNCIONAMENTO" AND EN.UF_COMPLEXO = "MG"
    """, conn)
    st.dataframe(df, use_container_width=True)

elif consulta_escolhida == "Consulta 8: Salas novas após 2023 e sem exibidor":
    st.subheader("Consulta 8: Nome das salas que não pertencem a nenhum grupo exibidor que abriram após o fim da pandemia (ou seja, após 2023)")
    df = pd.read_sql("""
        SELECT S.NOME_SALA
        FROM SALA S
        NATURAL JOIN CINEMA C
        NATURAL JOIN EXIBIDORA EX
        WHERE EX.NOME_GRUPO_EXIBIDOR = "NÃO PERTENCE A NENHUM GRUPO EXIBIDOR"
          AND CAST(SUBSTR(S.DATA_INICIO_FUNCIONAMENTO_SALA, -4, 4) AS INTEGER) >= 2023
    """, conn)
    st.dataframe(df, use_container_width=True)

elif consulta_escolhida == "Consulta 9: Total de assentos CINEMARK":
    st.subheader("Consulta 9: Somatório do número de assentos em todos os cinemas do grupo exibidor CINEMARK no país")
    df = pd.read_sql("""
        SELECT SUM(S.ASSENTOS_SALA) AS Total_Assentos
        FROM SALA S
        NATURAL JOIN CINEMA C
        NATURAL JOIN EXIBIDORA EX
        WHERE EX.NOME_GRUPO_EXIBIDOR = "CINEMARK" AND S.SITUACAO_SALA = "EM FUNCIONAMENTO"
    """, conn)
    st.dataframe(df, use_container_width=True)

elif consulta_escolhida == "Consulta 10: Média assentos de cadeirantes em MG":
    st.subheader("Consulta 10: Quantidade média de assentos de cadeirantes nas salas de cinemas no estado de Minas Gerais")
    df = pd.read_sql("""
        SELECT AVG(S.ASSENTOS_CADEIRANTES) AS Media_Cadeirantes
        FROM SALA S
        NATURAL JOIN CINEMA C
        NATURAL JOIN ENDERECO E
        WHERE S.SITUACAO_SALA = "EM FUNCIONAMENTO" AND E.UF_COMPLEXO = "MG"
    """, conn)
    st.dataframe(df, use_container_width=True)



st.sidebar.header("📋 Consultas Gerais")
consulta_geral = st.sidebar.selectbox("Escolha:", [
    "Visualizar Exibidoras",
    "Visualizar Cinemas",
    "Visualizar Salas",
    "Estatísticas"
])


# Separador
st.markdown("---")

# Consulta geral 
st.subheader(f"📄 Resultado da Consulta Geral: {consulta_geral}")

if consulta_geral == "Visualizar Exibidoras":
    df = pd.read_sql("SELECT * FROM Exibidora", conn)
    st.dataframe(df, use_container_width=True)

elif consulta_geral == "Visualizar Cinemas":
    df = pd.read_sql("SELECT * FROM Cinema NATURAL JOIN Endereco", conn)
    st.dataframe(df, use_container_width=True)

elif consulta_geral == "Visualizar Salas":
    df = pd.read_sql("SELECT * FROM Sala", conn)
    st.dataframe(df, use_container_width=True)

elif consulta_geral == "Estatísticas":
    estats = pd.read_sql("""
        SELECT E.UF_COMPLEXO, COUNT(S.REGISTRO_SALA) AS Total_Salas,
               SUM(S.ASSENTOS_SALA) AS Total_Assentos
        FROM Sala S
        JOIN Cinema C ON S.REGISTRO_COMPLEXO = C.REGISTRO_COMPLEXO
        JOIN Endereco E ON C.ID_ENDERECO = E.ID_ENDERECO
        GROUP BY E.UF_COMPLEXO
        ORDER BY Total_Salas DESC
    """, conn)
    st.dataframe(estats, use_container_width=True)
    st.bar_chart(estats.set_index("UF_COMPLEXO")[["Total_Salas"]])
