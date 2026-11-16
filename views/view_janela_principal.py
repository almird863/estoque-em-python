import customtkinter as ctk

# Ajuste o caminho conforme o nome real do seu arquivo de controllers
from controller.controller_estoque import (cadastrar_produto,
                                            somar_qnt_produto,
                                            subtrair_qnt_produto,
                                            deletar_produto)

from models.model_estoque import listar_items

ctk.set_appearance_mode("system")
ctk.set_default_color_theme("blue")


# ======================================================================
# TAMANHOS — altere aqui para aumentar/diminuir a interface inteira
# ======================================================================
JANELA_LARGURA = 820
JANELA_ALTURA = 820

FONTE_TITULO = 34
FONTE_ABA = 20
FONTE_ROTULO = 20
FONTE_CAMPO = 22
FONTE_BOTAO = 22
FONTE_LISTA = 22
FONTE_STATUS = 18
FONTE_DICA = 15

ALTURA_CAMPO = 56
ALTURA_BOTAO = 64
ALTURA_BOTAO_PEQUENO = 48

COR_OK = "#2e9e4f"
COR_OK_HOVER = "#237a3d"
COR_ERRO = "#d64545"
COR_ERRO_HOVER = "#a93232"
COR_ALERTA = "#d98a1f"
COR_ALERTA_HOVER = "#b0700f"
COR_INFO = "#888888"


