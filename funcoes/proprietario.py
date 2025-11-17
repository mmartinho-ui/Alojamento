from classes.proprietario import Proprietario
from classes.alojamento import Alojamento
from .utils import limpar_ecra, pausar, input_enter
import hashlib
import calendar 
from datetime import datetime, timedelta
from classes.gestor_dados import GestorDados 
import re


def criar_conta(gestor_props:GestorDados):
    limpar_ecra()
    print("\n-------------------------------------\n== CRIAR CONTA PROPRIETÁRIO ==\n-------------------------------------\n")
    while True:
            nome = input("\nNome: ")
            if len(nome.strip()) == 0:
                print("Erro: O nome não pode estar vazio.")
            else:
                if re.match(r"^[a-zA-ZÀ-ÿ\s]+$", nome):
                    break
                else:
                    print("Erro: Nome inválido (não use números ou símbolos especiais).")
    
    while True:
            email = input("Email: ")
            if re.match(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$', email):
                break
            else:
                print("Email inválido\n") 

    while True:
        user = input("\nUsername: ")
        if gestor_props.encontrar_por_campo("username", user):
            print("ERRO: Username já existe.")
        else:
            break
    
    
    while True:
        pwd = input("\nPassword: ")
        pwd_confirm = input("Confirme a password: ")
        if pwd != pwd_confirm:
            print("Passwords não coincidem. Coloque novamente.")
        else:
            pwd_hash = hashlib.sha256(pwd.encode("utf-8")).hexdigest()
            break
    
    
    

    novo_id = gestor_props.gerar_novo_id("id_proprietario")
    novo_prop = Proprietario(novo_id, nome, email, user, pwd_hash)
    gestor_props.adicionar(novo_prop)
    print("\nConta criada com sucesso!")
    pausar(2)

def login(gestor_props:GestorDados):
    limpar_ecra()
    print("\n-------------------------------------\n== LOGIN PROPRIETÁRIO ==\n-------------------------------------\n")
    user = input("Username: ")
    pwd = input("Password: ")
    
    prop = gestor_props.encontrar_por_campo("username", user)

    pwd_hash = hashlib.sha256(pwd.encode("utf-8")).hexdigest()

    if prop and prop["password"] == pwd_hash:
        return prop 
    else:
        print("\nERRO: Credenciais inválidas.")
        pausar(2)
        return None

def registar_alojamento(gestor_alojs:GestorDados, id_proprietario):
    limpar_ecra()
    print("\n-------------------------------------\n== NOVO ALOJAMENTO ==\n-------------------------------------\n")
    try:
        while True:
            nome = input("Nome do Alojamento: ")
            if len(nome.strip()) == 0:
                print("Nome não pode ser vazio\n")
            else: break
        
        while True:    
            morada = input("Morada: ")
            if len(morada.strip()) == 0:
                print("Morada não pode estar vazia\n")
            else: break

        while True:    
            tipo = input("Tipo (Moradia, Quarto, etc): ")
            if len(tipo.strip()) == 0:
                print("Tipo de alojamento não pode estar vazio.\n Sugestão: Moradia, Apartamento, Quarto, Tenda...\n")
            else: break
        
        while True:    
            try:
                preco = float(input("Preço por noite (€): "))
                if preco <= 0:
                    print("Valor não válido. Terá de ser superior a 0€.\n")
                else: break
            except ValueError:
                print("Formato inválido.\n")
        
        novo_id = gestor_alojs.gerar_novo_id("id_alojamento")
        novo_aloj = Alojamento(novo_id, id_proprietario, nome, morada, tipo, preco)
        gestor_alojs.adicionar(novo_aloj)
        print("\nAlojamento registado!")
    except ValueError:
        print("\nERRO: 1.")
    pausar(2)

def ver_meus_alojamentos(gestor_alojs:GestorDados, id_proprietario):
    limpar_ecra()
    print("\n-------------------------------------\n== OS MEUS ALOJAMENTOS ==\n-------------------------------------\n")
    todos = gestor_alojs.obter_todos()
    meus = [a for a in todos if a["id_proprietario"] == id_proprietario]
    
    if not meus:
        print("Ainda não tem alojamentos.")
    else:
        for a in meus:
            print(f"[ID {a['id_alojamento']}] {a['nome_alojamento']} - {a['preco_noite']}€")
    input_enter()

def ver_minhas_reservas(gestor_alojs:GestorDados, gestor_res:GestorDados, id_proprietario):
    limpar_ecra()
    print("------------------------------------------------------------------------\n\n")
    print("\n-------------------------------------\n====== AS MINHAS RESERVAS ======\n-------------------------------------\n")

    
    todos_alojs = gestor_alojs.obter_todos()
    meus_ids_aloj = [a["id_alojamento"] for a in todos_alojs if a["id_proprietario"] == id_proprietario]
    
    todas_res = gestor_res.obter_todos()
    res_minhas = [r for r in todas_res if r["id_alojamento"] in meus_ids_aloj]

    if not res_minhas:
        print("Não há reservas registadas.")
    else:
        for r in res_minhas:
            print(f"Reserva {r['codigo_reserva']} | Aloj. ID {r['id_alojamento']} | De {r['check_in']} a {r['check_out']}")
            print(f" -> Hóspede: {r['nome_hospede']} ({r['email_hospede']})\n")
    print("\n-------------------------------------\n======== CALENDÁRIO DE RESERVAS =======\n-------------------------------------")

    hoje = datetime.now()
    data_m1 = hoje
    
    #colocar uma selecao de qual mes pretende ver

    mes_2 = (data_m1.month % 12) + 1 
    ano_2 = data_m1.year + (1 if data_m1.month == 12 else 0) 
    data_m2 = datetime(year=ano_2, month=mes_2, day=1)

    mes_3 = (data_m2.month % 12) + 1
    ano_3 = data_m2.year + (1 if data_m2.month == 12 else 0)
    data_m3 = datetime(year=ano_3, month=mes_3, day=1)

    datas_calendarios = [data_m1]

    
    todos_alojs = gestor_alojs.obter_todos()
    ids_meus_alojamentos = {a["id_alojamento"] for a in todos_alojs if a["id_proprietario"] == id_proprietario}
    todas_res = gestor_res.obter_todos()

    ocupacao_total = {} 

    for r in todas_res:
        if r["id_alojamento"] in ids_meus_alojamentos:
            try:
                check_in = datetime.strptime(r['check_in'], '%Y-%m-%d').date()
                check_out = datetime.strptime(r['check_out'], '%Y-%m-%d').date()
                
                dia_atual = check_in
                while dia_atual < check_out:
                    chave_mes = (dia_atual.year, dia_atual.month)
                    
                    if chave_mes not in ocupacao_total:
                        ocupacao_total[chave_mes] = set()
                        
                    ocupacao_total[chave_mes].add(dia_atual.day)
                    dia_atual += timedelta(days=1)
            except ValueError:
                continue 

    for data_cal in datas_calendarios:
        ano = data_cal.year
        mes = data_cal.month
        
        dias_ocupados = ocupacao_total.get((ano, mes), set()) 

        cal = calendar.monthcalendar(ano, mes)
        
        print(f"---------- {calendar.month_name[mes]} {ano} ---------\n (Mês currente)")
        print("Seg  Ter  Qua  Qui  Sex  Sab  Dom")
        print("----------------------------------")
        
        for semana in cal:
            linha_semana = ""
            for dia in semana:
                if dia == 0:
                    linha_semana += "     " 
                elif dia in dias_ocupados:
                    linha_semana += f"[{dia:2}] " 
                else:
                    linha_semana += f" {dia:2}  " 
            print(linha_semana)

    print("\nLegenda: [Dia] = Dia com reserva")
    input_enter()


def eliminar_reservas(gestor_alojs:GestorDados, gestor_res:GestorDados, id_proprietario):
    limpar_ecra()
    print("\n-------------------------------------\n== ELIMINAR RESERVA ==\n-------------------------------------")
    
    todos_alojs = gestor_alojs.obter_todos()
    meus_ids_aloj = [a["id_alojamento"] for a in todos_alojs if a["id_proprietario"] == id_proprietario]
    
    todas_res = gestor_res.obter_todos()
    res_minhas = [r for r in todas_res if r["id_alojamento"] in meus_ids_aloj]

    if not res_minhas:
        print("Não há reservas registadas para eliminar.")
        pausar(2)
        return

    for r in res_minhas:
        print(f"-> Código: {r['codigo_reserva']} | Hóspede: {r['nome_hospede']} | Datas: {r['check_in']} a {r['check_out']}")
    
    print("\n-------------------------------------")
    codigo_para_eliminar = input("Insira o Código da Reserva a eliminar (ou '0' para cancelar): ").upper()

    if codigo_para_eliminar == '0':
        print("Operação cancelada.")
        pausar(1)
        return

    reserva_encontrada = None
    for res in res_minhas:
        if res["codigo_reserva"] == codigo_para_eliminar:
            reserva_encontrada = res
            break
            
    if not reserva_encontrada:
        print("\nERRO: Código de reserva não encontrado ou não lhe pertence.")
        pausar(2)
        return

    print(f"\nA eliminar reserva de: {reserva_encontrada['nome_hospede']}")
    confirmar = input("Tem a certeza? (s/n): ").lower()

    if confirmar == 's':
        sucesso = gestor_res.eliminar_por_campo("codigo_reserva", codigo_para_eliminar)
        if sucesso:
            print("\nReserva eliminada com sucesso.")
        else:
            print("\nERRO: Falha ao eliminar a reserva.")
    else:
        print("\nOperação cancelada.")
        
    pausar(2)