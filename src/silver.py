"""Silver: leitura, padronização, validação e consolidação dos CSVs do INMET."""
import csv
import re
from pathlib import Path
import pandas as pd

from config import (
    BRONZE_DIR, SILVER_FILE, MISSING_VALUES,
    PRECIPITATION_COLUMN_HINT, SOURCE_TIMEZONE, LOCAL_TIMEZONE
)

def encontrar_linha_cabecalho(caminho: Path, max_linhas: int = 40) -> int:
    """Localiza a linha de cabeçalho em CSVs que possuem metadados no início."""
    with caminho.open("r", encoding="latin1", errors="replace") as arquivo:
        for indice, linha in enumerate(arquivo):
            if indice >= max_linhas:
                break
            campos = [campo.strip().strip('"').lower() for campo in linha.split(";")]
            tem_data = any("data" in campo for campo in campos)
            tem_hora = any("hora" in campo for campo in campos)
            if tem_data and tem_hora:
                return indice
    return 0

def ler_csv_inmet(caminho: Path) -> pd.DataFrame:
    """Lê um CSV INMET com separador ;, decimal , e cabeçalho variável."""
    linha = encontrar_linha_cabecalho(caminho)
    tentativas = [
        {"sep": ";", "decimal": ",", "encoding": "latin1", "skiprows": linha},
        {"sep": ";", "decimal": ".", "encoding": "utf-8", "skiprows": linha},
    ]
    erro = None
    for parametros in tentativas:
        try:
            return pd.read_csv(caminho, **parametros, low_memory=False)
        except Exception as exc:
            erro = exc
    raise RuntimeError(f"Não foi possível ler {caminho}: {erro}")

def normalizar_nome_coluna(nome: str) -> str:
    nome = str(nome).strip().lower()
    nome = re.sub(r"\s+", "_", nome)
    nome = nome.replace("(", "").replace(")", "")
    return nome

def encontrar_coluna(df: pd.DataFrame, candidatos: list[str]) -> str | None:
    colunas = {normalizar_nome_coluna(c): c for c in df.columns}
    for candidato in candidatos:
        chave = normalizar_nome_coluna(candidato)
        if chave in colunas:
            return colunas[chave]
    # Busca parcial para diferenças de acentuação/abreviação nos arquivos.
    for coluna in df.columns:
        texto = normalizar_nome_coluna(coluna)
        if all(palavra in texto for palavra in candidatos[0].lower().split()[:2]):
            return coluna
    return None

def localizar_precipitacao(df: pd.DataFrame) -> str:
    hint = PRECIPITATION_COLUMN_HINT
    normalizadas = {normalizar_nome_coluna(c): c for c in df.columns}
    chave = normalizar_nome_coluna(hint)
    if chave in normalizadas:
        return normalizadas[chave]
    for coluna in df.columns:
        nome = normalizar_nome_coluna(coluna)
        if "precip" in nome and ("hor" in nome or "total" in nome):
            return coluna
    raise ValueError(
        "Coluna de precipitação não encontrada. Confira o cabeçalho do CSV "
        "e ajuste PRECIPITATION_COLUMN_HINT em src/config.py."
    )

def preparar_arquivo(caminho: Path) -> pd.DataFrame:
    df = ler_csv_inmet(caminho)
    df.columns = [str(c).strip() for c in df.columns]

    col_data = encontrar_coluna(df, ["DATA"])
    col_hora = encontrar_coluna(df, ["HORA UTC", "HORA"])
    col_precip = localizar_precipitacao(df)

    if col_data is None or col_hora is None:
        raise ValueError(f"Colunas de data/hora não encontradas em {caminho.name}")

    data = df[col_data].astype("string").str.strip()
    hora = df[col_hora].astype("string").str.strip()

    # Exemplos comuns: 2020-01-01 e 0000 UTC / 00:00 / 00:00:00.
    hora = hora.str.replace(r"\s*UTC\s*$", "", regex=True)
    hora = hora.str.replace(r"^(\d{2})(\d{2})$", r"\1:\2", regex=True)
    hora = hora.str.slice(0, 8)

    timestamp = pd.to_datetime(
        data + " " + hora,
        errors="coerce",
        dayfirst=True
    )

    precipitacao = pd.to_numeric(
        df[col_precip].replace(MISSING_VALUES, pd.NA),
        errors="coerce"
    )

    resultado = pd.DataFrame({
        "data_hora_utc": timestamp,
        "precipitacao_mm": precipitacao,
        "arquivo_origem": caminho.name,
    })

    resultado = resultado.dropna(subset=["data_hora_utc"])
    # A coluna de origem é mantida para rastreabilidade.
    resultado["data_hora_utc"] = (
        resultado["data_hora_utc"]
        .dt.tz_localize(SOURCE_TIMEZONE, ambiguous="NaT", nonexistent="NaT")
    )
    resultado["data_hora_local"] = (
        resultado["data_hora_utc"].dt.tz_convert(LOCAL_TIMEZONE)
    )
    resultado["ano"] = resultado["data_hora_local"].dt.year
    resultado["mes"] = resultado["data_hora_local"].dt.month
    resultado["dia"] = resultado["data_hora_local"].dt.day
    resultado["hora"] = resultado["data_hora_local"].dt.hour

    # Precipitação negativa não sentinela é marcada como inválida.
    resultado.loc[resultado["precipitacao_mm"] < 0, "precipitacao_mm"] = pd.NA
    return resultado

def construir_silver() -> pd.DataFrame:
    arquivos = sorted(
        set(BRONZE_DIR.glob("**/*.csv")) |
        set(BRONZE_DIR.glob("**/*.CSV"))
    )
    if not arquivos:
        raise FileNotFoundError(
            f"Nenhum CSV encontrado em {BRONZE_DIR}. "
            "Coloque os arquivos históricos do INMET nessa pasta."
        )

    partes = []
    erros = []
    for arquivo in arquivos:
        try:
            partes.append(preparar_arquivo(arquivo))
            print(f"OK: {arquivo.name}")
        except Exception as exc:
            erros.append((arquivo.name, str(exc)))
            print(f"AVISO: {arquivo.name} ignorado: {exc}")

    if not partes:
        raise RuntimeError("Nenhum arquivo foi processado com sucesso.")

    silver = pd.concat(partes, ignore_index=True)
    silver = silver.sort_values("data_hora_local")
    # Duplicatas de timestamp podem ocorrer em arquivos sobrepostos.
    silver = silver.drop_duplicates(
        subset=["data_hora_utc", "precipitacao_mm"],
        keep="first"
    )

    SILVER_FILE.parent.mkdir(parents=True, exist_ok=True)
    silver.to_csv(SILVER_FILE, index=False, encoding="utf-8")
    print(f"Silver salva: {SILVER_FILE}")
    print(f"Registros tratados: {len(silver):,}")
    if erros:
        print(f"Arquivos com erro: {len(erros)}")
    return silver

if __name__ == "__main__":
    construir_silver()
