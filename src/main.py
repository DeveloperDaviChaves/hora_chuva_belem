"""Executa o pipeline Bronze -> Silver -> Gold -> gráficos."""
from silver import construir_silver
from gold import construir_gold
from visualization import gerar_graficos

def main():
    print("=== ETAPA SILVER ===")
    silver = construir_silver()

    print("\n=== ETAPA GOLD ===")
    construir_gold(silver)

    print("\n=== VISUALIZAÇÕES ===")
    gerar_graficos()

    print("\nPipeline concluído.")

if __name__ == "__main__":
    main()
