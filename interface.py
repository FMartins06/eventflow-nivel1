import tkinter as tk
from tkinter import messagebox, simpledialog, ttk

from modelos import (
    Evento,
    Organizador,
    Participante,
    GerenciadorUsuarios,
    EquipeDivulgacao,
)

organizador = Organizador("Ana", "ana@email.com")

evento1 = Evento(
    titulo="Festival de Música",
    descricao="Música ao vivo e praça de alimentação.",
    data_hora="20/12/2026 às 18:00",
    local="Praça Central",
    categoria="Música",
    vagas=100,
    organizador=organizador,
)
evento1.publicar()

evento2 = Evento(
    titulo="Feira de Tecnologia",
    descricao="Palestras e demonstrações de tecnologia.",
    data_hora="15/01/2027 às 10:00",
    local="Centro de Convenções",
    categoria="Tecnologia",
    vagas=50,
    organizador=organizador,
)
evento2.publicar()

eventos = [evento1, evento2]

equipes_divulgacao = [
    EquipeDivulgacao(
        "Mídia Local",
        "Postagens e divulgação regional",
        250.00,
    ),
    EquipeDivulgacao(
        "Alcance Digital",
        "Campanhas em redes sociais",
        400.00,
    ),
]

gerenciador_usuarios = GerenciadorUsuarios()
usuario_atual = None


def cadastrar_conta():
    formulario = tk.Toplevel(janela)
    formulario.title("Criar conta")
    formulario.geometry("360x390")
    formulario.transient(janela)
    formulario.grab_set()

    nome_var = tk.StringVar()
    email_var = tk.StringVar()
    senha_var = tk.StringVar()
    tipo_var = tk.StringVar(value="")

    ttk.Label(formulario, text="Nome:").pack(anchor="w", padx=20, pady=(15, 0))
    ttk.Entry(formulario, textvariable=nome_var).pack(fill="x", padx=20)

    ttk.Label(formulario, text="Email:").pack(anchor="w", padx=20, pady=(10, 0))
    ttk.Entry(formulario, textvariable=email_var).pack(fill="x", padx=20)

    ttk.Label(formulario, text="Senha:").pack(anchor="w", padx=20, pady=(10, 0))
    ttk.Entry(
        formulario,
        textvariable=senha_var,
        show="*",
    ).pack(fill="x", padx=20)

    opcoes = ttk.LabelFrame(formulario, text="Tipo de conta", padding=10)
    opcoes.pack(fill="x", padx=20, pady=15)

    ttk.Radiobutton(
        opcoes,
        text="Organizador",
        variable=tipo_var,
        value="organizador",
    ).pack(anchor="w")

    ttk.Radiobutton(
        opcoes,
        text="Participante",
        variable=tipo_var,
        value="participante",
    ).pack(anchor="w")

    def salvar_conta():
        global usuario_atual

        try:
            usuario_atual = gerenciador_usuarios.cadastrar(
                nome_var.get(),
                email_var.get(),
                senha_var.get(),
                tipo_var.get(),
            )
        except ValueError as erro:
            messagebox.showwarning(
                "Cadastro não realizado",
                str(erro),
                parent=formulario,
            )
            return

        formulario.destroy()
        atualizar_controles_sessao()
        messagebox.showinfo("Conta criada", "Cadastro realizado com sucesso.")

    ttk.Button(
        formulario,
        text="Criar conta",
        command=salvar_conta,
    ).pack(pady=5)


