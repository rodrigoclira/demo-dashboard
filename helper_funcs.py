from datetime import datetime
import pandas as pd


# Helper function to filter data based on controls
def get_filtered_data(df, dept_filter="all", status_filter="all"):
    """Apply filters to the main dataframe"""
    filtered_df = df.copy()

    # Apply department filter
    if dept_filter != "all":
        filtered_df = filtered_df[filtered_df["departamento"] == dept_filter]

    # Apply status filter
    if status_filter != "all":
        filtered_df = filtered_df[filtered_df["status_funcionario"] == status_filter]

    return filtered_df


# Helper functions for birthday and anniversary features
def get_upcoming_birthdays(df, days_ahead=30, dept_filter="all"):
    """Get employees with birthdays in the next N days"""
    today = datetime.now()

    # Start with active employees only
    active_df = df[df["status_funcionario"] == "Ativo"].copy()

    # Apply department filter
    if dept_filter != "all":
        active_df = active_df[active_df["departamento"] == dept_filter].copy()

    # Create this year's birthday for each employee
    active_df["birthday_this_year"] = active_df["data_nascimento"].dt.strftime(
        f"{today.year}-%m-%d"
    )
    active_df["birthday_this_year"] = pd.to_datetime(active_df["birthday_this_year"])

    # If birthday already passed this year, use next year
    active_df.loc[active_df["birthday_this_year"] < today, "birthday_this_year"] = (
        active_df.loc[
            active_df["birthday_this_year"] < today, "data_nascimento"
        ].dt.strftime(f"{today.year + 1}-%m-%d")
    )
    active_df.loc[active_df["birthday_this_year"] < today, "birthday_this_year"] = (
        pd.to_datetime(
            active_df.loc[active_df["birthday_this_year"] < today, "birthday_this_year"]
        )
    )

    # Filter for upcoming birthdays
    end_date = today + pd.Timedelta(days=days_ahead)
    upcoming = active_df[active_df["birthday_this_year"] <= end_date].sort_values(
        "birthday_this_year"
    )

    return upcoming[
        [
            "nome",
            "departamento",
            "cargo",
            "data_nascimento",
            "birthday_this_year",
            "idade",
        ]
    ]


def get_work_anniversaries(df, days_ahead=30, dept_filter="all"):
    """Get employees with work anniversaries in the next N days"""
    today = datetime.now()

    # Start with active employees only
    active_df = df[df["status_funcionario"] == "Ativo"].copy()

    # Apply department filter
    if dept_filter != "all":
        active_df = active_df[active_df["departamento"] == dept_filter].copy()

    # Create this year's anniversary for each employee
    active_df["anniversary_this_year"] = active_df["data_admissao"].dt.strftime(
        f"{today.year}-%m-%d"
    )
    active_df["anniversary_this_year"] = pd.to_datetime(
        active_df["anniversary_this_year"]
    )

    # If anniversary already passed this year, use next year
    active_df.loc[
        active_df["anniversary_this_year"] < today, "anniversary_this_year"
    ] = active_df.loc[
        active_df["anniversary_this_year"] < today, "data_admissao"
    ].dt.strftime(f"{today.year + 1}-%m-%d")
    active_df.loc[
        active_df["anniversary_this_year"] < today, "anniversary_this_year"
    ] = pd.to_datetime(
        active_df.loc[
            active_df["anniversary_this_year"] < today, "anniversary_this_year"
        ]
    )

    # Filter for upcoming anniversaries
    end_date = today + pd.Timedelta(days=days_ahead)
    upcoming = active_df[active_df["anniversary_this_year"] <= end_date].sort_values(
        "anniversary_this_year"
    )

    return upcoming[
        [
            "nome",
            "departamento",
            "cargo",
            "data_admissao",
            "anniversary_this_year",
            "anos_servico",
        ]
    ]


def get_outdated_certifications(df, dept_filter="all"):
    """Get employees with outdated certifications (sorted by oldest training date)"""
    today = datetime.now()

    # Start with active employees only
    active_df = df[df["status_funcionario"] == "Ativo"].copy()

    # Apply department filter
    if dept_filter != "all":
        active_df = active_df[active_df["departamento"] == dept_filter].copy()

    # Filter only employees who have certifications
    certified_df = active_df[active_df["certificacoes_seguranca"].notna()].copy()

    # Calculate days since last training
    certified_df["dias_sem_treinamento"] = (
        today - certified_df["ultimo_treinamento"]
    ).dt.days

    # Sort by days without training (descending - oldest first)
    certified_df = certified_df.sort_values("dias_sem_treinamento", ascending=False)

    return certified_df[
        [
            "nome",
            "departamento",
            "cargo",
            "certificacoes_seguranca",
            "ultimo_treinamento",
            "dias_sem_treinamento",
            "horas_treinamento_ano",
        ]
    ]
