import streamlit as st
import pandas as pd
from fpdf import FPDF
from datetime import datetime

# ---------- Helpers ----------
def moeda(v):
    try:
        return f"R$ {float(v):,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")
    except:
        return str(v)

def float_pt(s):
    if s is None or s == "":
        return 0.0
    if isinstance(s, (int, float)):
        return float(s)
    return float(str(s).replace(".", "").replace(",", "."))

def numero_pedido():
    return datetime.now().strftime("%d%H%Y%M")

def tot_geral(df):
    if df.empty:
        return 0.0
    x = df.copy()
    x["Qtd(Kg)"] = x["Qtd(Kg)"].apply(float_pt)
    x["Valor_Unitario"] = x["Valor_Unitario"].apply(float_pt)
    x["Subtotal"] = x["Qtd(Kg)"] * x["Valor_Unitario"]
    return float(x["Subtotal"].sum())

# ---------- PDF ----------
class PedidoPDF(FPDF):
    def __init__(self):
        super().__init__("P", "mm", "A4")
        self.set_auto_page_break(auto=False)
        self.add_page()

    def cabecalho(self, pedido_id, emitido_em):

        try:
            self.image("logo_solobom.png", x=10, y=13, w=25)  # x, y em mm, w = largura
        except:
            pass  # se não encontrar, ignora
        self.set_font("Helvetica", "B", 14)
        self.cell(0, 8, "PEDIDO DE VENDA", ln=1, align="C")
        self.set_font("Helvetica", "", 10)
        self.cell(0, 6, f"Número do Pedido: {pedido_id}    Emitido em: {emitido_em}", ln=1, align="C")
        self.ln(4)

    def tabela_comprador_vendedor(self, vendedor: dict, comprador: dict):
        self.set_font("Helvetica", "B", 11)
        self.cell(0, 7, "Vendedor / Comprador", ln=1)
        self.set_draw_color(200, 200, 200)
        self.line(10, self.get_y(), 200, self.get_y())
        self.ln(2)

        self.set_font("Helvetica", "", 10)
        page_width = self.w - 2 * self.l_margin
        col_width = (page_width - 10) / 2

        v_items = list(vendedor.items())
        c_items = list(comprador.items())
        max_len = max(len(v_items), len(c_items))
        while len(v_items) < max_len:
            v_items.append(("", ""))
        while len(c_items) < max_len:
            c_items.append(("", ""))

        line_height = 6
        for (vk, vv), (ck, cv) in zip(v_items, c_items):
            x_start = self.l_margin
            y_start = self.get_y()
            # Vendedor
            self.set_xy(x_start, y_start)
            self.multi_cell(col_width, line_height, f"{vk}: {vv}", border=0)
            # Comprador
            self.set_xy(x_start + col_width + 10, y_start)
            self.multi_cell(col_width, line_height, f"{ck}: {cv}", border=0)
            self.set_y(max(self.get_y(), y_start + line_height))
        self.ln(4)

    def tabela_condicoes(self, condicoes: dict):
        # Transformar em duas colunas
        self._tabela_dupla("Detalhes Entrega/Pagamento", condicoes, {})

    def _tabela_dupla(self, titulo, esquerda: dict, direita: dict):
        self.set_font("Helvetica", "B", 11)
        self.cell(0, 7, titulo, ln=1)
        self.set_draw_color(200, 200, 200)
        self.line(10, self.get_y(), 200, self.get_y())
        self.ln(2)
        self.set_font("Helvetica", "", 10)

        page_width = self.w - 2 * self.l_margin
        col_width = (page_width - 10) / 2
        left_items = list(esquerda.items())
        right_items = list(direita.items())
        max_len = max(len(left_items), len(right_items))
        while len(left_items) < max_len:
            left_items.append(("", ""))
        while len(right_items) < max_len:
            right_items.append(("", ""))

        line_height = 6
        for (lk, lv), (rk, rv) in zip(left_items, right_items):
            y_start = self.get_y()
            self.set_xy(self.l_margin, y_start)
            self.multi_cell(col_width, line_height, f"{lk}: {lv}", border=0)
            self.set_xy(self.l_margin + col_width + 10, y_start)
            self.multi_cell(col_width, line_height, f"{rk}: {rv}" if rk else "", border=0)
            self.set_y(max(self.get_y(), y_start + line_height))
        self.ln(4)

    def pix(self):
        # Transformar em duas colunas
        self.ln(10)
        self.set_font("Helvetica", "", 10)
        self.multi_cell(0, 5, "\n PIX: mtq341370045@grupomantiqueira.com.br (Mantiqueira Alimentos Ltda.)")

    def tabela_itens(self, df):
        self.ln(10)
        self.set_font("Helvetica", "B", 10)
        cols = ["Item", "Descrição", "Qtd(Kg)", "Valor_Unitario", "Subtotal"]
        widths = [15, 90, 20, 30, 30]
        for c, w in zip(cols, widths):
            self.cell(w, 7, c, border=1, align="C")
        self.ln()
        self.set_font("Helvetica", "", 10)
        if df.empty:
            self.cell(sum(widths), 8, "Nenhum item informado.", border=1, ln=1, align="C")
            return
        for i, row in enumerate(df.itertuples(), 1):
            qtd = float_pt(getattr(row, "Qtd(Kg)", 0))
            vu  = float_pt(getattr(row, "Valor_Unitario", 0))
            sub = qtd * vu
            self.cell(widths[0], 7, str(i), border=1, align="C")
            self.cell(widths[1], 7, str(getattr(row, "Descrição", ""))[:50], border=1)
            self.cell(widths[2], 7, f"{qtd:g}", border=1, align="R")
            self.cell(widths[3], 7, moeda(vu), border=1, align="R")
            self.cell(widths[4], 7, moeda(sub), border=1, align="R")
            self.ln()
        self.ln(2)

    def total(self, valor):
        self.set_font("Helvetica", "B", 11)
        self.cell(0, 8, f"TOTAL: {moeda(valor)}", ln=1, align="R")
        self.ln(4)

    def assinaturas(self):
        y = self.get_y()
        w = 80
        #self.line(15, y+18, 15+w, y+18)
        self.set_xy(15, y+20)
        
        self.line(110, y+18, 110+w, y+18)
        self.set_xy(110, y+20)
        self.cell(w, 6, "Assinatura do Cliente", align="C")
        #self.cell(w, 6, "Assinatura MAnt", align="C")
        self.ln(25)
        self.set_font("Helvetica", "", 8)
        self.multi_cell(0, 5, "Ao assinar, o cliente confirma ciência de valores, prazos e condições descritas neste pedido.")