def entrar_conta():
    formulario = tk.Toplevel(janela)
    formulario.title("Entrar na conta")
    formulario.geometry("360x270")
    formulario.transient(janela)
    formulario.grab_set()

    email_var = tk.StringVar()
    senha_var = tk.StringVar()

    dados = ttk.LabelFrame(formulario, text="Dados de acesso", padding=15)
    dados.pack(fill="x", padx=20, pady=20)

    ttk.Label(dados, text="Email:").pack(anchor="w")
    ttk.Entry(dados, textvariable=email_var).pack(fill="x", pady=(0, 10))

    ttk.Label(dados, text="Senha:").pack(anchor="w")
    ttk.Entry(dados, textvariable=senha_var, show="*").pack(fill="x")

    def confirmar_login():
        global usuario_atual

        try:
            usuario_atual = gerenciador_usuarios.autenticar(
                email_var.get(),
                senha_var.get(),
            )
        except ValueError as erro:
            messagebox.showwarning(
                "Não foi possível entrar",
                str(erro),
                parent=formulario,
            )
            return

        formulario.destroy()
        atualizar_controles_sessao()
        messagebox.showinfo(
            "Login",
            "Entrada realizada com sucesso.",
            parent=janela,
        )

    botoes = ttk.Frame(formulario)
    botoes.pack(pady=5)

    ttk.Button(
        botoes,
        text="Entrar",
        command=confirmar_login,
    ).pack(side="left", padx=5)

    ttk.Button(
        botoes,
        text="Cancelar",
        command=formulario.destroy,
    ).pack(side="left", padx=5)

def sair_conta():
    global usuario_atual
    usuario_atual = None
    atualizar_controles_sessao()
    messagebox.showinfo("Sessão encerrada", "Você saiu da conta.")

def resumo_interesses(evento):
    confirmados = sum(
        1
        for interesse in evento.interesses
        if interesse.status == "Confirmado"
    )

    na_lista_de_espera = sum(
        1
        for interesse in evento.interesses
        if interesse.status == "Lista de espera"
    )

    return (
        f"Interessados: {len(evento.interesses)} | "
        f"Confirmados: {confirmados} | "
        f"Lista de espera: {na_lista_de_espera}"
    )

def registrar_interesse(evento, contador):
    if not isinstance(usuario_atual, Participante):
        messagebox.showwarning(
            "Acesso necessário",
            "Entre com uma conta de participante para demonstrar interesse.",
        )
        return

    try:
        interesse = evento.demonstrar_interesse(usuario_atual)
    except ValueError as erro:
        messagebox.showwarning("Não foi possível registrar", str(erro))
        return

    messagebox.showinfo(
        "Interesse registrado",
        f"Seu interesse foi: {interesse.status}",
    )

    contador.config(text=resumo_interesses(evento))

janela = tk.Tk()
janela.title("EventFlow - Gerenciamento de Eventos")
janela.geometry("700x450")

titulo = ttk.Label(
    janela,
    text="EventFlow",
    font=("Arial", 24, "bold"),
)
titulo.pack(pady=(20, 5))

subtitulo = ttk.Label(
    janela,
    text="Eventos publicados",
    font=("Arial", 14),
)
subtitulo.pack(pady=(0, 15))

painel_conta = ttk.Frame(janela)
painel_conta.pack(pady=5)

label_sessao = ttk.Label(painel_conta, text="Não conectado")
label_sessao.pack(side="left", padx=8)

botao_criar_conta = ttk.Button(
    painel_conta,
    text="Criar conta",
    command=cadastrar_conta,
)
botao_criar_conta.pack(side="left", padx=5)

botao_entrar = ttk.Button(
    painel_conta,
    text="Entrar",
    command=entrar_conta,
)
botao_entrar.pack(side="left", padx=5)

botao_sair = ttk.Button(
    painel_conta,
    text="Sair",
    command=sair_conta,
)
botao_sair.pack(side="left", padx=5)
botao_sair.pack_forget()


def atualizar_controles_sessao():
    if usuario_atual is None:
        label_sessao.config(text="Não conectado")
        botao_criar_conta.pack(side="left", padx=5)
        botao_entrar.pack(side="left", padx=5)
        botao_sair.pack_forget()
    else:
        label_sessao.config(
            text=f"Conectado: {usuario_atual.nome} "
                 f"({usuario_atual.tipo_de_perfil()})"
        )
        botao_criar_conta.pack_forget()
        botao_entrar.pack_forget()
        botao_sair.pack(side="left", padx=5)
    atualizar_lista_eventos()

lista_eventos = ttk.LabelFrame(janela, text="Eventos disponíveis", padding=12)
lista_eventos.pack(fill="both", expand=True, padx=20, pady=10)

