"""Ingestão: localiza os CSVs e preserva os dados originais na Bronze."""
import glob
import shutil
from pathlib import Path
from config import BRONZE_DIR

def listar_csvs(pasta: Path = BRONZE_DIR) -> list[Path]:
    """Busca CSVs recursivamente. Aceita extensão .csv em qualquer caixa."""
    encontrados = glob.glob(str(pasta / "**" / "*.csv"), recursive=True)
    encontrados += glob.glob(str(pasta / "**" / "*.CSV"), recursive=True)
    return sorted({Path(caminho) for caminho in encontrados})

def copiar_para_bronze(arquivos: list[Path], origem_raiz: Path) -> int:
    """
    Copia arquivos para Bronze mantendo subpastas relativas.
    Se os arquivos já estiverem na Bronze, não é necessário copiá-los.
    """
    BRONZE_DIR.mkdir(parents=True, exist_ok=True)
    copiados = 0
    for arquivo in arquivos:
        try:
            relativo = arquivo.relative_to(origem_raiz)
        except ValueError:
            relativo = Path(arquivo.name)
        destino = BRONZE_DIR / relativo
        destino.parent.mkdir(parents=True, exist_ok=True)
        if arquivo.resolve() != destino.resolve():
            shutil.copy2(arquivo, destino)
            copiados += 1
    return copiados

if __name__ == "__main__":
    csvs = listar_csvs()
    print(f"CSV(s) encontrados na Bronze: {len(csvs)}")
    for arquivo in csvs:
        print(arquivo)
