import tkinter as tk
from tkinter import ttk
from tkinter import messagebox

def calcular_preco():
    try:
        altura = float(entrada_altura.get()) 
        largura = float(entrada_largura.get()) 
        if altura <= 0 or largura <= 0:
            raise ValueError("Altura e largura devem ser valores positivos.")

        area = (altura * largura) / 10000
        preco = area * 329

        comodo = combo_comodo.get()
        if comodo in valores_comodos:
            valores_comodos[comodo]["altura"] = altura
            valores_comodos[comodo]["largura"] = largura
            valores_comodos[comodo]["area"] = area
            valores_comodos[comodo]["preco"] = preco
        else:
            valores_comodos[comodo] = {
                "altura": altura,
                "largura": largura,
                "area": area,
                "preco": preco
            }

        atualizar_lista_comodos()
        calcular_total()

    except ValueError as e:
        messagebox.showerror("Erro", f"Erro ao calcular preço: {str(e)}")

def atualizar_lista_comodos():
    lista_comodos.delete(0, tk.END)
    for comodo, valores in valores_comodos.items():
        texto = f"{comodo}: R$ {valores['preco']:.2f}"
        lista_comodos.insert(tk.END, texto)

def calcular_total():
    total = sum(valores['preco'] for valores in valores_comodos.values())
    total_com_desconto = total * 0.95
    parcela = total / 3

    label_total.config(text=f"Total: R$ {total:.2f}")
    label_total_com_desconto.config(text=f"Total à vista: R$ {total_com_desconto:.2f}")
    label_parcela.config(text=f"3x sem juros: R$ {parcela:.2f}")

def copiar_texto():
    try:
        texto_selecionado = lista_comodos.get(lista_comodos.curselection())
        janela.clipboard_clear()
        janela.clipboard_append(texto_selecionado)
        janela.update()
        messagebox.showinfo("Sucesso", "Cômodo copiado para área de transferência!")
    except:
        messagebox.showwarning("Aviso", "Selecione um cômodo para copiar.")

def copiar_valores_totais():
    valores_totais = (
        label_total.cget("text") + "\n" +
        label_total_com_desconto.cget("text") + "\n" +
        label_parcela.cget("text")
    )
    janela.clipboard_clear()
    janela.clipboard_append(valores_totais)
    janela.update()
    messagebox.showinfo("Sucesso", "Valores totais copiados para área de transferência!")

def reiniciar_orcamento():
    entrada_altura.delete(0, tk.END)
    entrada_largura.delete(0, tk.END)
    valores_comodos.clear()
    lista_comodos.delete(0, tk.END)
    label_total.config(text="Total: R$ 0.00")
    label_total_com_desconto.config(text="Total à vista: R$ 0.00")
    label_parcela.config(text="3x sem juros: R$ 0.00")
    combo_comodo.set(opcoes_comodos[0])

def excluir_comodo():
    try:
        comodo_selecionado = lista_comodos.get(lista_comodos.curselection()).split(":")[0]
        
        if comodo_selecionado in valores_comodos:
            del valores_comodos[comodo_selecionado]
            atualizar_lista_comodos()
            calcular_total()
            messagebox.showinfo("Sucesso", f"{comodo_selecionado} excluído com sucesso!")
        else:
            messagebox.showwarning("Aviso", "Nenhum cômodo selecionado para excluir!")
    except:
        messagebox.showwarning("Aviso", "Selecione um cômodo para excluir.")

# Função para copiar todos os cômodos e valores totais
def copiar_todos_comodos():
    todos_comodos = ""
    for comodo, valores in valores_comodos.items():
        todos_comodos += f"{comodo}: R$ {valores['preco']:.2f}\n"
    
    valores_totais = (
        "\nTotal: " + label_total.cget("text") + "\n" +
        label_total_com_desconto.cget("text") + "\n" +
        label_parcela.cget("text")
    )
    
    texto_completo = todos_comodos + valores_totais
    janela.clipboard_clear()
    janela.clipboard_append(texto_completo)
    janela.update()
    messagebox.showinfo("Sucesso", "Todos os cômodos e valores copiados para a área de transferência!")

