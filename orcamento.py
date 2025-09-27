import tkinter as tk
from tkinter import ttk, messagebox
import sqlite3

# ==============================
# Paleta de cores
# ==============================
BG_DARK = "#2E2E2E"
BTN = "#FF5733"
BTN_ACTIVE = "#FF4515"
FG = "white"

# ==============================
# Banco de Dados (SQLite)
# ==============================
def inicializar_banco():
    con = sqlite3.connect("clientes.db")
    cur = con.cursor()
    cur.execute("""
        CREATE TABLE IF NOT EXISTS clientes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT NOT NULL,
            os_numero TEXT NOT NULL,
            telefone TEXT NOT NULL,
            cpf TEXT NOT NULL,
            endereco TEXT NOT NULL,
            medidas TEXT NOT NULL,
            valor TEXT NOT NULL,
            pagamento TEXT NOT NULL
        )
    """)
    con.commit()
    con.close()

def adicionar_cliente(nome, os_numero, telefone, cpf, endereco, medidas, valor, pagamento):
    con = sqlite3.connect("clientes.db")
    cur = con.cursor()
    cur.execute("""
        INSERT INTO clientes (nome, os_numero, telefone, cpf, endereco, medidas, valor, pagamento)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    """, (nome, os_numero, telefone, cpf, endereco, medidas, valor, pagamento))
    con.commit()
    con.close()

def listar_clientes():
    con = sqlite3.connect("clientes.db")
    cur = con.cursor()
    cur.execute("SELECT * FROM clientes ORDER BY id DESC")
    dados = cur.fetchall()
    con.close()
    return dados

def atualizar_cliente_db(_id, nome, os_numero, telefone, cpf, endereco, medidas, valor, pagamento):
    con = sqlite3.connect("clientes.db")
    cur = con.cursor()
    cur.execute("""
        UPDATE clientes
        SET nome=?, os_numero=?, telefone=?, cpf=?, endereco=?, medidas=?, valor=?, pagamento=?
        WHERE id=?
    """, (nome, os_numero, telefone, cpf, endereco, medidas, valor, pagamento, _id))
    con.commit()
    con.close()

def excluir_cliente_db(_id):
    con = sqlite3.connect("clientes.db")
    cur = con.cursor()
    cur.execute("DELETE FROM clientes WHERE id=?", (_id,))
    con.commit()
    con.close()

