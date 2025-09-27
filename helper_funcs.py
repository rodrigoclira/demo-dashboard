from datetime import datetime
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split


def predict_turnover_risk(data):
    """Predict turnover risk for all active employees"""
    model, feature_importance, dept_mapping, feature_columns = train_turnover_model(
        data
    )

    if model is None:
        return None, None

    # Get active employees only
    active_df = data[data["status_funcionario"] == "Ativo"].copy()
    ml_df, _, _ = prepare_ml_features(active_df)

    # Make predictions
    X = ml_df[feature_columns]
    risk_scores = model.predict_proba(X)[:, 1]  # Probability of turnover

    # Add risk scores to the dataframe
    active_df["risk_score"] = risk_scores
    active_df["risk_level"] = pd.cut(
        risk_scores, bins=[0, 0.25, 0.5, 1.0], labels=["Baixo", "Médio", "Alto"]
    )

    return active_df, feature_importance


# Machine Learning: Employee Turnover Prediction
def prepare_ml_features(data):
    """Prepare features for machine learning model"""
    ml_df = data.copy()

    # Feature engineering
    ml_df["idade_normalizada"] = ml_df["idade"] / 100
    ml_df["salario_normalizado"] = ml_df["salario"] / ml_df["salario"].max()
    ml_df["anos_servico_normalizado"] = (
        ml_df["anos_servico"] / ml_df["anos_servico"].max()
    )

    # Encode categorical variables
    dept_mapping = {dept: i for i, dept in enumerate(ml_df["departamento"].unique())}
    ml_df["departamento_encoded"] = ml_df["departamento"].map(dept_mapping)

    # Create target variable (1 = Desligado, 0 = Ativo)
    ml_df["target"] = (ml_df["status_funcionario"] == "Desligado").astype(int)

    # Select features for the model
    feature_columns = [
        "idade_normalizada",
        "salario_normalizado",
        "anos_servico_normalizado",
        "departamento_encoded",
        "horas_treinamento_ano",
        "dias_ausencia_mes",
        "acidentes_trabalho",
        "uso_epi_score",
        "avaliacao_performance",
    ]

    # Fill missing values
    for col in feature_columns:
        if col in ml_df.columns:
            ml_df[col] = ml_df[col].fillna(ml_df[col].mean())

    return ml_df, feature_columns, dept_mapping


def train_turnover_model(data):
    """Train the turnover prediction model"""
    try:
        ml_df, feature_columns, dept_mapping = prepare_ml_features(data)

        # Prepare features and target
        X = ml_df[feature_columns]
        y = ml_df["target"]

        # Split data
        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=0.2, random_state=42, stratify=y
        )

        # Train model
        model = RandomForestClassifier(
            n_estimators=100, random_state=42, max_depth=10, min_samples_split=5
        )
        model.fit(X_train, y_train)

        # Calculate feature importance
        feature_importance = dict(zip(feature_columns, model.feature_importances_))

        return model, feature_importance, dept_mapping, feature_columns
    except Exception as e:
        print(f"Error training model: {e}")
        return None, None, None, None


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