canvas_eventos = tk.Canvas(lista_eventos, highlightthickness=0)

barra_rolagem = ttk.Scrollbar(
    lista_eventos,
    orient="vertical",
    command=canvas_eventos.yview,
)

canvas_eventos.configure(yscrollcommand=barra_rolagem.set)

barra_rolagem.pack(side="right", fill="y")
canvas_eventos.pack(side="left", fill="both", expand=True)

conteudo_eventos = ttk.Frame(canvas_eventos)

janela_eventos = canvas_eventos.create_window(
    (0, 0),
    window=conteudo_eventos,
    anchor="nw",
)


def atualizar_area_rolagem(event):
    canvas_eventos.configure(
        scrollregion=canvas_eventos.bbox("all")
    )


def ajustar_largura_conteudo(event):
    canvas_eventos.itemconfigure(
        janela_eventos,
        width=event.width,
    )


conteudo_eventos.bind("<Configure>", atualizar_area_rolagem)
canvas_eventos.bind("<Configure>", ajustar_largura_conteudo)


def rolar_com_mouse(event):
    canvas_eventos.yview_scroll(
        int(-1 * (event.delta / 120)),
        "units",
    )


canvas_eventos.bind_all("<MouseWheel>", rolar_com_mouse)

def cancelar_evento(evento):
    if (
        not isinstance(usuario_atual, Organizador)
        or evento.organizador.email.lower() != usuario_atual.email.lower()
    ):
        messagebox.showwarning(
            "Acesso negado",
            "Somente o organizador responsável pode cancelar este evento.",
        )
        return

    confirmar = messagebox.askyesno(
        "Cancelar evento",
        f"Tem certeza que deseja cancelar '{evento.titulo}'?",
    )

    if not confirmar:
        return

    try:
        evento.cancelar()
    except ValueError as erro:
        messagebox.showwarning("Não foi possível cancelar", str(erro))
        return

    atualizar_lista_eventos()
    messagebox.showinfo("Evento cancelado", f"{evento.titulo} foi cancelado.")

def editar_evento(evento, cartao):
    if (
        not isinstance(usuario_atual, Organizador)
        or evento.organizador.email.lower() != usuario_atual.email.lower()
    ):
        messagebox.showwarning(
            "Acesso negado",
            "Somente o organizador responsável pode editar este evento.",
            parent=janela,
        )
        return

    if evento.status != "Publicado":
        messagebox.showwarning(
            "Não é possível editar",
            "Somente eventos publicados podem ser editados.",
            parent=janela,
        )
        return

    formulario = tk.Toplevel(janela)
    formulario.title("Editar evento")
    formulario.geometry("420x610")
    formulario.transient(janela)
    formulario.grab_set()

    titulo_var = tk.StringVar(value=evento.titulo)
    data_hora_var = tk.StringVar(value=evento.data_hora)
    local_var = tk.StringVar(value=evento.local)
    categoria_var = tk.StringVar(value=evento.categoria)
    vagas_var = tk.StringVar(value=str(evento.vagas))

    dados = ttk.LabelFrame(formulario, text="Dados do evento", padding=15)
    dados.pack(fill="both", expand=True, padx=20, pady=15)

    ttk.Label(dados, text="Título:").pack(anchor="w")
    ttk.Entry(dados, textvariable=titulo_var).pack(fill="x", pady=(0, 8))

    ttk.Label(dados, text="Descrição:").pack(anchor="w")
    descricao_campo = tk.Text(dados, height=4, wrap="word")
    descricao_campo.pack(fill="x", pady=(0, 8))
    descricao_campo.insert("1.0", evento.descricao)

    ttk.Label(dados, text="Data e horário:").pack(anchor="w")
    ttk.Entry(dados, textvariable=data_hora_var).pack(fill="x", pady=(0, 8))

    ttk.Label(dados, text="Local:").pack(anchor="w")
    ttk.Entry(dados, textvariable=local_var).pack(fill="x", pady=(0, 8))

    ttk.Label(dados, text="Categoria:").pack(anchor="w")
    ttk.Entry(dados, textvariable=categoria_var).pack(fill="x", pady=(0, 8))

    ttk.Label(dados, text="Número de vagas:").pack(anchor="w")
    ttk.Entry(dados, textvariable=vagas_var).pack(fill="x")

    def salvar_alteracoes():
        try:
            vagas_novas = int(vagas_var.get().strip())

            evento.editar(
                titulo_var.get().strip(),
                descricao_campo.get("1.0", "end").strip(),
                data_hora_var.get().strip(),
                local_var.get().strip(),
                categoria_var.get().strip(),
                vagas_novas,
            )
        except ValueError as erro:
            messagebox.showwarning(
                "Não foi possível editar",
                str(erro),
                parent=formulario,
            )
            return

        formulario.destroy()
        atualizar_lista_eventos()

        messagebox.showinfo(
            "Evento atualizado",
            f"{evento.titulo} foi atualizado.",
            parent=janela,
        )

    botoes = ttk.Frame(formulario)
    botoes.pack(pady=(0, 15))

    ttk.Button(
        botoes,
        text="Salvar alterações",
        command=salvar_alteracoes,
    ).pack(side="left", padx=5)

    ttk.Button(
        botoes,
        text="Cancelar",
        command=formulario.destroy,
    ).pack(side="left", padx=5)

