import os
import json
from datetime import datetime
import tkinter as tk
from tkinter import messagebox, ttk

ARQUIVO_BANCO = "agendamentos.json"

SERVICOS = {
    "1": ("Degradê", 35),
    "2": ("Corte social", 30),
    "3": ("Barba completa", 25),
    "4": ("Pigmentação", 40),
    "5": ("Hidratação capilar", 50),
    "6": ("Platinado", 120),
    "7": ("Combo corte + barba", 50)
}


HORARIOS_PADRAO = ["09:00", "10:00", "11:00", "13:00", "14:00", "15:00", "16:00", "17:30"]


COR_FUNDO = "#121212"      
COR_CONTAINER = "#1E1E1E"   
COR_BOTAO = "#0056b3"     
COR_TEXTO = "#FFFFFF"     
COR_SUBTEXTO = "#A0A0A0"   

def carregar_agendamentos():
    if not os.path.exists(ARQUIVO_BANCO):
        with open(ARQUIVO_BANCO, "w", encoding="utf-8") as arquivo:
            json.dump([], arquivo)
    with open(ARQUIVO_BANCO, "r", encoding="utf-8") as arquivo:
        return json.load(arquivo)

def salvar_agendamentos(lista_agendamentos):
    with open(ARQUIVO_BANCO, "w", encoding="utf-8") as arquivo:
        json.dump(lista_agendamentos, arquivo, indent=4, ensure_ascii=False)

def obter_horarios_disponiveis(data_selecionada):
    agendamentos = carregar_agendamentos()
    horarios_ocupados = [
        a["horario"] for a in agendamentos if a["data"] == data_selecionada
    ]
    return [h for h in HORARIOS_PADRAO if h not in horarios_ocupados]


class BarbeariaApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Barbearia Andrades")
        self.root.geometry("650x550")
        self.root.configure(bg=COR_FUNDO)
      
        style = ttk.Style()
        style.theme_use('clam')
        style.configure("TCombobox", fieldbackground=COR_CONTAINER, background=COR_BOTAO, foreground=COR_TEXTO)

        self.mostrar_menu_principal()

    def limpar_tela(self):
        for widget in self.root.winfo_children():
            widget.destroy()

    def criar_cabecalho(self, titulo):
        header = tk.Frame(self.root, bg=COR_FUNDO, pady=10)
        header.pack(fill="x")
        
        lbl_titulo = tk.Label(header, text=f"Barbearia Andrades - {titulo}", font=("Helvetica", 16, "bold"), fg=COR_BOTAO, bg=COR_FUNDO)
        lbl_titulo.pack()
        
        linha = tk.Frame(self.root, height=2, bg=COR_CONTAINER)
        linha.pack(fill="x", padx=20, pady=5)

    def criar_botao_voltar(self):
        btn_voltar = tk.Button(self.root, text="Voltar ao Menu", font=("Helvetica", 10, "bold"), bg=COR_CONTAINER, fg=COR_TEXTO, activebackground=COR_BOTAO, activeforeground=COR_TEXTO, bd=0, padx=15, pady=8, command=self.mostrar_menu_principal)
        btn_voltar.pack(side="bottom", pady=20)

    def mostrar_menu_principal(self):
        self.limpar_tela()
        
        # Título Principal
        lbl_welcome = tk.Label(self.root, text="Barbearia Andrades", font=("Helvetica", 22, "bold"), fg=COR_TEXTO, bg=COR_FUNDO, pady=20)
        lbl_welcome.pack()
        
        lbl_sub = tk.Label(self.root, text="Seja Bem-Vindo! Escolha uma opção:", font=("Helvetica", 11), fg=COR_SUBTEXTO, bg=COR_FUNDO)
        lbl_sub.pack(pady=5)

        # Container dos botões
        menu_frame = tk.Frame(self.root, bg=COR_CONTAINER, bd=1, relief="flat", padx=30, pady=20)
        menu_frame.pack(pady=20)

        botoes = [
            ("1 - Agendar Horário", self.tela_agendar),
            ("2 - Cancelar Agendamento", self.tela_cancelar),
            ("3 - Ver Agendamentos", self.tela_listar),
            ("4 - Serviços e Preços", self.tela_servicos),
            ("5 - Localização e Contato", self.tela_contato),
        ]

        for texto, comando in botoes:
            btn = tk.Button(menu_frame, text=texto, font=("Helvetica", 11, "bold"), bg=COR_FUNDO, fg=COR_TEXTO, activebackground=COR_BOTAO, activeforeground=COR_TEXTO, bd=0, width=25, height=2, cursor="hand2", command=comando)
            btn.pack(pady=8)
            
        btn_sair = tk.Button(self.root, text="Sair", font=("Helvetica", 10, "bold"), bg="#8b0000", fg=COR_TEXTO, bd=0, width=10, pady=5, command=self.root.quit)
        btn_sair.pack(side="bottom", pady=20)

    def tela_agendar(self):
        self.limpar_tela()
        self.criar_cabecalho("Agendamento")

        form_frame = tk.Frame(self.root, bg=COR_CONTAINER, padx=20, pady=20)
        form_frame.pack(pady=10, fill="both", expand=True, padx=40)

      
        tk.Label(form_frame, text="Nome do Cliente:", font=("Helvetica", 10, "bold"), fg=COR_TEXTO, bg=COR_CONTAINER).grid(row=0, column=0, sticky="w", pady=5)
        ent_nome = tk.Entry(form_frame, font=("Helvetica", 11), bg=COR_FUNDO, fg=COR_TEXTO, insertbackground=COR_TEXTO, bd=1, relief="solid")
        ent_nome.grid(row=0, column=1, sticky="ew", pady=5, padx=10)

       
        tk.Label(form_frame, text="Serviço desejado:", font=("Helvetica", 10, "bold"), fg=COR_TEXTO, bg=COR_CONTAINER).grid(row=1, column=0, sticky="w", pady=5)
        
        lista_servicos_texto = [f"{nome} (R$ {preco})" for cod, (nome, preco) in SERVICOS.items()]
        cb_servico = ttk.Combobox(form_frame, values=lista_servicos_texto, state="readonly", font=("Helvetica", 10))
        cb_servico.grid(row=1, column=1, sticky="ew", pady=5, padx=10)
        cb_servico.current(0)

        # Campo Data
        tk.Label(form_frame, text="Data (DD/MM/AAAA):", font=("Helvetica", 10, "bold"), fg=COR_TEXTO, bg=COR_CONTAINER).grid(row=2, column=0, sticky="w", pady=5)
        ent_data = tk.Entry(form_frame, font=("Helvetica", 11), bg=COR_FUNDO, fg=COR_TEXTO, insertbackground=COR_TEXTO, bd=1, relief="solid")
        ent_data.insert(0, datetime.now().strftime("%d/%m/%Y"))
        ent_data.grid(row=2, column=1, sticky="ew", pady=5, padx=10)

     
        tk.Label(form_frame, text="Horário:", font=("Helvetica", 10, "bold"), fg=COR_TEXTO, bg=COR_CONTAINER).grid(row=3, column=0, sticky="w", pady=5)
        cb_horario = ttk.Combobox(form_frame, state="readonly", font=("Helvetica", 10))
        cb_horario.grid(row=3, column=1, sticky="ew", pady=5, padx=10)

        def atualizar_horarios(*args):
            data_str = ent_data.get().strip()
            try:
                data_validada = datetime.strptime(data_str, "%d/%m/%Y")
                if data_validada.date() >= datetime.now().date():
                    vagos = obter_horarios_disponiveis(data_str)
                    cb_horario['values'] = vagos
                    if vagos:
                        cb_horario.current(0)
                    else:
                        cb_horario['values'] = ["Nenhum horário vago"]
                        cb_horario.current(0)
                else:
                    cb_horario['values'] = ["Data retroativa"]
                    cb_horario.current(0)
            except ValueError:
                cb_horario['values'] = ["Aguardando data válida..."]
                cb_horario.current(0)

        ent_data.bind("<KeyRelease>", atualizar_horarios)
        atualizar_horarios()

        form_frame.columnconfigure(1, weight=1)

        def confirmar_agendamento():
            nome = ent_nome.get().strip()
            servico_escolhido = cb_servico.get()
            data_str = ent_data.get().strip()
            horario = cb_horario.get()

            if not nome:
                messagebox.showerror("Erro", "Por favor, digite seu nome.")
                return

            try:
                data_validada = datetime.strptime(data_str, "%d/%m/%Y")
                if data_validada.date() < datetime.now().date():
                    messagebox.showerror("Erro", "Não é possível agendar em datas passadas.")
                    return
            except ValueError:
                messagebox.showerror("Erro", "Formato de data inválido. Use DD/MM/AAAA.")
                return

            if horario in ["Nenhum horário vago", "Data retroativa", "Aguardando data válida...", ""]:
                messagebox.showerror("Erro", "Por favor, selecione um horário válido.")
                return

            nome_servico = servico_escolhido.split(" (")[0]

            novo_agendamento = {
                "nome": nome,
                "servico": nome_servico,
                "data": data_str,
                "horario": horario
            }

            lista = carregar_agendamentos()
            lista.append(novo_agendamento)
            salvar_agendamentos(lista)

            messagebox.showinfo("Sucesso", f"Agendamento confirmado para {nome} às {horario}!")
            self.mostrar_menu_principal()

        btn_confirmar = tk.Button(form_frame, text="Confirmar Agendamento", font=("Helvetica", 11, "bold"), bg=COR_BOTAO, fg=COR_TEXTO, bd=0, padding=10, cursor="hand2", command=confirmar_agendamento)
        btn_confirmar.grid(row=4, column=0, columnspan=2, pady=20)

        self.criar_botao_voltar()

    def tela_cancelar(self):
        self.limpar_tela()
        self.criar_cabecalho("Cancelar Agendamento")

        cancel_frame = tk.Frame(self.root, bg=COR_CONTAINER, padx=20, pady=20)
        cancel_frame.pack(pady=20, padx=40, fill="x")

        tk.Label(cancel_frame, text="Digite o Nome cadastrado para cancelar:", font=("Helvetica", 11, "bold"), fg=COR_TEXTO, bg=COR_CONTAINER).pack(pady=5)
        ent_nome = tk.Entry(cancel_frame, font=("Helvetica", 12), bg=COR_FUNDO, fg=COR_TEXTO, insertbackground=COR_TEXTO, bd=1, relief="solid")
        ent_nome.pack(pady=5, fill="x", padx=20)

        def acao_cancelar():
            nome = ent_nome.get().strip()
            if not nome:
                messagebox.showerror("Erro", "Digite um nome para buscar.")
                return

            lista = carregar_agendamentos()
            novo_banco = [a for a in lista if a["nome"].lower() != nome.lower()]

            if len(lista) == len(novo_banco):
                messagebox.showwarning("Aviso", "Nenhum agendamento encontrado com esse nome.")
            else:
                salvar_agendamentos(novo_banco)
                messagebox.showinfo("Sucesso", "Agendamento(s) cancelado(s) com sucesso!")
                self.mostrar_menu_principal()

        btn_cancelar = tk.Button(cancel_frame, text="Remover Agendamento", font=("Helvetica", 11, "bold"), bg="#8b0000", fg=COR_TEXTO, bd=0, pady=8, cursor="hand2", command=acao_cancelar)
        btn_cancelar.pack(pady=15)

        self.criar_botao_voltar()

    def tela_listar(self):
        self.limpar_tela()
        self.criar_cabecalho("Lista de Agendamentos")

    
        canvas = tk.Canvas(self.root, bg=COR_FUNDO, highlightthickness=0)
        scrollbar = tk.Scrollbar(self.root, orient="vertical", command=canvas.yview)
        scroll_frame = tk.Frame(canvas, bg=COR_FUNDO)

        scroll_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        canvas.create_window((0, 0), window=scroll_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)

        canvas.pack(side="left", fill="both", expand=True, padx=20)
        scrollbar.pack(side="right", fill="y")

        lista = carregar_agendamentos()

        if not lista:
            lbl_vazio = tk.Label(scroll_frame, text="Nenhum agendamento encontrado.", font=("Helvetica", 12, "italic"), fg=COR_SUBTEXTO, bg=COR_FUNDO)
            lbl_vazio.pack(pady=50, padx=150)
        else:
            for agendamento in lista:
                card = tk.Frame(scroll_frame, bg=COR_CONTAINER, padx=15, pady=10, bd=1, relief="solid")
                card.pack(fill="x", pady=5, padx=10)
                
                texto_card = f"Nome: {agendamento['nome']}\nServiço: {agendamento['servico']}\nData: {agendamento['data']} às {agendamento['horario']}"
                lbl_info = tk.Label(card, text=texto_card, font=("Helvetica", 10), justify="left", fg=COR_TEXTO, bg=COR_CONTAINER)
                lbl_info.pack(anchor="w")

        self.criar_botao_voltar()

    def tela_servicos(self):
        self.limpar_tela()
        self.criar_cabecalho("Nossos Serviços e Preços")

        tabela_frame = tk.Frame(self.root, bg=COR_CONTAINER, padx=20, pady=20)
        tabela_frame.pack(pady=20, padx=40, fill="both", expand=True)

        for cod, (nome, preco) in SERVICOS.items():
            row_frame = tk.Frame(tabela_frame, bg=COR_CONTAINER)
            row_frame.pack(fill="x", pady=4)
            
            lbl_nome = tk.Label(row_frame, text=nome, font=("Helvetica", 11, "bold"), fg=COR_TEXTO, bg=COR_CONTAINER)
            lbl_nome.pack(side="left")
            
            lbl_preco = tk.Label(row_frame, text=f"R$ {preco:.2f}", font=("Helvetica", 11), fg=COR_BOTAO, bg=COR_CONTAINER)
            lbl_preco.pack(side="right")
            
            # Linha fina divisória
            div = tk.Frame(tabela_frame, height=1, bg=COR_FUNDO)
            div.pack(fill="x", pady=2)

        self.criar_botao_voltar()

    def tela_contato(self):
        self.limpar_tela()
        self.criar_cabecalho("Contato & Localização")

        info_frame = tk.Frame(self.root, bg=COR_CONTAINER, padx=30, pady=30)
        info_frame.pack(pady=40, padx=50, fill="x")

        txt_contato = (
            "Endereço:\n"
            "Jardim Macedônia - Rua Póva de Varzim - Nº67\n\n"
            "Telefone / WhatsApp:\n"
            "+55 11 91539-7314\n\n"
            "Horário de atendimento:\n"
            "Terça a Sábado das 09:00 às 18:30"
        )

        lbl_info = tk.Label(info_frame, text=txt_contato, font=("Helvetica", 12), justify="left", fg=COR_TEXTO, bg=COR_CONTAINER, wraplength=450)
        lbl_info.pack(anchor="w")

        self.criar_botao_voltar()


if __name__ == "__main__":
    root = tk.Tk()
    app = BarbeariaApp(root)
    root.mainloop()