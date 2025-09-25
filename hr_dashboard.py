import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import dash
from dash import dcc, html, Input, Output, callback
import numpy as np

# Load and prepare data - handle CSV parsing issues
# no index column in the CSV
df = pd.read_csv("data/rh_construtora_dataset.csv", index_col=False, sep=",")

# Clean and convert date columns with proper error handling
# add format error coercion to handle invalid dates in the dataset YYYY-MM-DD
df["data_admissao"] = pd.to_datetime(df["data_admissao"], format="%Y-%m-%d")
df["data_demissao"] = pd.to_datetime(df["data_demissao"], format="%Y-%m-%d")

# Clean numeric columns
df["salario"] = pd.to_numeric(df["salario"], errors="coerce")
df["idade"] = pd.to_numeric(df["idade"], errors="coerce")
df["horas_treinamento_ano"] = pd.to_numeric(
    df["horas_treinamento_ano"], errors="coerce"
)
df["dias_ausencia_mes"] = pd.to_numeric(df["dias_ausencia_mes"], errors="coerce")
df["acidentes_trabalho"] = pd.to_numeric(df["acidentes_trabalho"], errors="coerce")
df["uso_epi_score"] = pd.to_numeric(df["uso_epi_score"], errors="coerce")
df["avaliacao_performance"] = pd.to_numeric(
    df["avaliacao_performance"], errors="coerce"
)

# Clean status column - set Desligado where we have termination date
mask_desligado = df["data_demissao"].notna()
df.loc[mask_desligado, "status_funcionario"] = "Desligado"

# Fill NaN status with 'Ativo'
df["status_funcionario"] = df["status_funcionario"].fillna("Ativo")

# Calculate metrics
total_employees = len(df)
active_employees = len(df[df["status_funcionario"] == "Ativo"])
avg_salary = df["salario"].mean()
turnover_rate = len(df[df["status_funcionario"] == "Desligado"]) / total_employees * 100

# Initialize Dash app
app = dash.Dash(__name__)

# Define colors
colors = {
    "primary": "#2E86AB",
    "secondary": "#A23B72",
    "accent": "#F18F01",
    "success": "#C73E1D",
    "background": "#F5F5F5",
    "card": "#FFFFFF",
}