# ---------- Streamlit UI ----------
st.title("🧾 Gerador de Pedido de Venda")

with st.form("form_pedido"):
    # Vendedor
    st.subheader("Empresa (Vendedor)")
    col1, col2 = st.columns(2)
    cidade = st.selectbox("Granja:", ["PRIMAVERA","CAMPANHA"])

    if cidade == "PRIMAVERA":
        emp_nome   = col1.text_input("Razão Social / Nome Fantasia", "MANTIQUEIRA ALIMENTOS S/A", key="emp_nome")
        emp_cnpj   = col2.text_input("CNPJ/CPF", "04.747.794/0008-89", key="emp_cnpj")
        emp_end    = st.text_input("Endereço", "Rodovia MT 130, Km 15 + 1 Km à Esquerda", key="emp_end")
        emp_contato= st.text_input("Contato (e-mail/telefone)", key="emp_contato")
    else:
        emp_nome   = col1.text_input("Razão Social / Nome Fantasia", "MANTIQUEIRA ALIMENTOS S/A", key="emp_nome")
        emp_cnpj   = col2.text_input("CNPJ/CPF", "04.747.794/0002-93", key="emp_cnpj")
        emp_end    = st.text_input("Endereço", "Rodovia Fernão Dias (BR 381), S/N", key="emp_end")
        emp_contato= st.text_input("Contato (e-mail/telefone)", key="emp_contato")

    # Comprador
    st.subheader("Cliente (Comprador)")
    col1, col2 = st.columns(2)
    cli_nome   = col1.text_input("Nome/Razão Social" , key="cli_nome")
    cli_doc    = col2.text_input("CNPJ/CPF", key="cli_doc")
    cli_end    = st.text_input("Endereço", key="cli_end")
    ins_est    = st.text_input("Inscrição Estadual", key="emp_end")
    cli_contato= st.text_input("Contato (e-mail/telefone)", key="cli_contato")

    # Condições
    st.subheader("Detalhes Entrega/Pagamento")
    col1, col2, col3 = st.columns(3)
    produto    = col1.selectbox("Produto Safra:", ["Milho", "Soja"], key="produto")
    pagamento  = col2.date_input("Data de pagamento:", key="pagamento", format="DD/MM/YYYY")
    pagamento = pagamento.strftime("%d/%m/%Y")
    entrega    = col3.date_input("Data de entrega:", key="entrega", format="DD/MM/YYYY")
    entrega = entrega.strftime("%d/%m/%Y")
    frete      = col4.selectbox("Tipo Frete:", ["CIF", "FOB"], key="frete")
    obs        = st.text_area("Dados Bancários:", "\n Itaú Unibanco S.A (Cód.: 341) \n Agência: 3032 \n C. Corrente: 37004-5", key="obs")

    # Itens
    st.subheader("Itens do Pedido")
    df_itens = st.data_editor(
        pd.DataFrame([{"Descrição": "Produto A", "Qtd(Kg)": 1, "Valor_Unitario": 100.00}]),
        num_rows="dynamic",
        use_container_width=True,
        column_config={
            "Descrição": st.column_config.TextColumn("Descrição", required=True),
            "Qtd(Kg)": st.column_config.NumberColumn("Qtd(Kg)", min_value=0.0, step=0.01, format="%.2f"),
            "Valor_Unitario": st.column_config.NumberColumn("Valor_Unitario", min_value=0.0, step=0.01, format="%.2f"),
        },
        key="grid_itens"
    )

    enviado = st.form_submit_button("Gerar PDF")

