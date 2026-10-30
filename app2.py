from dash import Dash,html, dcc, Input, Output, State
import dash_bootstrap_components as dbc
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
from dash_bootstrap_templates import load_figure_template
from dash.exceptions import PreventUpdate
import dash_mantine_components as dmc
from dash import dash_table
from assistent_IA import quest_timeWithMoreVictory, result_quest

df = pd.read_csv("COMPONENTS/Tabela_Clubes.csv")

df = df.dropna(axis=1, how="all")

df = df.loc[:, ~df.columns.str.contains("^Unnamed")]

df = df.rename(columns={
    "Pos.": "Posicao", 
    "Clubes": "Clube"
})

anos = sorted(df["Ano"].unique())
clubes = sorted(df["Clube"].unique())


app = Dash(__name__, external_stylesheets=[dbc.themes.FLATLY])
load_figure_template("flatly")

SIDEBAR_STYLE = {
    "position": "fixed",
    "top": 0,
    "left":0, 
    "bottom": 0, 
    "width": "250px",
    "padding": "20px",
    "background": "linear-gradient(180deg, #1E293B 0%, #0F172A 100%)",
    "boxShadow": "4px 0 15px rgba(0,0,0,0.25)",
}

CONTENT_STYLE = { 
    "marginLeft": "270px", 
    "padding": "20px",    
    "backgroundColor":"#F5F7FA", 
    "minHeight": "100vh"                   
}


nav_style = {
    "color": "white",
    "fontSize": "18px",
    "marginBottom": "10px",
    "borderRadius": "10px",
}


sidebar = html.Div(
    [
        html.H2("Futebol Dashboard", style={"color": "white", "textAlign": "center", "marginBotton": "40px"}), 
        
        dbc.Nav([
            dbc.NavLink("Home", href="/", style={
                "color": "white",
                "fontSize": "18px",
                "marginBottom": "10px",
                "borderRadius": "10px",}), 
            
            dbc.NavLink("Gols", href="/gols", style={
                "color": "white",
                "fontSize": "18px",
                "marginBottom": "10px",
                "borderRadius": "10px",}),
                
            dbc.NavLink("Times", href="/times", style={
                "color": "white",
                "fontSize": "18px",
                "marginBottom": "10px",
                "borderRadius": "10px",}),
            
            dbc.NavLink("Geral", href="/geral", style={
                "color": "white",
                "fontSize": "18px",
                "marginBottom": "10px",
                "borderRadius": "10px",})
            
        ], vertical=True, pills=True)
        
    ], style= SIDEBAR_STYLE,
)

def make_kpi_card(title, card_id): 
    return dbc.Card(
        dbc.CardBody([
            html.H6(title, className="text-muted"), 
            html.H3(id=card_id, className="fw-bold")
        ]), 
        style={
            "borderRadius": "14px",
            "boxShadow": "0 4px 12px rgba(0,0,0,0.08)"
        }
    )

filtros_card = dbc.Card(
    dbc.CardBody([
        html.H4("Filtros", className="mb-3"), 
    
    html.Label("Ano", className="fw-bold"), 
    dcc.Dropdown(
        id="filtro-ano", 
        options=[{"label": str(ano), "value":ano} for ano in anos], 
        value=anos, 
        multi=True, 
        placeholder="Selecione o(s) ano(s)"
    ), 
    
    html.Br(),
    
    html.Label("Clube", className="fw-bold"),
    dcc.Dropdown(
        id="filtro-clube", 
        options=[{"label":clube,"value": clube} for clube in clubes], 
        value=clubes, 
        multi=True, 
        placeholder="Selecione o(s) clube(s)"
        
        ), 
    ]), 
    style={
        "borderRadius": "14px", 
        "boxShadow": "0 4px 12px rgba(0,0,0,0.08)", 
        "height": "100%"
    }
)

content = html.Div([
    
    html.H1("Dashboard dos Clubes do Brasileirão", style={"marginBottom": "20px"}), 
    
    dbc.Row(
            [
                dbc.Col(make_kpi_card("Clubes analisados", "kpi-clubes"), md=4),
                dbc.Col(make_kpi_card("Vitórias médias", "kpi-vitorias"), md=4),
                dbc.Col(make_kpi_card("Valor médio do elenco", "kpi-valor"), md=4),
            ],
            className="mb-4"
        ),
    
    dbc.Row(
            [
                dbc.Col(filtros_card, md=3),
                dbc.Col(dcc.Graph(id="grafico-posicao"), md=9),
            ],
            className="mb-4"
        ),
    
    dbc.Row(
            [
                dbc.Col(dcc.Graph(id="grafico-vitorias"), md=12),
            ],
            className="mb-4"
        ),
    
    html.H4("Tabela", style={"marginTop": "20px"}),
    
    dash_table.DataTable(
            id="tabela-dados",
            page_size=10,
            style_table={"overflowX": "auto"},
            style_cell={
                "textAlign": "left",
                "padding": "10px",
                "fontFamily": "Arial",
                "fontSize": "14px"
            },
            style_header={
                "backgroundColor": "#E9ECEF",
                "fontWeight": "bold"
            }
        )
    
], style=CONTENT_STYLE)