# Dashboard layout
app.layout = html.Div(
    [
        html.Div(
            [
                html.H1(
                    "Dashboard RH - Construtora",
                    style={
                        "textAlign": "center",
                        "color": colors["primary"],
                        "marginBottom": 30,
                    },
                ),
                # KPI Cards Row
                html.Div(
                    [
                        html.Div(
                            [
                                html.Div(
                                    [
                                        html.H3(
                                            f"{total_employees}",
                                            style={
                                                "color": colors["primary"],
                                                "margin": 0,
                                            },
                                        ),
                                        html.P(
                                            "Total de Funcionários", style={"margin": 0}
                                        ),
                                    ],
                                    className="kpi-card",
                                    style={
                                        "background": colors["card"],
                                        "padding": 20,
                                        "borderRadius": 8,
                                        "boxShadow": "0 2px 4px rgba(0,0,0,0.1)",
                                    },
                                )
                            ],
                            style={
                                "width": "23%",
                                "display": "inline-block",
                                "margin": "1%",
                            },
                        ),
                        html.Div(
                            [
                                html.Div(
                                    [
                                        html.H3(
                                            f"{active_employees}",
                                            style={
                                                "color": colors["success"],
                                                "margin": 0,
                                            },
                                        ),
                                        html.P(
                                            "Funcionários Ativos", style={"margin": 0}
                                        ),
                                    ],
                                    className="kpi-card",
                                    style={
                                        "background": colors["card"],
                                        "padding": 20,
                                        "borderRadius": 8,
                                        "boxShadow": "0 2px 4px rgba(0,0,0,0.1)",
                                    },
                                )
                            ],
                            style={
                                "width": "23%",
                                "display": "inline-block",
                                "margin": "1%",
                            },
                        ),
                        html.Div(
                            [
                                html.Div(
                                    [
                                        html.H3(
                                            f"R$ {avg_salary:,.0f}",
                                            style={
                                                "color": colors["accent"],
                                                "margin": 0,
                                            },
                                        ),
                                        html.P("Salário Médio", style={"margin": 0}),
                                    ],
                                    className="kpi-card",
                                    style={
                                        "background": colors["card"],
                                        "padding": 20,
                                        "borderRadius": 8,
                                        "boxShadow": "0 2px 4px rgba(0,0,0,0.1)",
                                    },
                                )
                            ],
                            style={
                                "width": "23%",
                                "display": "inline-block",
                                "margin": "1%",
                            },
                        ),
                        html.Div(
                            [
                                html.Div(
                                    [
                                        html.H3(
                                            f"{turnover_rate:.1f}%",
                                            style={
                                                "color": colors["secondary"],
                                                "margin": 0,
                                            },
                                        ),
                                        html.P(
                                            "Taxa de Rotatividade", style={"margin": 0}
                                        ),
                                    ],
                                    className="kpi-card",
                                    style={
                                        "background": colors["card"],
                                        "padding": 20,
                                        "borderRadius": 8,
                                        "boxShadow": "0 2px 4px rgba(0,0,0,0.1)",
                                    },
                                )
                            ],
                            style={
                                "width": "23%",
                                "display": "inline-block",
                                "margin": "1%",
                            },
                        ),
                    ],
                    style={"marginBottom": 30},
                ),
                # Charts Row 1
                html.Div(
                    [
                        html.Div(
                            [dcc.Graph(id="dept-distribution")],
                            style={
                                "width": "48%",
                                "display": "inline-block",
                                "margin": "1%",
                            },
                        ),
                        html.Div(
                            [dcc.Graph(id="age-distribution")],
                            style={
                                "width": "48%",
                                "display": "inline-block",
                                "margin": "1%",
                            },
                        ),
                    ]
                ),
                # Charts Row 2
                html.Div(
                    [
                        html.Div(
                            [dcc.Graph(id="salary-by-dept")],
                            style={
                                "width": "48%",
                                "display": "inline-block",
                                "margin": "1%",
                            },
                        ),
                        html.Div(
                            [dcc.Graph(id="safety-metrics")],
                            style={
                                "width": "48%",
                                "display": "inline-block",
                                "margin": "1%",
                            },
                        ),
                    ]
                ),
                # Charts Row 3
                html.Div(
                    [
                        html.Div(
                            [dcc.Graph(id="performance-metrics")],
                            style={
                                "width": "48%",
                                "display": "inline-block",
                                "margin": "1%",
                            },
                        ),
                        html.Div(
                            [dcc.Graph(id="education-levels")],
                            style={
                                "width": "48%",
                                "display": "inline-block",
                                "margin": "1%",
                            },
                        ),
                    ]
                ),
                # Charts Row 4
                html.Div(
                    [
                        html.Div(
                            [dcc.Graph(id="training-hours")],
                            style={
                                "width": "48%",
                                "display": "inline-block",
                                "margin": "1%",
                            },
                        ),
                        html.Div(
                            [dcc.Graph(id="turnover-reasons")],
                            style={
                                "width": "48%",
                                "display": "inline-block",
                                "margin": "1%",
                            },
                        ),
                    ]
                ),
            ],
            style={
                "padding": 20,
                "backgroundColor": colors["background"],
                "minHeight": "100vh",
            },
        )
    ]
)


# Callbacks for charts
@app.callback(Output("dept-distribution", "figure"), Input("dept-distribution", "id"))
def update_dept_distribution(_):
    dept_counts = df["departamento"].value_counts()
    fig = px.pie(
        values=dept_counts.values,
        names=dept_counts.index,
        title="Distribuição por Departamento",
        color_discrete_sequence=px.colors.qualitative.Set3,
    )
    fig.update_layout(font_size=12)
    return fig