def abrir_contratacao_divulgacao(evento):
    if (
        not isinstance(usuario_atual, Organizador)
        or evento.organizador.email.lower() != usuario_atual.email.lower()
    ):
        messagebox.showwarning(
            "Acesso negado",
            "Somente o organizador responsável pode contratar uma equipe.",
            parent=janela,
        )
        return

    if evento.status != "Publicado":
        messagebox.showwarning(
            "Não é possível contratar",
            "Só é possível contratar para um evento publicado.",
            parent=janela,
        )
        return

    nomes_contratados = {
        contratacao.equipe.nome.strip().casefold()
        for contratacao in evento.contratacoes
        if contratacao.status == "Ativa"
    }

    equipes_disponiveis = [
        equipe
        for equipe in equipes_divulgacao
        if equipe.nome.strip().casefold() not in nomes_contratados
    ]

    if not equipes_disponiveis:
        messagebox.showinfo(
            "Sem equipes disponíveis",
            "Todas as equipes já estão contratadas ativamente para este evento.",
            parent=janela,
        )
        return

    formulario = tk.Toplevel(janela)
    formulario.title("Contratar equipe de divulgação")
    formulario.geometry("430x350")
    formulario.transient(janela)
    formulario.grab_set()

    dados = ttk.LabelFrame(formulario, text="Equipe de divulgação", padding=15)
    dados.pack(fill="both", expand=True, padx=20, pady=15)

    opcoes_equipes = {
        (
            f"{equipe.nome} — R$ {equipe.preco:.2f}"
        ): equipe
        for equipe in equipes_disponiveis
    }

    equipe_var = tk.StringVar(value=list(opcoes_equipes.keys())[0])

    ttk.Label(dados, text="Escolha uma equipe:").pack(anchor="w")

    lista_equipes = ttk.Combobox(
        dados,
        textvariable=equipe_var,
        values=list(opcoes_equipes.keys()),
        state="readonly",
    )
    lista_equipes.pack(fill="x", pady=(0, 15))

    detalhes_equipe = ttk.Label(dados, text="", wraplength=360)
    detalhes_equipe.pack(anchor="w")

    def atualizar_detalhes(event=None):
        equipe = opcoes_equipes.get(equipe_var.get())

        if equipe is not None:
            detalhes_equipe.config(
                text=(
                    f"Serviços: {equipe.servicos}\n"
                    f"Preço: R$ {equipe.preco:.2f}"
                )
            )

    lista_equipes.bind("<<ComboboxSelected>>", atualizar_detalhes)
    atualizar_detalhes()

    def confirmar_contratacao():
        equipe = opcoes_equipes.get(equipe_var.get())

        if equipe is None:
            messagebox.showwarning(
                "Seleção inválida",
                "Escolha uma equipe da lista.",
                parent=formulario,
            )
            return

        try:
            evento.contratar_equipe(usuario_atual, equipe)
        except ValueError as erro:
            messagebox.showwarning(
                "Contratação não realizada",
                str(erro),
                parent=formulario,
            )
            return

        formulario.destroy()
        atualizar_lista_eventos()

        messagebox.showinfo(
            "Equipe contratada",
            f"{equipe.nome} foi contratada para {evento.titulo}.",
            parent=janela,
        )

    botoes = ttk.Frame(formulario)
    botoes.pack(pady=(0, 15))

    ttk.Button(
        botoes,
        text="Contratar equipe",
        command=confirmar_contratacao,
    ).pack(side="left", padx=5)

    ttk.Button(
        botoes,
        text="Cancelar",
        command=formulario.destroy,
    ).pack(side="left", padx=5)