if enviado:
    total = tot_geral(df_itens)
    pedido_id = numero_pedido()
    emitido_em = datetime.now().strftime("%d/%m/%Y")

    # PDF
    pdf = PedidoPDF()
    pdf.cabecalho(pedido_id, emitido_em)

    pdf.tabela_comprador_vendedor(
        vendedor={"Empresa": emp_nome, "CNPJ/CPF": emp_cnpj, "Endereço": emp_end, "Contato": emp_contato},
        comprador={"Nome/Razão Social": cli_nome, "CNPJ/CPF": cli_doc, "Endereço": cli_end, "Inscrição": ins_est, "Contato": cli_contato}
    )

    pdf.tabela_condicoes({
        "Produto Safra": produto,
        "Data de pagamento": pagamento,
        "Data de entrega": entrega,
        "Frete": frete,
        "Observações": obs
    })

    pdf.pix()

    pdf.tabela_itens(df_itens)
    pdf.total(total)
    pdf.assinaturas()

    # Gerar PDF só em memória
    pdf_bytes = bytes(pdf.output(dest="S"))

    # Preview no Streamlit
    st.pdf(pdf_bytes, height=500, key="preview_pdf")

    # Botão de download
    st.download_button(
        "⬇️ Baixar PDF do Pedido",
        data=pdf_bytes,
        file_name=f"pedido_{pedido_id}.pdf",
        mime="application/pdf",
        key="download_pdf"
    )
