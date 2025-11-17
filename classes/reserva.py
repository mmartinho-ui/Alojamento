class Reserva:
    def __init__(self, id_reserva: int, id_alojamento: int, nome_hospede: str, email_hospede: str, check_in: str, check_out: str, codigo_reserva: str):
        self.id_reserva = id_reserva
        self.id_alojamento = id_alojamento
        self.nome_hospede = nome_hospede
        self.email_hospede = email_hospede
        self.check_in = check_in
        self.check_out = check_out
        self.codigo_reserva = codigo_reserva

    def to_dict(self) -> dict:
        return self.__dict__