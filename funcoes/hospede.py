from classes.hospede import Hospede
from classes.reserva import Reserva
from .utils import limpar_ecra, pausar, input_enter
from datetime import datetime
import uuid
from classes.gestor_dados import GestorDados
import re



def _verificar_disponibilidade(gestor_res:GestorDados, id_alo, data_in_str, data_out_str):
    todas_res = gestor_res.obter_todos()
    for r in todas_res:
        if r["id_alojamento"] == id_alo:
            try:
                r_in = datetime.strptime(r["check_in"], '%Y-%m-%d')
                r_out = datetime.strptime(r["check_out"], '%Y-%m-%d')
                pedido_in = datetime.strptime(data_in_str, '%Y-%m-%d')
                pedido_out = datetime.strptime(data_out_str, '%Y-%m-%d')
                
                if pedido_in < r_out and pedido_out > r_in:
                    return False 
                
                
                hoje = datetime.now()
                data_m1 = hoje
                if pedido_in < data_m1 or pedido_out < data_m1:
                    return False 

            except ValueError:
                continue 
    return True 




def listar_e_reservar(gestor_alojs:GestorDados, gestor_res:GestorDados):
    limpar_ecra()
    print("== ALOJAMENTOS DISPONÍVEIS ==\n")
    todos = gestor_alojs.obter_todos()
    if not todos:
        print("Não há alojamentos disponíveis de momento.")
        pausar(2)
        return

    for a in todos:
        print(f"[ID {a['id_alojamento']}] {a['nome_alojamento']} ({a['morada']}) - {a['preco_noite']}€/noite")
    
    try:
        escolha = int(input("\nIntroduza o ID do alojamento para reservar (0 para voltar): "))
        if escolha == 0: return

        aloj = gestor_alojs.encontrar_por_campo("id_alojamento", escolha)
        if not aloj:
            print("ID inválido.")
            pausar(2); return


        hoje = datetime.now()
 
        print(f"\nA reservar: {aloj['nome_alojamento']}")
        print("Dia de hoje: ",hoje)
        d_in = input("\nData Check-in (AAAA-MM-DD): ")
        d_out = input("Data Check-out (AAAA-MM-DD): ")

        try:
            dt_in = datetime.strptime(d_in, '%Y-%m-%d')
            dt_out = datetime.strptime(d_out, '%Y-%m-%d')
            if dt_out <= dt_in:
                print("\nData de check-out deve ser posterior ao check-in.")
                pausar(2); return
            if dt_in < hoje:
                print("\nData deverá ser posterior ao dia de hoje")
                pausar(2); return
        except ValueError:
            print("Formato de data inválido. Use AAAA-MM-DD.")
            pausar(2); return

        if not _verificar_disponibilidade(gestor_res, escolha, d_in, d_out):
            print("\nLamentamos mas não está disponivel")
            pausar(2)
            return
      
        print("O Alojamento está LIVRE,\nindique os dados abaixos para a reserva:")
        print("\n-- Dados do Hóspede --")
        
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
        

        hospede_atual = Hospede(nome=nome, email=email)

        
        cod = uuid.uuid4().hex[:3].upper()
        novo_id_res = gestor_res.gerar_novo_id("id_reserva")
        
        nova_reserva = Reserva(
            id_reserva=novo_id_res,
            id_alojamento=escolha,
            nome_hospede=hospede_atual.nome,
            email_hospede=hospede_atual.email,
            check_in=d_in,
            check_out=d_out,
            codigo_reserva=cod
        )
        gestor_res.adicionar(nova_reserva)
        print(f"\nRESERVADO! O seu código de reserva é: {cod}")
        print("Guarde este código para consultar a sua reserva.")
        input_enter()

    except ValueError:
        print("Erro nos dados inseridos.")
        pausar(2)

def consultar_minha_reserva(gestor_res:GestorDados, gestor_alojs:GestorDados):
    limpar_ecra()
    print("== CONSULTAR RESERVA ==\n")
    cod = input("Insira o código da reserva: ").upper()
    
    res = gestor_res.encontrar_por_campo("codigo_reserva", cod)
    if res:
        aloj = gestor_alojs.encontrar_por_campo("id_alojamento", res["id_alojamento"])
        nome_aloj = aloj["nome_alojamento"] if aloj else "Desconhecido"
        print(f"\nReserva encontrada para {res['nome_hospede']}!")
        print(f"Alojamento: {nome_aloj}")
        print(f"Data: {res['check_in']} até {res['check_out']}")
    else:
        print("\nReserva não encontrada.")
    input_enter()

def eliminar_minha_reserva(gestor_res):
    """Permite ao hóspede eliminar a sua própria reserva (APENAS COM O CÓDIGO)."""
    limpar_ecra()
    print("== ELIMINAR A MINHA RESERVA ==\n")
    
    codigo_consulta = input("Insira o seu Código de Reserva: ").upper()
    
    # 1. Encontrar a reserva
    reserva_encontrada = gestor_res.encontrar_por_campo("codigo_reserva", codigo_consulta)
    
    # 2. Validar (só pelo código)
    if reserva_encontrada:
        
        # 3. Pedir confirmação
        print("\nReserva encontrada!")
        print(f"Hóspede: {reserva_encontrada['nome_hospede']}")
        print(f"Datas: {reserva_encontrada['check_in']} a {reserva_encontrada['check_out']}")
        
        confirmar = input("\nTem a certeza que quer eliminar esta reserva? (s/n): ").lower()
        
        if confirmar == 's':
            # 4. Eliminar
            sucesso = gestor_res.eliminar_por_campo("codigo_reserva", codigo_consulta)
            if sucesso:
                print("\nReserva eliminada com sucesso.")
            else:
                print("\nERRO: Falha ao eliminar a reserva.")
        else:
            print("\nOperação cancelada.")
            
    else:
        print("\nERRO: Código de reserva não encontrado.")
    
    input_enter()