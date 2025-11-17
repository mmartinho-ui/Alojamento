class Alojamento:
    def __init__(self, id_alojamento: int, id_proprietario: int, nome_alojamento: str, morada: str, tipo_quarto: str, preco_noite: float):
        self.id_alojamento = id_alojamento
        self.id_proprietario = id_proprietario
        self.nome_alojamento = nome_alojamento
        self.morada = morada
        self.tipo_quarto = tipo_quarto
        self.preco_noite = preco_noite

    def to_dict(self) -> dict:
        return self.__dict__