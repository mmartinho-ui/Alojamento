from classes.gestor_dados import GestorDados
import funcoes.menus as menus
import funcoes.proprietario as f_prop
import funcoes.hospede as f_hosp

def main():
    gestor_props = GestorDados("proprietarios.json")
    gestor_alojs = GestorDados("alojamentos.json")
    gestor_res = GestorDados("reservas.json")

    while True:
        
        opcao = menus.menu_inicial()

        if opcao == 1: 
            while True:
                op_prop = menus.menu_proprietario_inicial()
                if op_prop == 1: 
                    prop_logado = f_prop.login(gestor_props)
                    if prop_logado:
                        
                        while True:
                            op_logado = menus.menu_proprietario_logado(prop_logado["nome"])
                            if op_logado == 1:
                                f_prop.registar_alojamento(gestor_alojs, prop_logado["id_proprietario"])
                            elif op_logado == 2:
                                f_prop.ver_meus_alojamentos(gestor_alojs, prop_logado["id_proprietario"])
                            elif op_logado == 3:
                                f_prop.ver_minhas_reservas(gestor_alojs, gestor_res, prop_logado["id_proprietario"])
                            elif op_logado == 4:
                                f_prop.eliminar_reservas(gestor_alojs, gestor_res, prop_logado["id_proprietario"])
                                pass
                            elif op_logado == 0:
                                break 
                elif op_prop == 2: 
                    f_prop.criar_conta(gestor_props)
                elif op_prop == 0: 
                    break

        elif opcao == 2: 
             while True:
                op_hosp = menus.menu_hospede_inicial()
                if op_hosp == 1:
                    f_hosp.listar_e_reservar(gestor_alojs, gestor_res)
                elif op_hosp == 2:
                    f_hosp.consultar_minha_reserva(gestor_res, gestor_alojs)
                elif op_hosp == 3:
                    f_hosp.eliminar_minha_reserva(gestor_res)
                elif op_hosp == 0:
                    break

        elif opcao == 0: 
            print("\nA encerrar...")
            break
        else:
            print("Opção inválida.")

if __name__ == "__main__":
    main()