from datetime import datetime
from Reserva import Reserva

def fazer_checkout():
    id_res = int(input("\nDigite o ID da Reserva para Checkout: "))
    for i, r in enumerate(lista_reservas):
        if r.id == id_res and r.status == "Ativa":
            r.status = "Finalizada"
            r.suite.status = "Disponível"
            print(f"Checkout concluído! Total pago: R${r.valor_total:.2f}")
            return
    print("Reserva ativa não encontrada.")

def fazer_checkin(lista_clientes, lista_suites, lista_reservas):
    print("\n--- INICIAR CHECK-IN ---")
    
    try:
        id_cliente = int(input("ID do Cliente: "))
    except ValueError:
        print("❌ O ID deve ser um número.")
        return

    cliente = next((c for c in lista_clientes if c.id == id_cliente), None)
    
    if not cliente:
        print("❌ Cliente não encontrado no sistema.")
        return

    num_suite = input("Número da Suíte: ")
    suite = next((s for s in lista_suites if s.numero == num_suite), None)

    if not suite:
        print("❌ Suíte não encontrada.")
        return
    
    if suite.status != "Disponível":
        print(f"⚠️ A suíte {num_suite} está {suite.status}.")
        return

    try:
        d_in = input("Data de Entrada (DD/MM/AAAA): ")
        d_out = input("Data de Saída (DD/MM/AAAA): ")
        
        datetime.strptime(d_in, "%d/%m/%Y")
        datetime.strptime(d_out, "%d/%m/%Y")
    except ValueError:
        print("❌ Erro: Use o formato DD/MM/AAAA para as datas.")
        return

    nova_reserva = Reserva(cliente, suite, d_in, d_out, "Ativa")
    
    suite.status = "Ocupada"
    lista_reservas.append(nova_reserva)
    
    print(f"\n✅ Check-in concluído para {cliente.nome}!")
    print(f"🏨 Suíte: {suite.numero} | Status da Reserva: {nova_reserva.status}")