app.layout = html.Div([
    sidebar, content, 
    
    dcc.Store(
    id="historico-mensagens",
    data=[]
),
    
    html.Button(
    "💬",
    id="botao-chat",
    n_clicks=0
),

html.Div(
    id="window-chat",
    children=[

        html.Div(
            [
                html.H5("Assistente do Brasileirão"),

                html.Button(
                    "X",
                    id="close-chat",
                    n_clicks=0
                )
            ],
            className="chat-header"
        ),

        html.Div(
            id="historico-chat",
            children=[
                html.P(
                    "Olá! Sou o seu assistente pessoal do Brasileirão. Como posso ajudar?",
                    className="mensagem-ia"
                )
            ],
            className="chat-messages"
        ),

        html.Div(
            [
                dcc.Input(
                    id="entrada-chat",
                    type="text",
                    placeholder="Digite sua pergunta aqui",
                    className="chat-input"
                ),

                html.Button(
                    "➤",
                    id="enviar-chat",
                    n_clicks=0,
                    className="chat-send"
                )
            ],
            className="chat-footer"
        )

    ],
    style={"display": "none"}
)
    
])

@app.callback(
    Output("kpi-clubes", "children"), 
    Output("kpi-vitorias", "children"),
    Output("kpi-valor", "children"),
    Output("grafico-posicao", "figure"),
    Output("grafico-vitorias", "figure"),
    Output("tabela-dados", "data"),
    Output("tabela-dados", "columns"),
    Input("filtro-ano", "value"),
    Input("filtro-clube", "value"),
    
    
)



def atualizar_dashboard(anos_selecionados, clubes_selecionados): 
    
    df_filtrado = df[
        (df["Ano"].isin(anos_selecionados)) & 
        (df["Clube"].isin(clubes_selecionados))
    ]
    
    clubes_analisados = df_filtrado["Clube"].nunique()
    vitorias_medias = round(df_filtrado["Vitorias"].mean(), 2) if not df_filtrado.empty else 0
    valor_medio = round(df_filtrado["Valor_total"].mean(), 2) if not df_filtrado.empty else 0
    
    ranking_pos = (
        df_filtrado.groupby("Clube", as_index=False)["Posicao"]
        .mean()
        .sort_values("Posicao")
        .head(10)
    )
    
    fig1 = px.bar(
        ranking_pos.sort_values("Posicao", ascending=False),
        x="Posicao",
        y="Clube",
        orientation="h",
        title="Top 10 clubes por melhor posição média",
        text="Posicao"
    )

    fig1.update_layout(title_x=0.5)

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
        title="Top 10 clubes por vitórias",
        text="Vitorias"
    )
    
    fig2.update_layout(title_x=0.5)

    data = df_filtrado.to_dict("records")
    columns = [{"name": col, "id": col} for col in df_filtrado.columns]

    return clubes_analisados, vitorias_medias, valor_medio, fig1, fig2, data, columns


@app.callback(
    Output("window-chat", "style"),
    Input("botao-chat", "n_clicks"),
    Input("close-chat", "n_clicks")
)

def controller_chat(abrir, fechar):
    if abrir > fechar:
        return {"display":"flex"}

    return {"display":"none"}

@app.callback(
    Output("historico-chat", "children"),
    Output("historico-mensagens", "data"),
    Output("entrada-chat", "value"),
    Input("enviar-chat", "n_clicks"),
    State("entrada-chat", "value"),
    State("historico-mensagens", "data"),
    State("filtro-ano", "value"),
    State("filtro-clube", "value"),
    prevent_initial_call=True
)
def enviar_mensagem(n_clicks, mensagem, historico,
                    anos_selecionados, clubes_selecionados):

    if not mensagem or not mensagem.strip():
        raise PreventUpdate

    historico = historico or []

    historico.append({
        "tipo": "usuario",
        "texto": mensagem
    })

    try:
        df_filtrado = df[
            (df["Ano"].isin(anos_selecionados or [])) &
            (df["Clube"].isin(clubes_selecionados or []))
        ]

        if  any(palavra in mensagem.lower() for palavra in [
            "vitória", "vitórias", "vitoria", "vitorias", "venceu", "venceram", "ganhou", "ganharam", "mais partidas"
        ]):

            resultado = quest_timeWithMoreVictory(df_filtrado)

            resposta = result_quest(mensagem, resultado)

        else:
            resposta = (
                "Por enquanto, consigo responder perguntas "
                "sobre o clube com mais vitórias. "
                "Em breve terei mais funcionalidades!"
            )

    except Exception as erro:
        print("Erro no Gemini:", erro)
        resposta = "Não consegui processar sua pergunta. Tente novamente."

    historico.append({
        "tipo": "ia",
        "texto": resposta
    })

    mensagens = []

    for item in historico:
        classe = (
            "mensagem-usuario"
            if item["tipo"] == "usuario"
            else "mensagem-ia"
        )

        mensagens.append(
            html.P(item["texto"], className=classe)
        )

    return mensagens, historico, ""



if __name__ == "__main__":
    app.run()