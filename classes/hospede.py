class Hospede:
    def __init__(self, nome: str, email: str):
        self.nome = nome
        self.email = email
    
    def to_dict(self) -> dict:
        return self.__dict__
   