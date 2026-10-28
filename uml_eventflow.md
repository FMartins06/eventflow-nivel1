```mermaid  
classDiagram
    class Usuario {
        +nome: str
        +email: str
        +senha: str
        +tipo_de_perfil()
    }

    class Organizador {
        +tipo_de_perfil()
    }

    class Participante {
        +tipo_de_perfil()
    }

    class GerenciadorUsuarios {
        +usuarios: list
        +cadastrar(nome, email, senha, tipo)
        +autenticar(email, senha)
    }

    class Evento {
        +titulo: str
        +descricao: str
        +data_hora: str
        +local: str
        +categoria: str
        +vagas: int
        +status: str
        +publicar()
        +demonstrar_interesse(participante)
        +cancelar()
        +editar(...)
        +contratar_equipe(organizador, equipe)
        +cancelar_contratacao(organizador, contratacao)
        +substituir_equipe(organizador, contratacao, equipe)
    }

    class Interesse {
        +participante: Participante
        +status: str
    }

    class EquipeDivulgacao {
        +nome: str
        +servicos: str
        +preco: float
    }

    class ContratacaoDivulgacao {
        +organizador: Organizador
        +evento: Evento
        +equipe: EquipeDivulgacao
        +status: str
    }

    Usuario <|-- Organizador
    Usuario <|-- Participante

    GerenciadorUsuarios "1" o-- "0..*" Usuario : gerencia
    Organizador "1" -- "0..*" Evento : organiza

    Evento "1" *-- "0..*" Interesse : contém
    Evento "1" *-- "0..*" ContratacaoDivulgacao : registra

    Interesse "*" --> "1" Participante : pertence a
    ContratacaoDivulgacao "*" --> "1" Organizador : contratante
    ContratacaoDivulgacao "*" --> "1" EquipeDivulgacao : equipe contratada

    Evento ..> Participante : registra interesse
    Evento ..> EquipeDivulgacao : contrata equipe
    ```