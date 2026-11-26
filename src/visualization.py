"""Gráficos a partir das tabelas Gold usando Matplotlib."""
import pandas as pd
import matplotlib.pyplot as plt
from config import GOLD_HOURLY_FILE, GOLD_MONTHLY_FILE, GOLD_YEARLY_FILE, OUTPUT_DIR

def gerar_graficos() -> None:
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    hourly = pd.read_csv(GOLD_HOURLY_FILE)
    plt.figure(figsize=(11, 5))
    plt.bar(hourly["hora"], hourly["quantidade_registros_com_chuva"])
    plt.title("Frequência de registros com chuva por hora — Belém")
    plt.xlabel("Hora local")
    plt.ylabel("Número de registros com precipitação > 0")
    plt.xticks(range(24))
    plt.grid(axis="y", alpha=0.25)
    plt.tight_layout()
    plt.savefig(OUTPUT_DIR / "chuva_por_hora.png", dpi=150)
    plt.close()

    monthly = pd.read_csv(GOLD_MONTHLY_FILE)
    plt.figure(figsize=(10, 5))
    plt.bar(monthly["mes"], monthly["precipitacao_acumulada_mm"])
    plt.title("Precipitação acumulada por mês — série histórica")
    plt.xlabel("Mês")
    plt.ylabel("Precipitação acumulada (mm)")
    plt.xticks(range(1, 13))
    plt.grid(axis="y", alpha=0.25)
    plt.tight_layout()
    plt.savefig(OUTPUT_DIR / "chuva_por_mes.png", dpi=150)
    plt.close()

    yearly = pd.read_csv(GOLD_YEARLY_FILE)
    plt.figure(figsize=(12, 5))
    plt.plot(yearly["ano"], yearly["precipitacao_acumulada_mm"], marker="o")
    plt.title("Precipitação acumulada por ano — Belém")
    plt.xlabel("Ano")
    plt.ylabel("Precipitação acumulada (mm)")
    plt.grid(alpha=0.25)
    plt.tight_layout()
    plt.savefig(OUTPUT_DIR / "chuva_por_ano.png", dpi=150)
    plt.close()

    print(f"Gráficos salvos em: {OUTPUT_DIR}")

if __name__ == "__main__":
    gerar_graficos()