def cancelar_contratacao_divulgacao(evento, contratacao):
    confirmar = messagebox.askyesno(
        "Cancelar contratação",
        f"Deseja cancelar a contratação da equipe "
        f"{contratacao.equipe.nome}?",
        parent=janela,
    )

    if not confirmar:
        return

    try:
        evento.cancelar_contratacao(usuario_atual, contratacao)
    except ValueError as erro:
        messagebox.showwarning("Não foi possível cancelar", str(erro))
        return

    atualizar_lista_eventos()
    messagebox.showinfo(
        "Contratação cancelada",
        f"A contratação da equipe {contratacao.equipe.nome} foi cancelada.",
    )


def substituir_equipe_divulgacao(evento, contratacao_atual):
    if (
        not isinstance(usuario_atual, Organizador)
        or evento.organizador.email.lower() != usuario_atual.email.lower()
    ):
        messagebox.showwarning(
            "Acesso negado",
            "Somente o organizador responsável pode substituir a equipe.",
            parent=janela,
        )
        return

    if (
        contratacao_atual not in evento.contratacoes
        or contratacao_atual.status != "Ativa"
    ):
        messagebox.showwarning(
            "Contratação indisponível",
            "Essa contratação não está mais ativa.",
            parent=janela,
        )
        return

    nomes_contratados = {
        contratacao.equipe.nome.strip().casefold()
        for contratacao in evento.contratacoes
        if contratacao.status == "Ativa"
    }

    equipes_disponiveis = [
        equipe
        for equipe in equipes_divulgacao
        if equipe.nome.strip().casefold() not in nomes_contratados
    ]

    if not equipes_disponiveis:
        messagebox.showinfo(
            "Sem outras equipes",
            "Não há outra equipe disponível para substituir esta.",
            parent=janela,
        )
        return

    formulario = tk.Toplevel(janela)
    formulario.title("Substituir equipe")
    formulario.geometry("430x350")
    formulario.transient(janela)
    formulario.grab_set()

    dados = ttk.LabelFrame(formulario, text="Nova equipe", padding=15)
    dados.pack(fill="both", expand=True, padx=20, pady=15)

    opcoes_equipes = {
        f"{equipe.nome} — R$ {equipe.preco:.2f}": equipe
        for equipe in equipes_disponiveis
    }

    equipe_var = tk.StringVar(value=list(opcoes_equipes.keys())[0])

    ttk.Label(dados, text="Escolha a equipe substituta:").pack(anchor="w")

    lista_equipes = ttk.Combobox(
        dados,
        textvariable=equipe_var,
        values=list(opcoes_equipes.keys()),
        state="readonly",
    )
    lista_equipes.pack(fill="x", pady=(0, 15))

    detalhes_equipe = ttk.Label(dados, text="", wraplength=360)
    detalhes_equipe.pack(anchor="w")

    def atualizar_detalhes(event=None):
        equipe = opcoes_equipes.get(equipe_var.get())

        if equipe is not None:
            detalhes_equipe.config(
                text=(
                    f"Serviços: {equipe.servicos}\n"
                    f"Preço: R$ {equipe.preco:.2f}"
                )
            )

    lista_equipes.bind("<<ComboboxSelected>>", atualizar_detalhes)
    atualizar_detalhes()

    def confirmar_substituicao():
        nova_equipe = opcoes_equipes.get(equipe_var.get())

        if nova_equipe is None:
            messagebox.showwarning(
                "Seleção inválida",
                "Escolha uma equipe da lista.",
                parent=formulario,
            )
            return

        try:
            evento.substituir_equipe(
                usuario_atual,
                contratacao_atual,
                nova_equipe,
            )
        except ValueError as erro:
            messagebox.showwarning(
                "Não foi possível substituir",
                str(erro),
                parent=formulario,
            )
            return

        formulario.destroy()
        atualizar_lista_eventos()

        messagebox.showinfo(
            "Equipe substituída",
            f"{contratacao_atual.equipe.nome} foi substituída por "
            f"{nova_equipe.nome}.",
            parent=janela,
        )

    botoes = ttk.Frame(formulario)
    botoes.pack(pady=(0, 15))

    ttk.Button(
        botoes,
        text="Substituir equipe",
        command=confirmar_substituicao,
    ).pack(side="left", padx=5)

    ttk.Button(
        botoes,
        text="Cancelar",
        command=formulario.destroy,
    ).pack(side="left", padx=5)

