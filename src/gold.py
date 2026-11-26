"""Gold: tabelas agregadas para análise da precipitação."""
import pandas as pd
from config import (
    SILVER_FILE, GOLD_HOURLY_FILE, GOLD_MONTHLY_FILE, GOLD_YEARLY_FILE
)

def construir_gold(df: pd.DataFrame | None = None) -> dict[str, pd.DataFrame]:
    if df is None:
        if not SILVER_FILE.exists():
            raise FileNotFoundError("Silver não encontrada. Execute main.py primeiro.")
        df = pd.read_csv(SILVER_FILE, parse_dates=["data_hora_local"])

    # Valor zero é ausência de precipitação registrada; NA é dado desconhecido.
    validos = df.dropna(subset=["precipitacao_mm"]).copy()
    com_chuva = validos[validos["precipitacao_mm"] > 0].copy()

    hourly = (
        com_chuva.groupby("hora")
        .agg(
            quantidade_registros_com_chuva=("precipitacao_mm", "size"),
            precipitacao_acumulada_mm=("precipitacao_mm", "sum"),
            precipitacao_media_mm=("precipitacao_mm", "mean"),
        )
        .reindex(range(24), fill_value=0)
        .rename_axis("hora")
        .reset_index()
    )

    monthly = (
        validos.groupby("mes")
        .agg(
            precipitacao_acumulada_mm=("precipitacao_mm", "sum"),
            precipitacao_media_por_registro_mm=("precipitacao_mm", "mean"),
            registros_validos=("precipitacao_mm", "count"),
        )
        .reindex(range(1, 13))
        .rename_axis("mes")
        .reset_index()
    )

    yearly = (
        validos.groupby("ano")
        .agg(
            precipitacao_acumulada_mm=("precipitacao_mm", "sum"),
            precipitacao_media_por_registro_mm=("precipitacao_mm", "mean"),
            registros_validos=("precipitacao_mm", "count"),
        )
        .reset_index()
        .sort_values("ano")
    )

    for caminho, tabela in [
        (GOLD_HOURLY_FILE, hourly),
        (GOLD_MONTHLY_FILE, monthly),
        (GOLD_YEARLY_FILE, yearly),
    ]:
        caminho.parent.mkdir(parents=True, exist_ok=True)
        tabela.to_csv(caminho, index=False, encoding="utf-8")
        print(f"Gold salva: {caminho}")

    return {"hourly": hourly, "monthly": monthly, "yearly": yearly}

if __name__ == "__main__":
    construir_gold()
