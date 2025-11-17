from .utils import limpar_ecra

def menu_inicial():
    limpar_ecra()
    print("\n-------------------------------------\n== ALOJAMENTO FÁCIL ==\n-------------------------------------\n")
    print("1: Sou proprietário")
    print("2: Sou hóspede")
    print("\n0: Sair")
    try:
        return int(input("-------------------------------------\nSelecione a opção desejada: "))
    except ValueError:
        return -1

def menu_proprietario_inicial():
    limpar_ecra()
    print("\n-------------------------------------\n== LOGIN PROPRIETÁRIO ==\n-------------------------------------\n")
    print("1: Fazer Login")
    print("2: Criar Conta Nova")
    print("\n0: Voltar")
    try:
        return int(input("-------------------------------------\nSelecione a opção: "))
    except ValueError:
        return -1

def menu_proprietario_logado(nome):
    limpar_ecra()
    print(f"\n-------------------------------------\n== BEM-VINDO, {nome} ==\n-------------------------------------\n")
    print("1: Registar novo alojamento")
    print("2: Ver os meus alojamentos")
    print("3: Ver reservas das minhas propriedades")
    print("4: Eliminar os meus alojamentos")
    print("\n0: Logout")
    try:
        return int(input("-------------------------------------\nSelecione a opção: "))
    except ValueError:
        return -1

def menu_hospede_inicial():
    limpar_ecra()
    print("\n-------------------------------------\n== BEM-VINDO, HÓSPEDE ==\n-------------------------------------\n")
    print("1: Ver Alojamentos e Reservar")
    print("2: Consultar a minha Reserva")
    print("3: Eliminar a minha Reserva")
    print("\n0: Voltar")
    try:
        return int(input("-------------------------------------\nSelecione a opção: "))
    except ValueError:
        return -1