def adicionar_cartao(evento):
    cartao = ttk.Frame(conteudo_eventos, padding=10)
    cartao.pack(fill="x", pady=5)

    ttk.Label(
        cartao,
        text=evento.titulo,
        font=("Arial", 12, "bold"),
    ).pack(anchor="w")

    detalhes = (
        f"{evento.categoria} | {evento.data_hora} | {evento.local} | "
        f"{evento.vagas} vagas | Organizador: {evento.organizador.nome}"
    )

    ttk.Label(cartao, text=detalhes).pack(anchor="w")
    ttk.Label(cartao, text=evento.descricao).pack(anchor="w")

    rotulo_status = ttk.Label(cartao, text=f"Status: {evento.status}")
    rotulo_status.pack(anchor="w")

    eh_dono = (
        isinstance(usuario_atual, Organizador)
        and evento.organizador.email.lower() == usuario_atual.email.lower()
    )

    for contratacao in evento.contratacoes:
        linha_contratacao = ttk.Frame(cartao)
        linha_contratacao.pack(fill="x", anchor="w")

        ttk.Label(
            linha_contratacao,
            text=(
                f"Divulgação: {contratacao.equipe.nome} — "
                f"{contratacao.status}"
            ),
        ).pack(side="left", anchor="w")

        if (
            eh_dono
            and evento.status == "Publicado"
            and contratacao.status == "Ativa"
        ):
            ttk.Button(
                linha_contratacao,
                text="Cancelar contratação",
                command=lambda e=evento, c=contratacao:
                    cancelar_contratacao_divulgacao(e, c),
            ).pack(side="left", padx=5)

            ttk.Button(
                linha_contratacao,
                text="Substituir equipe",
                command=lambda e=evento, c=contratacao:
                    substituir_equipe_divulgacao(e, c),
            ).pack(side="left", padx=5)

    contador = ttk.Label(
        cartao,
        text=resumo_interesses(evento),
    )
    contador.pack(anchor="w", pady=(5, 0))

    if isinstance(usuario_atual, Participante) and evento.status == "Publicado":
        ttk.Button(
            cartao,
            text="Tenho interesse",
            command=lambda e=evento, c=contador: registrar_interesse(e, c),
        ).pack(anchor="w", pady=5)

    if eh_dono and evento.status == "Publicado":
        ttk.Button(
            cartao,
            text="Contratar divulgação",
            command=lambda e=evento: abrir_contratacao_divulgacao(e),
        ).pack(anchor="w", pady=5)

        botao_editar = ttk.Button(
            cartao,
            text="Editar evento",
            command=lambda e=evento, c=cartao: editar_evento(e, c),
        )
        botao_editar.pack(anchor="w", pady=5)

        ttk.Button(
            cartao,
            text="Cancelar evento",
            command=lambda e=evento: cancelar_evento(e),
        ).pack(anchor="w")