# ==============================
# Calculadora de Orçamentos (Toplevel)
# ==============================
def abrir_calculadora():
    janela_calc = tk.Toplevel()
    janela_calc.title("Orçamento de Tela Mosquiteira")
    janela_calc.geometry("600x900")
    janela_calc.configure(bg=BG_DARK)

    valores_comodos = {}

    def calcular_preco():
        try:
            altura = float(entrada_altura.get())
            largura = float(entrada_largura.get())
            if altura <= 0 or largura <= 0:
                raise ValueError("Altura e largura devem ser valores positivos.")

            area = (altura * largura) / 10000
            preco = area * 329

            comodo = combo_comodo.get()
            valores_comodos[comodo] = {"altura": altura, "largura": largura, "area": area, "preco": preco}

            atualizar_lista_comodos()
            calcular_total()

        except ValueError as e:
            messagebox.showerror("Erro", f"Erro ao calcular preço: {str(e)}", parent=janela_calc)

    def atualizar_lista_comodos():
        lista_comodos.delete(0, tk.END)
        for comodo, valores in valores_comodos.items():
            texto = f"{comodo}: R$ {valores['preco']:.2f}"
            lista_comodos.insert(tk.END, texto)

    def calcular_total():
        total = sum(v['preco'] for v in valores_comodos.values())
        total_com_desconto = total * 0.95
        parcela = total / 3 if total > 0 else 0

        label_total.config(text=f"Total: R$ {total:.2f}")
        label_total_com_desconto.config(text=f"Total à vista: R$ {total_com_desconto:.2f}")
        label_parcela.config(text=f"3x sem juros: R$ {parcela:.2f}")

    def copiar_todos_comodos():
        todos = []
        for comodo, v in valores_comodos.items():
            todos.append(f"{comodo}: {v['altura']}cm x {v['largura']}cm = R$ {v['preco']:.2f}")
        resumo = "\n".join(todos)
        resumo += "\n" + label_total.cget("text")
        resumo += "\n" + label_total_com_desconto.cget("text")
        resumo += "\n" + label_parcela.cget("text")

        janela_calc.clipboard_clear()
        janela_calc.clipboard_append(resumo)
        janela_calc.update()
        messagebox.showinfo("Sucesso", "Itens e totais copiados!", parent=janela_calc)

    def reiniciar_orcamento():
        entrada_altura.delete(0, tk.END)
        entrada_largura.delete(0, tk.END)
        valores_comodos.clear()
        lista_comodos.delete(0, tk.END)
        label_total.config(text="Total: R$ 0.00")
        label_total_com_desconto.config(text="Total à vista: R$ 0.00")
        label_parcela.config(text="3x sem juros: R$ 0.00")
        combo_comodo.set(opcoes_comodos[0])

    def botao(parent, texto, comando, w=20, h=2):
        return tk.Button(parent, text=texto, command=comando, fg=FG, bg=BTN,
                         activebackground=BTN_ACTIVE, font=("Helvetica", 12, "bold"),
                         relief="flat", bd=0, width=w, height=h)

    tk.Label(janela_calc, text="Orçamento telas mosquiteiras",
             fg=FG, bg=BG_DARK, font=("Helvetica", 16, "bold")).pack(pady=20)

    opcoes_comodos = ["Quarto casal", "Quarto filho", "Quarto filha", "Banheiro social",
                      "Banheiro suíte", "Banheiro suíte filho", "Banheiro suíte filha",
                      "Lavabo", "Sala", "Cozinha", "Área técnica", "Sacada", "Vão"]
    combo_comodo = ttk.Combobox(janela_calc, values=opcoes_comodos, state="readonly", font=("Helvetica", 10))
    combo_comodo.current(0)
    combo_comodo.pack(pady=5)

    tk.Label(janela_calc, text="Altura (cm):", fg=FG, bg=BG_DARK, font=("Helvetica", 10)).pack(pady=5)
    entrada_altura = tk.Entry(janela_calc, font=("Helvetica", 10), justify="center", width=20)
    entrada_altura.pack(pady=5)

    tk.Label(janela_calc, text="Largura (cm):", fg=FG, bg=BG_DARK, font=("Helvetica", 10)).pack(pady=5)
    entrada_largura = tk.Entry(janela_calc, font=("Helvetica", 10), justify="center", width=20)
    entrada_largura.pack(pady=5)

    botao(janela_calc, "Calcular Preço", calcular_preco).pack(pady=10)

    lista_comodos = tk.Listbox(janela_calc, width=60, height=10, font=("Helvetica", 10),
                               bg="#555555", fg=FG, selectmode=tk.SINGLE, bd=0, relief="flat")
    lista_comodos.pack(pady=10)

    label_total = tk.Label(janela_calc, text="Total: R$ 0.00", font=("Helvetica", 12, "bold"), fg=FG, bg=BG_DARK)
    label_total.pack(pady=5)
    label_total_com_desconto = tk.Label(janela_calc, text="Total à vista: R$ 0.00", font=("Helvetica", 12, "bold"), fg=FG, bg=BG_DARK)
    label_total_com_desconto.pack(pady=5)
    label_parcela = tk.Label(janela_calc, text="3x sem juros: R$ 0.00", font=("Helvetica", 12, "bold"), fg=FG, bg=BG_DARK)
    label_parcela.pack(pady=5)

    botao(janela_calc, "Copiar tudo", copiar_todos_comodos).pack(pady=5)
    botao(janela_calc, "Reiniciar Orçamento", reiniciar_orcamento).pack(pady=10)

