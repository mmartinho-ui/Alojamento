class Proprietario:
    def __init__(self, id_proprietario: int, nome: str, email: str, username: str, password: str):
        self.id_proprietario = id_proprietario
        self.nome = nome
        self.email = email
        self.username = username
        self.password = password
    
    def to_dict(self) -> dict:
        return self.__dict__