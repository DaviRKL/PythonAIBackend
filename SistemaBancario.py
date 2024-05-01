menu = """

[d] Depositar
[s] Sacar
[e] Extrato
[q] Sair

=> """

saldo = 0
limite = 500
extrato = ""
numero_saques = 0
LIMITE_SAQUES = 3

while True:

    opcao = input(menu)

    if opcao == "d":
        
        saldo += float(input("\nInsira o valor a ser depositado: "))
        extrato += f"Deposito: R${saldo} "
        print(f"\n{saldo} depositado com sucesso \nSeu saldo atual é {saldo}")

    elif opcao == "s":
        
        if numero_saques < LIMITE_SAQUES:
            
            valor_saque = float(input("\nInsira o valor a ser sacado: "))
            
            if valor_saque <= saldo:
                saldo -= valor_saque
                numero_saques += 1
                extrato += f"Saque: R${valor_saque} "
                print(f"\n{valor_saque} sacado com sucesso \nSeu saldo atual é {saldo}")

            else:
                print("Saldo indisponivel")
        else:
            print("Limite de saques diários execedido")

    elif opcao == "e":
      print(f"""

            Extrato: {extrato}
            Saldo atual: R${saldo}
=> """)

    elif opcao == "q":
        break

    else:
        print("Operação inválida, por favor selecione novamente a operação desejada.")