class JanelaPrincipal(ctk.CTk):

    def __init__(self):
        super().__init__()
        self.title("Controle de Estoque")
        self.geometry(f"{JANELA_LARGURA}x{JANELA_ALTURA}")
        self.minsize(700, 720)

        self._criar_fontes()
        self._montar_janela()
        self.atualizar_lista()

    # ------------------------------------------------------------------
    # Fábricas de widgets (evitam repetição e mantêm o padrão de tamanho)
    # ------------------------------------------------------------------
    def _criar_fontes(self):
        self.f_titulo = ctk.CTkFont(size=FONTE_TITULO, weight="bold")
        self.f_aba = ctk.CTkFont(size=FONTE_ABA, weight="bold")
        self.f_rotulo = ctk.CTkFont(size=FONTE_ROTULO)
        self.f_campo = ctk.CTkFont(size=FONTE_CAMPO)
        self.f_botao = ctk.CTkFont(size=FONTE_BOTAO, weight="bold")
        self.f_lista = ctk.CTkFont(size=FONTE_LISTA)
        self.f_lista_neg = ctk.CTkFont(size=FONTE_LISTA, weight="bold")
        self.f_status = ctk.CTkFont(size=FONTE_STATUS)
        self.f_dica = ctk.CTkFont(size=FONTE_DICA)

    def _rotulo(self, parent, texto):
        return ctk.CTkLabel(parent, text=texto, font=self.f_rotulo, anchor="w")

    def _campo(self, parent, placeholder=""):
        return ctk.CTkEntry(parent, placeholder_text=placeholder,
                            font=self.f_campo, height=ALTURA_CAMPO)

    def _botao(self, parent, texto, comando, cor=None, hover=None,
               altura=ALTURA_BOTAO, **extra):
        opcoes = dict(text=texto, command=comando, font=self.f_botao,
                      height=altura, corner_radius=10)
        if cor:
            opcoes["fg_color"] = cor
        if hover:
            opcoes["hover_color"] = hover
        opcoes.update(extra)
        return ctk.CTkButton(parent, **opcoes)

    # ------------------------------------------------------------------
    # Janela e abas
    # ------------------------------------------------------------------
    def _montar_janela(self):
        ctk.CTkLabel(self, text="Controle de Estoque",
                     font=self.f_titulo).pack(pady=(22, 10))

        self.tabs = ctk.CTkTabview(self)
        self.tabs.pack(fill="both", expand=True, padx=20, pady=(0, 8))
        self.tabs.add("Estoque")
        self.tabs.add("Cadastro")
        self.tabs.add("Movimentação")

        # Abas (botões de navegação) maiores
        try:
            self.tabs._segmented_button.configure(font=self.f_aba, height=48)
        except AttributeError:
            pass

        self._montar_aba_estoque(self.tabs.tab("Estoque"))
        self._montar_aba_cadastro(self.tabs.tab("Cadastro"))
        self._montar_aba_movimentacao(self.tabs.tab("Movimentação"))

        self.lbl_status = ctk.CTkLabel(
            self, text="", font=self.f_status,
            wraplength=JANELA_LARGURA - 80, text_color=COR_INFO)
        self.lbl_status.pack(pady=(0, 18), padx=20)

    def _montar_aba_estoque(self, aba):
        aba.grid_columnconfigure(0, weight=1)
        aba.grid_rowconfigure(1, weight=1)

        topo = ctk.CTkFrame(aba, fg_color="transparent")
        topo.grid(row=0, column=0, sticky="ew", padx=6, pady=(8, 8))
        topo.grid_columnconfigure(0, weight=1)

        self.lbl_total = ctk.CTkLabel(topo, text="", font=self.f_rotulo,
                                      anchor="w", text_color=COR_INFO)
        self.lbl_total.grid(row=0, column=0, sticky="w")

        self._botao(topo, "⟳  Atualizar", self.atualizar_lista,
                    altura=ALTURA_BOTAO_PEQUENO, width=170
                    ).grid(row=0, column=1)

        self.frame_lista = ctk.CTkScrollableFrame(aba)
        self.frame_lista.grid(row=1, column=0, sticky="nsew", padx=6, pady=(0, 8))
        self.frame_lista.grid_columnconfigure(1, weight=1)

        ctk.CTkLabel(
            aba, text="Dica: clique em um produto para movimentá-lo.",
            text_color=COR_INFO, font=self.f_dica
        ).grid(row=2, column=0, pady=(0, 6))

    def _montar_aba_cadastro(self, aba):
        aba.grid_columnconfigure(0, weight=1)

        self._rotulo(aba, "Nome do produto").grid(
            row=0, column=0, sticky="w", padx=14, pady=(20, 4))
        self.ent_cad_nome = self._campo(aba, "Nome do produto")
        self.ent_cad_nome.grid(row=1, column=0, sticky="ew", padx=14)

        self._rotulo(aba, "Quantidade inicial").grid(
            row=2, column=0, sticky="w", padx=14, pady=(18, 4))
        self.ent_cad_qtd = self._campo(aba, "Ex.: 10")
        self.ent_cad_qtd.grid(row=3, column=0, sticky="ew", padx=14)

        self._botao(aba, "Cadastrar produto", self.cadastrar).grid(
            row=4, column=0, sticky="ew", padx=14, pady=(30, 10))

        self._botao(
            aba, "Limpar campos", self._limpar_cadastro,
            altura=ALTURA_BOTAO_PEQUENO, fg_color="transparent",
            border_width=2, text_color=("gray10", "gray90")
        ).grid(row=5, column=0, sticky="ew", padx=14)

    def _montar_aba_movimentacao(self, aba):
        aba.grid_columnconfigure((0, 1), weight=1)

        self._rotulo(aba, "Nome do produto").grid(
            row=0, column=0, columnspan=2, sticky="w", padx=14, pady=(20, 4))
        self.ent_mov_nome = self._campo(aba, "Nome do produto")
        self.ent_mov_nome.grid(row=1, column=0, columnspan=2,
                               sticky="ew", padx=14)

        self._rotulo(aba, "Quantidade a movimentar").grid(
            row=2, column=0, columnspan=2, sticky="w", padx=14, pady=(18, 4))
        self.ent_mov_qtd = self._campo(aba, "Ex.: 5")
        self.ent_mov_qtd.grid(row=3, column=0, columnspan=2,
                              sticky="ew", padx=14)

        self._botao(aba, "➕  Adicionar", self.adicionar,
                    COR_OK, COR_OK_HOVER).grid(
            row=4, column=0, sticky="ew", padx=(14, 7), pady=(30, 10))
        self._botao(aba, "➖  Subtrair", self.subtrair,
                    COR_ALERTA, COR_ALERTA_HOVER).grid(
            row=4, column=1, sticky="ew", padx=(7, 14), pady=(30, 10))

        self._botao(aba, "🗑  Excluir produto", self.excluir,
                    COR_ERRO, COR_ERRO_HOVER,
                    altura=ALTURA_BOTAO_PEQUENO).grid(
            row=5, column=0, columnspan=2, sticky="ew", padx=14)

    # ------------------------------------------------------------------
    # Lista de produtos
    # ------------------------------------------------------------------
    def atualizar_lista(self):
        """Busca os produtos no controller e redesenha a lista."""
        sucesso, dados = listar_items()

        for widget in self.frame_lista.winfo_children():
            widget.destroy()

        if not sucesso:
            self.lbl_total.configure(text="")
            return self._status(False, dados)

        # Cabeçalho
        for col, (texto, anchor) in enumerate(
                [("ID", "w"), ("Produto", "w"), ("Qtd.", "e")]):
            ctk.CTkLabel(self.frame_lista, text=texto, font=self.f_lista_neg,
                         anchor=anchor).grid(
                row=0, column=col, sticky="ew", padx=14, pady=(4, 10))

        if not dados:
            self.lbl_total.configure(text="Nenhum produto")
            ctk.CTkLabel(self.frame_lista, text="Nenhum produto cadastrado.",
                         font=self.f_lista, text_color=COR_INFO).grid(
                row=1, column=0, columnspan=3, pady=30)
            return

        self.lbl_total.configure(text=f"{len(dados)} produto(s)")

        for linha, item in enumerate(dados, start=1):
            item_id, nome, qnt = item[:3]
            cor_qtd = COR_ERRO if qnt == 0 else None

            celulas = [
                ctk.CTkLabel(self.frame_lista, text=str(item_id),
                             font=self.f_lista, anchor="w"),
                ctk.CTkLabel(self.frame_lista, text=str(nome).title(),
                             font=self.f_lista, anchor="w"),
                ctk.CTkLabel(self.frame_lista, text=str(qnt),
                             font=self.f_lista_neg, anchor="e",
                             text_color=cor_qtd),
            ]
            for col, celula in enumerate(celulas):
                celula.grid(row=linha, column=col, sticky="ew",
                            padx=14, pady=8)
                celula.configure(cursor="hand2")
                celula.bind("<Button-1>",
                            lambda e, n=nome: self._selecionar_produto(n))

    def _selecionar_produto(self, nome):
        """Leva o produto clicado para a aba de movimentação."""
        self.ent_mov_nome.delete(0, "end")
        self.ent_mov_nome.insert(0, str(nome).title())
        self.tabs.set("Movimentação")
        self.ent_mov_qtd.focus()

    # ------------------------------------------------------------------
    # Utilidades
    # ------------------------------------------------------------------
    def _status(self, sucesso, mensagem):
        self.lbl_status.configure(
            text=str(mensagem),
            text_color=COR_OK if sucesso else COR_ERRO)

    def _limpar_cadastro(self):
        self.ent_cad_nome.delete(0, "end")
        self.ent_cad_qtd.delete(0, "end")

    def _limpar_movimentacao(self, limpar_nome=False):
        self.ent_mov_qtd.delete(0, "end")
        if limpar_nome:
            self.ent_mov_nome.delete(0, "end")

    def _confirmar(self, texto):
        """Diálogo modal de confirmação (Sim/Não)."""
        resposta = {"ok": False}

        dialogo = ctk.CTkToplevel(self)
        dialogo.title("Confirmar")
        dialogo.geometry("520x240")
        dialogo.resizable(False, False)
        dialogo.transient(self)
        dialogo.after(100, dialogo.grab_set)

        ctk.CTkLabel(dialogo, text=texto, font=self.f_rotulo,
                     wraplength=460).pack(pady=(34, 24), padx=24)

        botoes = ctk.CTkFrame(dialogo, fg_color="transparent")
        botoes.pack(fill="x", padx=24)
        botoes.grid_columnconfigure((0, 1), weight=1)

        def responder(valor):
            resposta["ok"] = valor
            dialogo.destroy()

        self._botao(botoes, "Sim", lambda: responder(True),
                    COR_ERRO, COR_ERRO_HOVER).grid(
            row=0, column=0, sticky="ew", padx=(0, 8))
        self._botao(botoes, "Não", lambda: responder(False)).grid(
            row=0, column=1, sticky="ew", padx=(8, 0))

        self.wait_window(dialogo)
        return resposta["ok"]

    # ------------------------------------------------------------------
    # Ações (a validação fica nos controllers; a view só repassa e exibe)
    # ------------------------------------------------------------------
    def cadastrar(self):
        sucesso, msg = cadastrar_produto(
            self.ent_cad_nome.get(), self.ent_cad_qtd.get())
        self._status(sucesso, msg)
        if sucesso:
            self._limpar_cadastro()
            self.atualizar_lista()

    def adicionar(self):
        sucesso, msg = somar_qnt_produto(
            self.ent_mov_nome.get(), self.ent_mov_qtd.get())
        self._status(sucesso, msg)
        if sucesso:
            self._limpar_movimentacao()
            self.atualizar_lista()

    def subtrair(self):
        sucesso, msg = subtrair_qnt_produto(
            self.ent_mov_nome.get(), self.ent_mov_qtd.get())
        self._status(sucesso, msg)
        if sucesso:
            self._limpar_movimentacao()
            self.atualizar_lista()

    def excluir(self):
        nome = self.ent_mov_nome.get().strip()
        if not nome:
            return self._status(False, "Nome precisa ser válido")

        if not self._confirmar(f"Excluir definitivamente o produto '{nome}'?"):
            return

        sucesso, msg = deletar_produto(nome)
        self._status(sucesso, msg)
        if sucesso:
            self._limpar_movimentacao(limpar_nome=True)
            self.atualizar_lista()


if __name__ == "__main__":
    app = JanelaPrincipal()
    app.mainloop()