@app.callback(Output("age-distribution", "figure"), Input("age-distribution", "id"))
def update_age_distribution(_):
    fig = px.histogram(
        df,
        x="idade",
        nbins=15,
        title="Distribuição por Idade",
        color_discrete_sequence=[colors["primary"]],
    )
    fig.update_layout(xaxis_title="Idade", yaxis_title="Número de Funcionários")
    return fig


@app.callback(Output("salary-by-dept", "figure"), Input("salary-by-dept", "id"))
def update_salary_by_dept(_):
    fig = px.box(
        df,
        x="departamento",
        y="salario",
        title="Distribuição Salarial por Departamento",
        color="departamento",
    )
    fig.update_layout(xaxis_title="Departamento", yaxis_title="Salário (R$)")
    fig.update_xaxes(tickangle=45)
    return fig


@app.callback(Output("safety-metrics", "figure"), Input("safety-metrics", "id"))
def update_safety_metrics(_):
    safety_data = pd.DataFrame(
        {
            "Métrica": ["Acidentes de Trabalho", "Uso EPI >= 9.0", "Com Certificações"],
            "Quantidade": [
                df["acidentes_trabalho"].sum(),
                len(df[df["uso_epi_score"] >= 9.0]),
                len(df[df["certificacoes_seguranca"].notna()]),
            ],
        }
    )

    fig = px.bar(
        safety_data,
        x="Métrica",
        y="Quantidade",
        title="Métricas de Segurança",
        color="Métrica",
        color_discrete_sequence=[
            colors["success"],
            colors["primary"],
            colors["accent"],
        ],
    )
    return fig


@app.callback(
    Output("performance-metrics", "figure"), Input("performance-metrics", "id")
)
def update_performance_metrics(_):
    fig = make_subplots(specs=[[{"secondary_y": True}]])

    fig.add_trace(
        go.Scatter(
            x=df["avaliacao_performance"],
            y=df["horas_treinamento_ano"],
            mode="markers",
            name="Funcionários",
            marker=dict(color=colors["primary"], size=8, opacity=0.6),
        ),
        secondary_y=False,
    )

    fig.update_xaxes(title_text="Avaliação de Performance")
    fig.update_yaxes(title_text="Horas de Treinamento/Ano", secondary_y=False)
    fig.update_layout(title_text="Performance vs. Treinamento")

    return fig


@app.callback(Output("education-levels", "figure"), Input("education-levels", "id"))
def update_education_levels(_):
    edu_counts = df["escolaridade"].value_counts()
    fig = px.bar(
        x=edu_counts.index,
        y=edu_counts.values,
        title="Níveis de Escolaridade",
        color_discrete_sequence=[colors["accent"]],
    )
    fig.update_layout(xaxis_title="Escolaridade", yaxis_title="Número de Funcionários")

    fig.update_xaxes(tickangle=45)
    return fig


@app.callback(Output("training-hours", "figure"), Input("training-hours", "id"))
def update_training_hours(_):
    avg_training = (
        df.groupby("departamento")["horas_treinamento_ano"]
        .mean()
        .sort_values(ascending=True)
    )

    fig = px.bar(
        x=avg_training.values,
        y=avg_training.index,
        orientation="h",
        title="Média de Horas de Treinamento por Departamento",
        color_discrete_sequence=[colors["secondary"]],
    )
    fig.update_layout(
        xaxis_title="Horas de Treinamento (Média)", yaxis_title="Departamento"
    )
    return fig


@app.callback(Output("turnover-reasons", "figure"), Input("turnover-reasons", "id"))
def update_turnover_reasons(_):
    turnover_df = df[df["status_funcionario"] == "Desligado"]

    if len(turnover_df) > 0:
        reasons = turnover_df["motivo_saida"].value_counts()
        fig = px.pie(
            values=reasons.values,
            names=reasons.index,
            title="Motivos de Desligamento",
            color_discrete_sequence=px.colors.qualitative.Pastel,
        )
    else:
        fig = px.pie(values=[1], names=["Sem dados"], title="Motivos de Desligamento")

    return fig


if __name__ == "__main__":
    app.run_server(debug=True, host="0.0.0.0", port=8050)
