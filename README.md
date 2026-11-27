# Análise de Dados Meteorológicos — INMET

Este repositório contém a estrutura, os scripts e os dados meteorológicos extraídos da base oficial do **Instituto Nacional de Meteorologia (INMET)**, coletados em **15 de novembro de 2026**.

---

## 📋 Sobre o Projeto

O objetivo deste projeto é processar, tratar e analisar séries históricas e registros climáticos das estações meteorológicas do INMET para extração de indicadores climáticos, tendências e visualizações.

---

## 🗂️ Fonte dos Dados

* **Órgão:** Instituto Nacional de Meteorologia (INMET)
* **Portal:** [BDMEP — Banco de Dados Meteorológicos](https://inmet.gov.br) / [Portal INMET](https://inmet.gov.br)
* **Data de extração (download):** 15/11/2026
* **Formato original:** Arquivos `.csv` (separados por ponto e vírgula `;`, codificação `ISO-8859-1` ou `UTF-8`)

### Principais Variáveis Contidas nas Bases
* Data e Hora (UTC)
* Precipitação Total (mm)
* Pressão Atmosférica (mB)
* Temperatura do Ar — Bulbo Seco (°C)
* Temperatura Máxima e Mínima (°C)
* Umidade Relativa do Ar (%)
* Direção e Velocidade do Vento (m/s)

---

## 📁 Estrutura de Diretórios

```text
├── data/
│   ├── raw/                 # Arquivos brutos baixados do INMET em 15/11/2026
│   └── processed/           # Dados limpos, tratados e prontos para análise
├── notebooks/               # Jupyter Notebooks com análises exploratórias
├── src/                     # Scripts de ETL, limpeza e geração de gráficos
├── reports/                 # Relatórios, tabelas e figuras exportadas
├── requirements.txt         # Dependências do projeto
└── README.md                # Documentação do projeto
```

---

## ⚙️ Pré-requisitos e Instalação

1. **Clone o repositório:**
   ```bash
   git clone https://github.com
   cd seu-repositorio
   ```

2. **Crie e ative um ambiente virtual (opcional, mas recomendado):**
   ```bash
   python -m venv venv
   source venv/bin/activate  # Linux/Mac
   venv\Scripts\activate     # Windows
   ```

3. **Instale as dependências:**
   ```bash
   pip install -r requirements.txt
   ```

---

## 🚀 Como Executar

1. Certifique-se de que os arquivos `.csv` baixados estejam na pasta `data/bronze/INMET`.
2. Execute o script main para limpeza e padronização dos dados (ajuste de cabeçalhos, tratamento de valores ausentes `-9999` ou `NaN` e conversão de tipos):
   ```bash
   python src/main.py
   ```
3. Abra os notebooks na pasta `notebooks/` para visualizar as análises e gráficos.

---

## ⚠️ Notas sobre os Dados do INMET

* Os arquivos brutos do INMET costumam apresentar **8 linhas de metadados** no cabeçalho antes do início da tabela de registros.
* Valores ausentes ou falhas de leitura nas estações automáticas geralmente vêm preenchidos como `-9999` ou células vazias.
* O separador decimal padrão dos arquivos brasileiros do INMET é a vírgula (`,`).

---

## 📄 Licença

Este projeto está sob a licença MIT. Os dados pertencem ao domínio público conforme as diretrizes de dados abertos do INMET.