def atualizar_lista_eventos():
    for cartao in conteudo_eventos.winfo_children():
        cartao.destroy()

    for evento in eventos:
        adicionar_cartao(evento)

for evento in eventos:
    adicionar_cartao(evento)


def criar_evento():
    if not isinstance(usuario_atual, Organizador):
        messagebox.showwarning(
            "Acesso necessário",
            "Entre com uma conta de organizador para cadastrar eventos.",
            parent=janela,
        )
        return

    formulario = tk.Toplevel(janela)
    formulario.title("Cadastrar evento")
    formulario.geometry("420x610")
    formulario.transient(janela)
    formulario.grab_set()

    titulo_var = tk.StringVar()
    data_hora_var = tk.StringVar()
    local_var = tk.StringVar()
    categoria_var = tk.StringVar()
    vagas_var = tk.StringVar()

    dados = ttk.LabelFrame(formulario, text="Dados do evento", padding=15)
    dados.pack(fill="both", expand=True, padx=20, pady=15)

    ttk.Label(dados, text="Título:").pack(anchor="w")
    ttk.Entry(dados, textvariable=titulo_var).pack(fill="x", pady=(0, 8))

    ttk.Label(dados, text="Descrição:").pack(anchor="w")
    descricao_campo = tk.Text(dados, height=4, wrap="word")
    descricao_campo.pack(fill="x", pady=(0, 8))

    ttk.Label(dados, text="Data e horário:").pack(anchor="w")
    ttk.Entry(dados, textvariable=data_hora_var).pack(fill="x", pady=(0, 8))

    ttk.Label(dados, text="Local:").pack(anchor="w")
    ttk.Entry(dados, textvariable=local_var).pack(fill="x", pady=(0, 8))

    ttk.Label(dados, text="Categoria:").pack(anchor="w")
    ttk.Entry(dados, textvariable=categoria_var).pack(fill="x", pady=(0, 8))

    ttk.Label(dados, text="Número de vagas:").pack(anchor="w")
    ttk.Entry(dados, textvariable=vagas_var).pack(fill="x")

    def salvar_evento():
        titulo_novo = titulo_var.get().strip()
        descricao_nova = descricao_campo.get("1.0", "end").strip()
        data_hora_nova = data_hora_var.get().strip()
        local_novo = local_var.get().strip()
        categoria_nova = categoria_var.get().strip()
        vagas_texto = vagas_var.get().strip()

        if not all(
            [
                titulo_novo,
                descricao_nova,
                data_hora_nova,
                local_novo,
                categoria_nova,
                vagas_texto,
            ]
        ):
            messagebox.showwarning(
                "Campos incompletos",
                "Preencha todos os campos.",
                parent=formulario,
            )
            return

        try:
            vagas_novas = int(vagas_texto)
            if vagas_novas < 1:
                raise ValueError
        except ValueError:
            messagebox.showwarning(
                "Número de vagas inválido",
                "Informe um número inteiro maior que zero.",
                parent=formulario,
            )
            return

        novo_evento = Evento(
            titulo=titulo_novo,
            descricao=descricao_nova,
            data_hora=data_hora_nova,
            local=local_novo,
            categoria=categoria_nova,
            vagas=vagas_novas,
            organizador=usuario_atual,
        )

        novo_evento.publicar()
        eventos.append(novo_evento)

        formulario.destroy()
        atualizar_lista_eventos()

        messagebox.showinfo(
            "Evento cadastrado",
            f"{novo_evento.titulo} foi publicado.",
            parent=janela,
        )

    botoes = ttk.Frame(formulario)
    botoes.pack(pady=(0, 15))

    ttk.Button(
        botoes,
        text="Cadastrar evento",
        command=salvar_evento,
    ).pack(side="left", padx=5)

    ttk.Button(
        botoes,
        text="Cancelar",
        command=formulario.destroy,
    ).pack(side="left", padx=5)


ttk.Button(
    janela,
    text="Cadastrar evento",
    command=criar_evento,
).pack(pady=10)

janela.mainloop()