# ==============================
# Banco de Clientes (Toplevel)
# ==============================
def abrir_banco_clientes():
    janela = tk.Toplevel()
    janela.title("Banco de Clientes")
    janela.geometry("1100x600")
    janela.configure(bg="#1E1E2E")  # fundo moderno escuro

    # ==========================
    # Estilo Treeview moderno
    # ==========================
    style = ttk.Style(janela)
    try:
        style.theme_use("clam")
    except tk.TclError:
        pass

    style.configure("Treeview",
                    background="#2A2A3F", fieldbackground="#2A2A3F",
                    foreground="#FFFFFF", rowheight=30, borderwidth=0, font=("Helvetica", 11))
    style.configure("Treeview.Heading",
                    background="#FF6F61", foreground="#FFFFFF", font=("Helvetica", 11, "bold"))
    style.map("Treeview", background=[("selected", "#555555")])

    # ==========================
    # Frame único: botões + filtro/pesquisa
    # ==========================
    frame_top = tk.Frame(janela, bg="#1E1E2E")
    frame_top.pack(fill="x", padx=12, pady=8)

    # Função hover nos botões
    def hover_color(btn, cor_entrada, cor_saida):
        btn.bind("<Enter>", lambda e: btn.config(bg=cor_entrada))
        btn.bind("<Leave>", lambda e: btn.config(bg=cor_saida))

    # Botões
    btn_cadastrar = tk.Button(frame_top, text="Cadastrar", fg="#FFFFFF", bg="#FF6F61",
                              font=("Helvetica", 11, "bold"), relief="flat", bd=0, width=15, height=2)
    btn_cadastrar.pack(side="left", padx=5)
    hover_color(btn_cadastrar, "#FF4B3E", "#FF6F61")

    btn_editar = tk.Button(frame_top, text="Editar", fg="#FFFFFF", bg="#FF6F61",
                           font=("Helvetica", 11, "bold"), relief="flat", bd=0, width=15, height=2)
    btn_editar.pack(side="left", padx=5)
    hover_color(btn_editar, "#FF4B3E", "#FF6F61")

    btn_excluir = tk.Button(frame_top, text="Excluir", fg="#FFFFFF", bg="#FF6F61",
                            font=("Helvetica", 11, "bold"), relief="flat", bd=0, width=15, height=2)
    btn_excluir.pack(side="left", padx=5)
    hover_color(btn_excluir, "#FF4B3E", "#FF6F61")

    # Combobox filtro
    opcoes_filtro = ["Nº OS", "Nome", "Telefone", "CPF", "Endereço"]
    var_filtro = tk.StringVar(value=opcoes_filtro[0])
    combo_filtro = ttk.Combobox(frame_top, values=opcoes_filtro, textvariable=var_filtro,
                                state="readonly", width=12, font=("Helvetica", 11))
    combo_filtro.pack(side="left", padx=(30,5))

    # Caixa de pesquisa
    var_busca = tk.StringVar()
    entrada_busca = tk.Entry(frame_top, textvariable=var_busca, font=("Helvetica", 11), width=30)
    entrada_busca.pack(side="left", padx=5)
    entrada_busca.insert(0, "Digite para buscar...")

    def limpar_placeholder(e):
        if entrada_busca.get() == "Digite para buscar...":
            entrada_busca.delete(0, tk.END)
    entrada_busca.bind("<FocusIn>", limpar_placeholder)

    # ==========================
    # Funções de CRUD
    # ==========================
    colunas = ["ID", "Nº OS", "Nome", "Telefone", "CPF", "Endereço"]

    def atualizar_tabela(filtro_campo=None, filtro_valor=""):
        for i in tabela.get_children():
            tabela.delete(i)
        dados = listar_clientes()
        if filtro_campo and filtro_valor.strip() != "":
            idx = colunas.index(filtro_campo)
            dados = [d for d in dados if filtro_valor.lower() in str(d[idx]).lower()]
        for i, item in enumerate(dados):
            tabela.insert("", "end", values=(item[0], item[2], item[1], item[3], item[4], item[5]),
                          tags=('par' if i % 2 == 0 else 'impar',))
        tabela.tag_configure('par', background="#2A2A3F")
        tabela.tag_configure('impar', background="#33334A")

    def excluir_cliente():
        sel = tabela.selection()
        if not sel:
            messagebox.showwarning("Aviso", "Selecione um registro na tabela.", parent=janela)
            return
        _id = tabela.item(sel[0], "values")[0]
        if messagebox.askyesno("Confirmação", "Deseja excluir este cliente?", parent=janela):
            excluir_cliente_db(_id)
            atualizar_tabela()

    # ==========================
    # Função abrir formulário
    # ==========================
    def abrir_formulario(modo="cadastrar", cliente=None):
        form = tk.Toplevel(janela)
        form.title("Cadastro de Cliente" if modo == "cadastrar" else "Editar Cliente")
        form.geometry("500x400")
        form.configure(bg="#1E1E2E")

        campos = ["Nº OS", "Nome", "Telefone", "CPF", "Endereço"]
        vars_campos = {c: tk.StringVar() for c in campos}

        if cliente:
            mapa = dict(zip(colunas, cliente))
            for c in campos:
                vars_campos[c].set(mapa[c])

        for c in campos:
            tk.Label(form, text=c+":", fg="#FFFFFF", bg="#1E1E2E", font=("Helvetica", 11)).pack(anchor="w", padx=10, pady=5)
            tk.Entry(form, textvariable=vars_campos[c], font=("Helvetica", 11), width=40).pack(padx=10, pady=2)

        def salvar():
            dados = [vars_campos[c].get().strip() for c in campos]
            if not all(dados):
                messagebox.showwarning("Aviso", "Preencha todos os campos!", parent=form)
                return
            if modo == "cadastrar":
                adicionar_cliente(dados[1], dados[0], dados[2], dados[3], dados[4], "", "", "")
            else:
                _id = cliente[0]
                atualizar_cliente_db(_id, dados[1], dados[0], dados[2], dados[3], dados[4], "", "", "")
            atualizar_tabela()
            form.destroy()

        btn_salvar = tk.Button(form, text="Salvar", fg="#FFFFFF", bg="#FF6F61",
                               font=("Helvetica", 11, "bold"), relief="flat", bd=0, width=15, height=2,
                               command=salvar)
        btn_salvar.pack(pady=20)
        hover_color(btn_salvar, "#FF4B3E", "#FF6F61")

    # ==========================
    # Associar botões
    # ==========================
    btn_cadastrar.config(command=lambda: abrir_formulario("cadastrar"))
    btn_editar.config(command=lambda: (
        abrir_formulario("editar", tabela.item(tabela.selection()[0], "values"))
        if tabela.selection() else messagebox.showwarning("Aviso", "Selecione um cliente!", parent=janela)
    ))
    btn_excluir.config(command=excluir_cliente)

    # ==========================
    # Filtrar enquanto digita
    # ==========================
    var_busca.trace_add("write", lambda *args: atualizar_tabela(var_filtro.get(), var_busca.get()))
    combo_filtro.bind("<<ComboboxSelected>>", lambda e: atualizar_tabela(var_filtro.get(), var_busca.get()))

    # ==========================
    # Tabela
    # ==========================
    tabela = ttk.Treeview(janela, columns=colunas, show="headings", height=12)
    for col in colunas:
        tabela.heading(col, text=col)
    larguras = [60, 100, 200, 120, 120, 280]
    for col, w in zip(colunas, larguras):
        tabela.column(col, width=w, anchor="center")

    vsb = ttk.Scrollbar(janela, orient="vertical", command=tabela.yview)
    tabela.configure(yscroll=vsb.set)

    tabela.pack(fill="both", expand=True, padx=(12,0), pady=(0,12), side="left")
    vsb.pack(fill="y", pady=(0,12), side="left")

    atualizar_tabela()

