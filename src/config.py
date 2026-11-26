from pathlib import Path

# Ajuste para a pasta onde você guardou os CSVs originais do INMET.
PROJECT_ROOT = Path(__file__).resolve().parents[1]
BRONZE_DIR = PROJECT_ROOT / "data" / "bronze" / "inmet"
SILVER_DIR = PROJECT_ROOT / "data" / "silver"
GOLD_DIR = PROJECT_ROOT / "data" / "gold"
OUTPUT_DIR = PROJECT_ROOT / "outputs"

# Nome da coluna de precipitação nos arquivos do INMET.
# O pipeline também tenta encontrá-la automaticamente por palavras-chave.
PRECIPITATION_COLUMN_HINT = "PRECIPITAÇÃO TOTAL, HORÁRIO (mm)"

# O INMET costuma disponibilizar "Hora UTC". Para obter o horário de Belém,
# convertemos UTC para America/Belem.
SOURCE_TIMEZONE = "UTC"
LOCAL_TIMEZONE = "America/Belem"

# Valores sentinela usados em alguns arquivos para representar dado ausente.
MISSING_VALUES = [-9999, -9999.0, "-9999", ""]

# Arquivos CSV gerados pelo pipeline.
SILVER_FILE = SILVER_DIR / "precipitacao_tratada.csv"
GOLD_HOURLY_FILE = GOLD_DIR / "chuva_por_hora.csv"
GOLD_MONTHLY_FILE = GOLD_DIR / "chuva_por_mes.csv"
GOLD_YEARLY_FILE = GOLD_DIR / "chuva_por_ano.csv"