# Criando a interface gráfica
janela = tk.Tk()
janela.title("Orçamento de Tela Mosquiteira")
janela.geometry("600x900")  # Ajustei o tamanho da janela
janela.configure(bg="#2E2E2E")

# Função para criar botões arredondados
def criar_botao(janela, texto, comando):
    return tk.Button(janela, text=texto, command=comando, fg="white", bg="#FF5733", font=("Helvetica", 12, "bold"), relief="flat", bd=0, width=20, height=2, activebackground="#FF4515")

# Título da aplicação
tk.Label(janela, text="Orçamento telas mosquiteiras", fg="white", bg="#2E2E2E", font=("Helvetica", 16, "bold")).pack(pady=20)

# Entrada de dados
tk.Label(janela, text="Cômodo:", fg="white", bg="#2E2E2E", font=("Helvetica", 10)).pack(pady=5)
opcoes_comodos = ["Quarto casal", "Quarto filho", "Quarto filha", "Banheiro social", 
           "Banheiro suíte", "Banheiro suíte filho", "Banheiro suíte filha", 
           "Lavabo", "Sala", "Cozinha", "Área técnica", "Sacada", "Vão"]
combo_comodo = ttk.Combobox(janela, values=opcoes_comodos, state="readonly", font=("Helvetica", 10))
combo_comodo.current(0)
combo_comodo.pack(pady=5)

tk.Label(janela, text="Altura (cm):", fg="white", bg="#2E2E2E", font=("Helvetica", 10)).pack(pady=5)
entrada_altura = tk.Entry(janela, font=("Helvetica", 10), relief="flat", bd=0, justify="center", width=20)
entrada_altura.pack(pady=5)

tk.Label(janela, text="Largura (cm):", fg="white", bg="#2E2E2E", font=("Helvetica", 10)).pack(pady=5)
entrada_largura = tk.Entry(janela, font=("Helvetica", 10), relief="flat", bd=0, justify="center", width=20)
entrada_largura.pack(pady=5)

# Botão de calcular
criar_botao(janela, "Calcular Preço", calcular_preco).pack(pady=10)

# Lista de cômodos
lista_comodos = tk.Listbox(janela, width=60, height=10, font=("Helvetica", 10), bg="#555555", fg="white", selectmode=tk.SINGLE, bd=0, relief="flat")
lista_comodos.pack(pady=10)

# Frame para botões "Copiar" e "Excluir"
frame_botoes = tk.Frame(janela, bg="#2E2E2E")
frame_botoes.pack(pady=10)

criar_botao(frame_botoes, "Copiar Cômodo", copiar_texto).pack(side=tk.LEFT, padx=5)
criar_botao(frame_botoes, "Excluir Cômodo", excluir_comodo).pack(side=tk.LEFT, padx=5)

# Labels de resultado
label_total = tk.Label(janela, text="Total: R$ 0.00", font=("Helvetica", 12, "bold"), fg="white", bg="#2E2E2E")
label_total.pack(pady=5)
label_total_com_desconto = tk.Label(janela, text="Total à vista: R$ 0.00", font=("Helvetica", 12, "bold"), fg="white", bg="#2E2E2E")
label_total_com_desconto.pack(pady=5)
label_parcela = tk.Label(janela, text="3x sem juros: R$ 0.00", font=("Helvetica", 12, "bold"), fg="white", bg="#2E2E2E")
label_parcela.pack(pady=5)

# Botão para copiar todos os cômodos e valores totais
criar_botao(janela, "Copiar tudo", copiar_todos_comodos).pack(pady=5)

# Botão para reiniciar o orçamento
criar_botao(janela, "Reiniciar Orçamento", reiniciar_orcamento).pack(pady=10)

# Dicionário para armazenar os valores dos cômodos
valores_comodos = {}

janela.mainloop()
