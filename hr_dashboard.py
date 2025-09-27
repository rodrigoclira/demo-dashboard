import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import dash
from dash import dcc, html, Input, Output
from datetime import datetime
from styles import *
from helper_funcs import * 

# Load and prepare data - handle CSV parsing issues
# no index column in the CSV
df = pd.read_csv("data/rh_construtora_dataset2.csv", index_col=False, sep=",")

# Clean and convert date columns with proper error handling
# add format error coercion to handle invalid dates in the dataset YYYY-MM-DD
df["data_admissao"] = pd.to_datetime(df["data_admissao"], format="%Y-%m-%d")
df["data_nascimento"] = pd.to_datetime(df["data_nascimento"], format="%Y-%m-%d")

df["data_demissao"] = pd.to_datetime(df["data_demissao"], format="%Y-%m-%d")
df["ultimo_treinamento"] = pd.to_datetime(df["ultimo_treinamento"], format="%Y-%m-%d")

# Clean numeric columns
df["salario"] = pd.to_numeric(df["salario"], errors="coerce")

# calculate idade column based in data_nascimento
df["idade"] = (datetime.now() - df["data_nascimento"]).dt.days // 365
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

# Calculate total payroll (only active employees)
total_payroll = df[df["status_funcionario"] == "Ativo"]["salario"].sum()

# Calculate years of service
today = datetime.now()
df["anos_servico"] = (today - df["data_admissao"]).dt.days / 365.25

# Initialize Dash app
app = dash.Dash(__name__, suppress_callback_exceptions=True, title="Dashboard RH")

