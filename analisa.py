import os
import subprocess
import re
import pandas as pd
from fpdf import FPDF

INPUT_FILE = "cadastros.xlsx"
OUTPUT_FOLDER = "saida"
OUTPUT_APTOS_PDF = os.path.join(OUTPUT_FOLDER, "aptos.pdf")
OUTPUT_INAPTOS_PDF = os.path.join(OUTPUT_FOLDER, "inaptos.pdf")

os.makedirs(OUTPUT_FOLDER, exist_ok=True)

def validar_cpf(cpf):
    cpf = ''.join(filter(str.isdigit, str(cpf)))
    if len(cpf) != 11 or cpf == cpf[0] * 11:
        return False
    for i in [9, 10]:
        soma = sum(int(cpf[j]) * ((i+1) - j) for j in range(i))
        dig = ((soma * 10) % 11) % 10
        if dig != int(cpf[i]):
            return False
    return True

def esta_apto(linha):
    cpf = str(linha.get('CPF', '')).strip().zfill(11)
    rg = str(linha.get('RG', '')).strip()
    horas = linha.get('Horas_Trator', 0)
    idade = linha.get('Idade', 0)
    email = str(linha.get('Email', '')).strip()

    if not validar_cpf(cpf):
        return False
    if len(rg) < 5 or not rg.replace('.', '').replace('-', '').isalnum():
        return False
    if not isinstance(horas, (int, float)) or pd.isna(horas) or horas <= 0:
        return False
    if not isinstance(idade, (int, float)) or idade <= 0 or idade > 120:
        return False
    if not re.match(r"[^@]+@[^@]+\.[^@]+", email):
        return False

    return True

def carregar_dados(arquivo):
    try:
        print("📑 Carregando dados...")
        return pd.read_excel(arquivo)
    except Exception as e:
        print(f"❌ Erro ao abrir o arquivo: {e}")
        exit()

def gerar_pdf(dados, caminho_pdf, titulo):
    if dados.empty:
        print(f"⚠️ Nenhum cadastro {titulo}.")
        return

    pdf = FPDF(orientation='P', unit='mm', format='A4')
    pdf.add_page()
    pdf.set_auto_page_break(auto=True, margin=10)

    pdf.set_font("Helvetica", 'B', 14)
    pdf.cell(0, 10, f"Relatório de {titulo} - Secretaria de Cultura", ln=True, align='C')
    pdf.ln(5)

    pdf.set_font("Helvetica", size=10)

    for idx, row in dados.iterrows():
        pdf.set_fill_color(230, 230, 250)
        pdf.cell(0, 8, f"{idx+1}. {row.get('Nome', 'N/A')}", ln=True, fill=True)

        pdf.set_font("Helvetica", size=9)
        pdf.multi_cell(0, 6,
            f"CPF: {str(row.get('CPF', '')).zfill(11)}  |  RG: {row.get('RG', 'N/A')}\n"
            f"Horas Trator: {row.get('Horas_Trator', 0)}  |  Idade: {row.get('Idade', 'N/A')}\n"
            f"Localidade: {row.get('Localidade', 'N/A')}  |  Email: {row.get('Email', 'N/A')}"
        )
        pdf.ln(2)

    pdf.output(caminho_pdf)
    print(f"📄 PDF de {titulo} gerado: {caminho_pdf}")

def abrir_arquivo(caminho):
    try:
        if os.name == 'nt':
            os.startfile(caminho)
        elif os.name == 'posix':
            subprocess.run(['open' if os.uname().sysname == 'Darwin' else 'xdg-open', caminho])
    except Exception as e:
        print(f"⚠️ Não foi possível abrir o PDF: {e}")

def processar():
    df = carregar_dados(INPUT_FILE)
    validos = df.apply(esta_apto, axis=1)

    aptos = df[validos].reset_index(drop=True)
    inaptos = df[~validos].reset_index(drop=True)

    print("\n========= RESUMO =========")
    print(f"🔍 Total: {len(df)}")
    print(f"✅ Aptos: {len(aptos)}")
    print(f"❌ Inaptos: {len(inaptos)}")
    print("==========================")

    gerar_pdf(aptos, OUTPUT_APTOS_PDF, "Aptos")
    gerar_pdf(inaptos, OUTPUT_INAPTOS_PDF, "Inaptos")

    if not aptos.empty: abrir_arquivo(OUTPUT_APTOS_PDF)
    if not inaptos.empty: abrir_arquivo(OUTPUT_INAPTOS_PDF)

    print("\n🏁 Finalizado com sucesso!")

if __name__ == "__main__":
    processar()