# ==============================
# Nova Venda (placeholder)
# ==============================
def abrir_venda():
    janela = tk.Toplevel()
    janela.title("Nova Venda")
    janela.geometry("500x300")
    janela.configure(bg=BG_DARK)
    tk.Label(janela, text="🛒 Aqui será a tela de vendas",
             font=("Helvetica", 12), fg=FG, bg=BG_DARK).pack(pady=20)

# ==============================
# Painel de Controle
# ==============================
def main():
    inicializar_banco()
    root = tk.Tk()
    root.title("Painel de Controle")
    root.geometry("700x420")
    root.configure(bg=BG_DARK)

    tk.Label(root, text="Painel de Controle", font=("Helvetica", 18, "bold"),
             fg=FG, bg=BG_DARK).pack(pady=20)

    frame_icones = tk.Frame(root, bg=BG_DARK)
    frame_icones.pack(pady=20)

    def botao_menu(parent, texto, cmd):
        return tk.Button(parent, text=texto, command=cmd, fg=FG, bg=BTN,
                         activebackground=BTN_ACTIVE, font=("Helvetica", 12, "bold"),
                         relief="flat", bd=0, width=25, height=4)

    btn1 = botao_menu(frame_icones, "📐 Calculadora de Medidas", abrir_calculadora)
    btn1.grid(row=0, column=0, padx=15, pady=15)

    btn2 = botao_menu(frame_icones, "👥 Banco de Clientes", abrir_banco_clientes)
    btn2.grid(row=0, column=1, padx=15, pady=15)

    btn3 = botao_menu(frame_icones, "🛒 Nova Venda", abrir_venda)
    btn3.grid(row=1, column=0, padx=15, pady=15)

    root.mainloop()

if __name__ == "__main__":
    main()
