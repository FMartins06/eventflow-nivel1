class Usuario:
    def __init__(self, nome, email, senha=None):
        self.nome = nome
        self.email = email
        self.senha = senha

    def tipo_de_perfil(self):
        return "Usuário"

class Organizador(Usuario):
    def tipo_de_perfil(self):
        return "Organizador"


class Participante(Usuario):
    def tipo_de_perfil(self):
        return "Participante"

class GerenciadorUsuarios:
    def __init__(self):
        self.usuarios = []

    def cadastrar(self, nome, email, senha, tipo):
        if not nome.strip() or not email.strip() or not senha:
            raise ValueError("Preencha nome, email e senha.")

        email = email.strip().lower()

        for usuario in self.usuarios:
            if usuario.email.lower() == email:
                raise ValueError("Já existe uma conta com esse email.")

        if tipo == "organizador":
            usuario = Organizador(nome, email, senha)
        elif tipo == "participante":
            usuario = Participante(nome, email, senha)
        else:
            raise ValueError("O tipo deve ser organizador ou participante.")

        self.usuarios.append(usuario)
        return usuario

    def autenticar(self, email, senha):
        email = email.strip().lower()

        for usuario in self.usuarios:
            if usuario.email.lower() == email and usuario.senha == senha:
                return usuario

        raise ValueError("Email ou senha incorretos.")

class Interesse:
    def __init__(self, participante, status):
        self.participante = participante
        self.status = status

class EquipeDivulgacao:
    def __init__(self, nome, servicos, preco):
        self.nome = nome
        self.servicos = servicos
        self.preco = preco


class ContratacaoDivulgacao:
    def __init__(self, organizador, evento, equipe):
        self.organizador = organizador
        self.evento = evento
        self.equipe = equipe
        self.status = "Ativa"

class Evento:
    def __init__(
        self,
        titulo,
        descricao,
        data_hora,
        local,
        categoria,
        vagas,
        organizador,
    ):
        self.titulo = titulo
        self.descricao = descricao
        self.data_hora = data_hora
        self.local = local
        self.categoria = categoria
        self.vagas = vagas
        self.organizador = organizador
        self.status = "Rascunho"
        self.interesses = []
        self.contratacoes = []

    def publicar(self):
        self.status = "Publicado"

    def demonstrar_interesse(self, participante):
        if self.status != "Publicado":
            raise ValueError("O evento não está publicado.")

        for interesse in self.interesses:
            if interesse.participante.email == participante.email:
                raise ValueError(
                    "Esse participante já demonstrou interesse."
                )

        confirmados = sum(
            1
            for interesse in self.interesses
            if interesse.status == "Confirmado"
        )

        if confirmados < self.vagas:
            status = "Confirmado"
        else:
            status = "Lista de espera"

        novo_interesse = Interesse(participante, status)
        self.interesses.append(novo_interesse)

        return novo_interesse

    def cancelar(self):
        if self.status != "Publicado":
            raise ValueError("Somente eventos publicados podem ser cancelados.")

        self.status = "Cancelado"

        for contratacao in self.contratacoes:
            if contratacao.status == "Ativa":
                contratacao.status = "Cancelada"

    def editar(self, titulo, descricao, data_hora, local, categoria, vagas):
        if self.status != "Publicado":
            raise ValueError("Somente eventos publicados podem ser editados.")

        textos = [titulo, descricao, data_hora, local, categoria]

        if any(not texto.strip() for texto in textos):
            raise ValueError("Nenhum campo de texto pode ficar vazio.")

        if vagas < 1:
            raise ValueError("O evento precisa ter pelo menos uma vaga.")

        confirmados = sum(
            1
            for interesse in self.interesses
            if interesse.status == "Confirmado"
        )

        if vagas < confirmados:
            raise ValueError(
                "Não é possível definir menos vagas que o número de confirmados."
            )

        self.titulo = titulo
        self.descricao = descricao
        self.data_hora = data_hora
        self.local = local
        self.categoria = categoria
        self.vagas = vagas

    def contratar_equipe(self, organizador, equipe):
        if not isinstance(organizador, Organizador):
            raise ValueError("Somente um organizador pode contratar uma equipe.")

        if organizador.email.lower() != self.organizador.email.lower():
            raise ValueError(
                "Somente o organizador responsável pode contratar para este evento."
            )

        if self.status != "Publicado":
            raise ValueError(
                "Só é possível contratar para um evento publicado."
            )

        for contratacao_existente in self.contratacoes:
            mesmo_nome = (
                contratacao_existente.equipe.nome.strip().casefold()
                == equipe.nome.strip().casefold()
            )

            if mesmo_nome and contratacao_existente.status == "Ativa":
                raise ValueError(
                    "Essa equipe já foi contratada para este evento."
                )

        contratacao = ContratacaoDivulgacao(
            organizador,
            self,
            equipe,
        )
        self.contratacoes.append(contratacao)

        return contratacao

    def cancelar_contratacao(self, organizador, contratacao):
        if not isinstance(organizador, Organizador):
            raise ValueError("Somente um organizador pode cancelar uma contratação.")

        if organizador.email.lower() != self.organizador.email.lower():
            raise ValueError(
                "Somente o organizador responsável pode alterar as contratações."
            )

        if contratacao not in self.contratacoes:
            raise ValueError("Essa contratação não pertence a este evento.")

        if contratacao.status != "Ativa":
            raise ValueError("Essa contratação não está ativa.")

        contratacao.status = "Cancelada"

    def substituir_equipe(self, organizador, contratacao_atual, nova_equipe):
        if contratacao_atual not in self.contratacoes:
            raise ValueError("Essa contratação não pertence a este evento.")

        if contratacao_atual.status != "Ativa":
            raise ValueError("A contratação atual não está ativa.")

        nova_contratacao = self.contratar_equipe(organizador, nova_equipe)
        contratacao_atual.status = "Cancelada"

        return nova_contratacao