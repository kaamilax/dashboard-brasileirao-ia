import pandas as pd
import streamlit as st 
import plotly.express as px 

st.set_page_config(page_title="Dashboard Brasileirão", layout="wide")

st.title("Dashboard dos Clubes do Brasileirão")

df = pd.read_csv("COMPONENTS/Tabela_Clubes.csv")
df = df.loc[:, ~df.columns.str.contains("^Unnamed")]

st.sidebar.title("Side-Bar")
st.sidebar.markdown("Filtrar: ")

df = df.rename(columns={
    "Pos.": "Posicao",
    "Clubes": "Clube"
})


anos = sorted(df["Ano"].unique())
anos_selecionados = st.sidebar.multiselect(
    "Selecione o(s) ano(s):",
    anos,
    default=anos
)


clubes = sorted(df["Clube"].unique())
clubes_selecionados = st.sidebar.multiselect(
    "Selecione o(s) clube(s):",
    clubes,
    default=clubes
)


df_filtrado = df[
    (df["Ano"].isin(anos_selecionados)) &
    (df["Clube"].isin(clubes_selecionados))
]

col1, col2, col3 = st.columns(3)

col1.metric("Clubes analisados", df_filtrado["Clube"].nunique())
col2.metric("Vitórias médias", round(df_filtrado["Vitorias"].mean(), 2))
col3.metric("Valor médio do elenco", round(df_filtrado["Valor_total"].mean(), 2))

st.divider()

ranking_pos = (df_filtrado.groupby("Clube", as_index=False)["Posicao"].mean().sort_values("Posicao").head(10))

fig1 = px.bar(
    ranking_pos.sort_values("Posicao", ascending=False),
    x="Posicao",
    y="Clube",
    orientation="h",
    title="Top 10 clubes por melhor posição média"
)

ranking_vitorias = (
    df_filtrado.groupby("Clube", as_index=False)["Vitorias"]
    .sum()
    .sort_values("Vitorias", ascending=False)
    .head(10)
)

fig2 = px.bar(
    ranking_vitorias.sort_values("Vitorias"),
    x="Vitorias",
    y="Clube",
    orientation="h",
    title="Top 10 clubes por vitórias"
)

c1, c2 = st.columns(2)
c1.plotly_chart(fig1, use_container_width=True)
c2.plotly_chart(fig2, use_container_width=True)


st.subheader("Tabela: ")
st.dataframe(df_filtrado, use_container_width=True)