# Define colors
colors = {
    "primary": "#053042",
    "secondary": "#AF200D",
    "accent": "#8B590D",
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
                    "Dashboard RH",
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
                                            id="total-employees-kpi",
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
                                "width": "18%",
                                "display": "inline-block",
                                "margin": "1%",
                            },
                        ),
                        html.Div(
                            [
                                html.Div(
                                    [
                                        html.H3(
                                            id="active-employees-kpi",
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
                                "width": "18%",
                                "display": "inline-block",
                                "margin": "1%",
                            },
                        ),
                        html.Div(
                            [
                                html.Div(
                                    [
                                        html.H3(
                                            id="avg-salary-kpi",
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
                                "width": "18%",
                                "display": "inline-block",
                                "margin": "1%",
                            },
                        ),
                        html.Div(
                            [
                                html.Div(
                                    [
                                        html.H3(
                                            id="total-payroll-kpi",
                                            style={
                                                "color": colors["primary"],
                                                "margin": 0,
                                            },
                                        ),
                                        html.P(
                                            "Folha de Pagamento", style={"margin": 0}
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
                                "width": "18%",
                                "display": "inline-block",
                                "margin": "1%",
                            },
                        ),
                        html.Div(
                            [
                                html.Div(
                                    [
                                        html.H3(
                                            id="turnover-rate-kpi",
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
                                "width": "18%",
                                "display": "inline-block",
                                "margin": "1%",
                            },
                        ),
                    ],
                    style={"marginBottom": 30},
                ),
                # Tabs for different sections
                dcc.Tabs(
                    id="main-tabs",
                    value="dashboard",
                    children=[
                        dcc.Tab(
                            label="Visão Geral",
                            value="dashboard",
                            style=tab_style,
                            selected_style=tab_selected_style,
                        ),
                        dcc.Tab(
                            label="Aniversários",
                            value="birthdays",
                            style=tab_style,
                            selected_style=tab_selected_style,
                        ),
                        dcc.Tab(
                            label="Tempo de Empresa",
                            value="work-anniversaries",
                            style=tab_style,
                            selected_style=tab_selected_style,
                        ),
                        dcc.Tab(
                            label="Certificações",
                            value="certifications",
                            style=tab_style,
                            selected_style=tab_selected_style,
                        ),
                    ],
                ),
                # Tab content
                html.Div(id="tabs-content"),
            ],
            style={
                "padding": 20,
                "backgroundColor": colors["background"],
                "minHeight": "100vh",
            },
        )
    ]
)


# Callbacks for tabs
@app.callback(Output("tabs-content", "children"), Input("main-tabs", "value"))
def render_tab_content(active_tab):
    if active_tab == "birthdays":
        return html.Div(
            [
                html.H2(
                    "Aniversários dos Funcionários",
                    style={"color": colors["primary"], "marginBottom": 20},
                ),
                # Control Panel for this tab
                html.Div(
                    [
                        html.Label(
                            "Filtrar por Departamento:",
                            style={"fontWeight": "bold", "marginBottom": 5},
                        ),
                        dcc.Dropdown(
                            id="birthdays-dept-filter",
                            options=[
                                {"label": "Todos os Departamentos", "value": "all"}
                            ]
                            + [
                                {"label": dept, "value": dept}
                                for dept in sorted(df["departamento"].unique())
                            ],
                            value="all",
                            clearable=False,
                            style={"marginBottom": 10, "width": "300px"},
                        ),
                        html.Label(
                            "Período:",
                            style={
                                "fontWeight": "bold",
                                "marginBottom": 5,
                                "marginLeft": 20,
                            },
                        ),
                        dcc.Dropdown(
                            id="birthdays-period-filter",
                            options=[
                                {"label": "Próximos 30 dias", "value": 30},
                                {"label": "Próximos 60 dias", "value": 60},
                                {"label": "Próximos 90 dias", "value": 90},
                                {"label": "Próximos 180 dias", "value": 180},
                            ],
                            value=30,
                            clearable=False,
                            style={
                                "marginBottom": 10,
                                "width": "200px",
                                "marginLeft": 20,
                                "display": "inline-block",
                            },
                        ),
                    ],
                    style={
                        "background": colors["card"],
                        "padding": 15,
                        "borderRadius": 8,
                        "boxShadow": "0 2px 4px rgba(0,0,0,0.1)",
                        "marginBottom": 20,
                        "display": "flex",
                        "alignItems": "center",
                    },
                ),
                # Content will be updated by another callback
                html.Div(id="birthdays-content"),
            ]
        )

    elif active_tab == "work-anniversaries":
        return html.Div(
            [
                html.H2(
                    "Aniversários de Tempo de Empresa",
                    style={"color": colors["primary"], "marginBottom": 20},
                ),
                # Control Panel for this tab
                html.Div(
                    [
                        html.Label(
                            "Filtrar por Departamento:",
                            style={"fontWeight": "bold", "marginBottom": 5},
                        ),
                        dcc.Dropdown(
                            id="anniversaries-dept-filter",
                            options=[
                                {"label": "Todos os Departamentos", "value": "all"}
                            ]
                            + [
                                {"label": dept, "value": dept}
                                for dept in sorted(df["departamento"].unique())
                            ],
                            value="all",
                            clearable=False,
                            style={"marginBottom": 10, "width": "300px"},
                        ),
                        html.Label(
                            "Período:",
                            style={
                                "fontWeight": "bold",
                                "marginBottom": 5,
                                "marginLeft": 20,
                            },
                        ),
                        dcc.Dropdown(
                            id="anniversaries-period-filter",
                            options=[
                                {"label": "Próximos 30 dias", "value": 30},
                                {"label": "Próximos 60 dias", "value": 60},
                                {"label": "Próximos 90 dias", "value": 90},
                                {"label": "Próximos 180 dias", "value": 180},
                            ],
                            value=30,
                            clearable=False,
                            style={
                                "marginBottom": 10,
                                "width": "200px",
                                "marginLeft": 20,
                                "display": "inline-block",
                            },
                        ),
                    ],
                    style={
                        "background": colors["card"],
                        "padding": 15,
                        "borderRadius": 8,
                        "boxShadow": "0 2px 4px rgba(0,0,0,0.1)",
                        "marginBottom": 20,
                        "display": "flex",
                        "alignItems": "center",
                    },
                ),
                # Content will be updated by another callback
                html.Div(id="anniversaries-content"),
            ]
        )

    elif active_tab == "certifications":
        return html.Div(
            [
                html.H2(
                    "Status das Certificações de Segurança",
                    style={"color": colors["primary"], "marginBottom": 20},
                ),
                # Control Panel for this tab
                html.Div(
                    [
                        html.Label(
                            "Filtrar por Departamento:",
                            style={"fontWeight": "bold", "marginBottom": 5},
                        ),
                        dcc.Dropdown(
                            id="certifications-dept-filter",
                            options=[
                                {"label": "Todos os Departamentos", "value": "all"}
                            ]
                            + [
                                {"label": dept, "value": dept}
                                for dept in sorted(df["departamento"].unique())
                            ],
                            value="all",
                            clearable=False,
                            style={"marginBottom": 20, "width": "300px"},
                        ),
                    ],
                    style={
                        "background": colors["card"],
                        "padding": 15,
                        "borderRadius": 8,
                        "boxShadow": "0 2px 4px rgba(0,0,0,0.1)",
                        "marginBottom": 20,
                    },
                ),
                # Content will be updated by another callback
                html.Div(id="certifications-content"),
            ]
        )

    else:  # dashboard tab
        return html.Div(
            [
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
            ]
        )


# Callbacks for KPIs
@app.callback(
    [
        Output("total-employees-kpi", "children"),
        Output("active-employees-kpi", "children"),
        Output("avg-salary-kpi", "children"),
        Output("total-payroll-kpi", "children"),
        Output("turnover-rate-kpi", "children"),
    ],
    Input("main-tabs", "value"),
)
def update_kpis(_):
    # Use all data for KPIs (no filtering)
    total_employees = len(df)
    active_employees = len(df[df["status_funcionario"] == "Ativo"])
    avg_salary = df["salario"].mean()
    total_payroll = df[df["status_funcionario"] == "Ativo"]["salario"].sum()
    turnover_rate = (
        len(df[df["status_funcionario"] == "Desligado"]) / total_employees * 100
        if total_employees > 0
        else 0
    )

    return (
        f"{total_employees}",
        f"{active_employees}",
        f"R$ {avg_salary:,.2f}",
        f"R$ {total_payroll:,.2f}",
        f"{turnover_rate:.1f}%",
    )


# Callbacks for tab content
@app.callback(
    Output("birthdays-content", "children"),
    [
        Input("birthdays-dept-filter", "value"),
        Input("birthdays-period-filter", "value"),
    ],
)
def update_birthdays_content(dept_filter, period_filter):
    upcoming_birthdays = get_upcoming_birthdays(df, period_filter, dept_filter)

    return html.Div(
        [
            html.Div(
                [
                    html.H4(f"Total: {len(upcoming_birthdays)} aniversariantes"),
                    html.P(
                        "Funcionários ativos com aniversário no período selecionado"
                    ),
                ],
                style={
                    "background": colors["card"],
                    "padding": 20,
                    "borderRadius": 8,
                    "boxShadow": "0 2px 4px rgba(0,0,0,0.1)",
                    "marginBottom": 20,
                },
            ),
            # Birthday table
            html.Div(
                [
                    html.Table(
                        [
                            html.Thead(
                                [
                                    html.Tr(
                                        [
                                            html.Th(
                                                "Nome",
                                                style={
                                                    "padding": 10,
                                                    "background": colors["primary"],
                                                    "color": "white",
                                                },
                                            ),
                                            html.Th(
                                                "Departamento",
                                                style={
                                                    "padding": 10,
                                                    "background": colors["primary"],
                                                    "color": "white",
                                                },
                                            ),
                                            html.Th(
                                                "Cargo",
                                                style={
                                                    "padding": 10,
                                                    "background": colors["primary"],
                                                    "color": "white",
                                                },
                                            ),
                                            html.Th(
                                                "Data Aniversário",
                                                style={
                                                    "padding": 10,
                                                    "background": colors["primary"],
                                                    "color": "white",
                                                },
                                            ),
                                            html.Th(
                                                "Idade",
                                                style={
                                                    "padding": 10,
                                                    "background": colors["primary"],
                                                    "color": "white",
                                                },
                                            ),
                                            html.Th(
                                                "Dias até Aniversário",
                                                style={
                                                    "padding": 10,
                                                    "background": colors["primary"],
                                                    "color": "white",
                                                },
                                            ),
                                        ]
                                    )
                                ]
                            ),
                            html.Tbody(
                                [
                                    html.Tr(
                                        [
                                            html.Td(
                                                row["nome"],
                                                style={
                                                    "padding": 10,
                                                    "borderBottom": "1px solid #ddd",
                                                },
                                            ),
                                            html.Td(
                                                row["departamento"],
                                                style={
                                                    "padding": 10,
                                                    "borderBottom": "1px solid #ddd",
                                                },
                                            ),
                                            html.Td(
                                                row["cargo"],
                                                style={
                                                    "padding": 10,
                                                    "borderBottom": "1px solid #ddd",
                                                },
                                            ),
                                            html.Td(
                                                row["data_nascimento"].strftime(
                                                    "%d/%m"
                                                ),
                                                style={
                                                    "padding": 10,
                                                    "borderBottom": "1px solid #ddd",
                                                },
                                            ),
                                            html.Td(
                                                f"{int(row['idade'])} anos",
                                                style={
                                                    "padding": 10,
                                                    "borderBottom": "1px solid #ddd",
                                                },
                                            ),
                                            html.Td(
                                                f"{(row['birthday_this_year'] - datetime.now()).days} dias",
                                                style={
                                                    "padding": 10,
                                                    "borderBottom": "1px solid #ddd",
                                                },
                                            ),
                                        ]
                                    )
                                    for _, row in upcoming_birthdays.iterrows()
                                ]
                            ),
                        ],
                        style={
                            "width": "100%",
                            "borderCollapse": "collapse",
                            "background": colors["card"],
                        },
                    )
                ],
                style={
                    "borderRadius": 8,
                    "boxShadow": "0 2px 4px rgba(0,0,0,0.1)",
                    "overflow": "hidden",
                },
            ),
        ]
    )


@app.callback(
    Output("anniversaries-content", "children"),
    [
        Input("anniversaries-dept-filter", "value"),
        Input("anniversaries-period-filter", "value"),
    ],
)
def update_anniversaries_content(dept_filter, period_filter):
    upcoming_anniversaries = get_work_anniversaries(df, period_filter, dept_filter)

    return html.Div(
        [
            html.Div(
                [
                    html.H4(
                        f"Total: {len(upcoming_anniversaries)} aniversários de empresa"
                    ),
                    html.P(
                        "Funcionários com aniversário de admissão no período selecionado"
                    ),
                ],
                style={
                    "background": colors["card"],
                    "padding": 20,
                    "borderRadius": 8,
                    "boxShadow": "0 2px 4px rgba(0,0,0,0.1)",
                    "marginBottom": 20,
                },
            ),
            # Anniversary table
            html.Div(
                [
                    html.Table(
                        [
                            html.Thead(
                                [
                                    html.Tr(
                                        [
                                            html.Th(
                                                "Nome",
                                                style={
                                                    "padding": 10,
                                                    "background": colors["primary"],
                                                    "color": "white",
                                                },
                                            ),
                                            html.Th(
                                                "Departamento",
                                                style={
                                                    "padding": 10,
                                                    "background": colors["primary"],
                                                    "color": "white",
                                                },
                                            ),
                                            html.Th(
                                                "Cargo",
                                                style={
                                                    "padding": 10,
                                                    "background": colors["primary"],
                                                    "color": "white",
                                                },
                                            ),
                                            html.Th(
                                                "Data Admissão",
                                                style={
                                                    "padding": 10,
                                                    "background": colors["primary"],
                                                    "color": "white",
                                                },
                                            ),
                                            html.Th(
                                                "Anos de Empresa",
                                                style={
                                                    "padding": 10,
                                                    "background": colors["primary"],
                                                    "color": "white",
                                                },
                                            ),
                                            html.Th(
                                                "Dias até Aniversário",
                                                style={
                                                    "padding": 10,
                                                    "background": colors["primary"],
                                                    "color": "white",
                                                },
                                            ),
                                        ]
                                    )
                                ]
                            ),
                            html.Tbody(
                                [
                                    html.Tr(
                                        [
                                            html.Td(
                                                row["nome"],
                                                style={
                                                    "padding": 10,
                                                    "borderBottom": "1px solid #ddd",
                                                },
                                            ),
                                            html.Td(
                                                row["departamento"],
                                                style={
                                                    "padding": 10,
                                                    "borderBottom": "1px solid #ddd",
                                                },
                                            ),
                                            html.Td(
                                                row["cargo"],
                                                style={
                                                    "padding": 10,
                                                    "borderBottom": "1px solid #ddd",
                                                },
                                            ),
                                            html.Td(
                                                row["data_admissao"].strftime(
                                                    "%d/%m/%Y"
                                                ),
                                                style={
                                                    "padding": 10,
                                                    "borderBottom": "1px solid #ddd",
                                                },
                                            ),
                                            html.Td(
                                                f"{row['anos_servico']:.1f} anos",
                                                style={
                                                    "padding": 10,
                                                    "borderBottom": "1px solid #ddd",
                                                },
                                            ),
                                            html.Td(
                                                f"{(row['anniversary_this_year'] - datetime.now()).days} dias",
                                                style={
                                                    "padding": 10,
                                                    "borderBottom": "1px solid #ddd",
                                                },
                                            ),
                                        ]
                                    )
                                    for _, row in upcoming_anniversaries.iterrows()
                                ]
                            ),
                        ],
                        style={
                            "width": "100%",
                            "borderCollapse": "collapse",
                            "background": colors["card"],
                        },
                    )
                ],
                style={
                    "borderRadius": 8,
                    "boxShadow": "0 2px 4px rgba(0,0,0,0.1)",
                    "overflow": "hidden",
                },
            ),
        ]
    )


@app.callback(
    Output("certifications-content", "children"),
    Input("certifications-dept-filter", "value"),
)
def update_certifications_content(dept_filter):
    outdated_certs = get_outdated_certifications(df, dept_filter)

    return html.Div(
        [
            html.Div(
                [
                    html.H4(f"Total: {len(outdated_certs)} funcionários certificados"),
                    html.P(
                        "Funcionários ordenados por tempo sem atualização de treinamento"
                    ),
                ],
                style={
                    "background": colors["card"],
                    "padding": 20,
                    "borderRadius": 8,
                    "boxShadow": "0 2px 4px rgba(0,0,0,0.1)",
                    "marginBottom": 20,
                },
            ),
            # Certifications table
            html.Div(
                [
                    html.Table(
                        [
                            html.Thead(
                                [
                                    html.Tr(
                                        [
                                            html.Th(
                                                "Nome",
                                                style={
                                                    "padding": 10,
                                                    "background": colors["primary"],
                                                    "color": "white",
                                                },
                                            ),
                                            html.Th(
                                                "Departamento",
                                                style={
                                                    "padding": 10,
                                                    "background": colors["primary"],
                                                    "color": "white",
                                                },
                                            ),
                                            html.Th(
                                                "Cargo",
                                                style={
                                                    "padding": 10,
                                                    "background": colors["primary"],
                                                    "color": "white",
                                                },
                                            ),
                                            html.Th(
                                                "Certificações",
                                                style={
                                                    "padding": 10,
                                                    "background": colors["primary"],
                                                    "color": "white",
                                                },
                                            ),
                                            html.Th(
                                                "Último Treinamento",
                                                style={
                                                    "padding": 10,
                                                    "background": colors["primary"],
                                                    "color": "white",
                                                },
                                            ),
                                            html.Th(
                                                "Dias sem Treinamento",
                                                style={
                                                    "padding": 10,
                                                    "background": colors["primary"],
                                                    "color": "white",
                                                },
                                            ),
                                            html.Th(
                                                "Horas Anuais",
                                                style={
                                                    "padding": 10,
                                                    "background": colors["primary"],
                                                    "color": "white",
                                                },
                                            ),
                                        ]
                                    )
                                ]
                            ),
                            html.Tbody(
                                [
                                    html.Tr(
                                        [
                                            html.Td(
                                                row["nome"],
                                                style={
                                                    "padding": 10,
                                                    "borderBottom": "1px solid #ddd",
                                                },
                                            ),
                                            html.Td(
                                                row["departamento"],
                                                style={
                                                    "padding": 10,
                                                    "borderBottom": "1px solid #ddd",
                                                },
                                            ),
                                            html.Td(
                                                row["cargo"],
                                                style={
                                                    "padding": 10,
                                                    "borderBottom": "1px solid #ddd",
                                                },
                                            ),
                                            html.Td(
                                                row["certificacoes_seguranca"],
                                                style={
                                                    "padding": 10,
                                                    "borderBottom": "1px solid #ddd",
                                                    "fontSize": "12px",
                                                },
                                            ),
                                            html.Td(
                                                row["ultimo_treinamento"].strftime(
                                                    "%d/%m/%Y"
                                                ),
                                                style={
                                                    "padding": 10,
                                                    "borderBottom": "1px solid #ddd",
                                                },
                                            ),
                                            html.Td(
                                                f"{int(row['dias_sem_treinamento'])} dias",
                                                style={
                                                    "padding": 10,
                                                    "borderBottom": "1px solid #ddd",
                                                    "color": "red"
                                                    if row["dias_sem_treinamento"] > 365
                                                    else "orange"
                                                    if row["dias_sem_treinamento"] > 180
                                                    else "green",
                                                    "fontWeight": "bold",
                                                },
                                            ),
                                            html.Td(
                                                f"{int(row['horas_treinamento_ano'])}h",
                                                style={
                                                    "padding": 10,
                                                    "borderBottom": "1px solid #ddd",
                                                },
                                            ),
                                        ],
                                        style={
                                            "backgroundColor": "#ffebee"
                                            if row["dias_sem_treinamento"] > 365
                                            else "#fff3e0"
                                            if row["dias_sem_treinamento"] > 180
                                            else "#e8f5e8"
                                        },
                                    )
                                    for _, row in outdated_certs.iterrows()
                                ]
                            ),
                        ],
                        style={
                            "width": "100%",
                            "borderCollapse": "collapse",
                            "background": colors["card"],
                        },
                    )
                ],
                style={
                    "borderRadius": 8,
                    "boxShadow": "0 2px 4px rgba(0,0,0,0.1)",
                    "overflow": "hidden",
                },
            ),
        ]
    )


# Callbacks for charts
@app.callback(Output("dept-distribution", "figure"), Input("main-tabs", "value"))
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


@app.callback(Output("age-distribution", "figure"), Input("main-tabs", "value"))
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


@app.callback(Output("salary-by-dept", "figure"), Input("main-tabs", "value"))
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
