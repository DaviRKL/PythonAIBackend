menu = """

[1] Criar usuario
[2] Criar conta
[3] Ver contas
[4] Ver usuários
[5] Depositar
[6] Sacar
[7] Extrato
[8] Sair

=> """

saldo = 0
limite = 500
extrato = ""
numero_saques = 0
LIMITE_SAQUES = 3
valor_deposito = 0
num_conta = 1
AGENCIA = "0001"
usuario = {"cpf": {"nome": None, "dataNasc": None, "endereco": None}}
conta_corrente = {"num_conta": {"agencia": None,"usuario":None}}

def criar_usuario(nome, data_nasc, cpf_user, endereco):
    usuario.pop("cpf", {}) 
    resultado = cpf_user in usuario
    if resultado != True:
        usuario.update({cpf_user: {"nome": nome, "data_nasc": data_nasc, "endereco": endereco}})
        print(f"{nome} cadastrado com sucesso!")
        print(usuario)
       
    else:
        print("CPF já cadastrado")

def exibir_usuario(cpf_user):

    for usuario["cpf"] in usuario:
        if usuario["cpf"] == cpf_user:
            print(usuario)
            
def exibir_conta(num_conta):

    for conta_corrente["num_conta"] in conta_corrente:
        if conta_corrente["num_conta"] == num_conta:
            print(conta_corrente)
       
def criar_conta_corrente(agencia, num_conta, usuario):
    conta_corrente.pop("num_conta", {}) 
    conta_corrente.update({num_conta: {"agencia": agencia, "usuario": usuario}})
    print(f"Conta criada com sucesso! Seu numero da conta é {num_conta} ")
           
def depositar(valor_deposito, saldo, /):
    global extrato
    saldo += valor_deposito
    extrato += f"Deposito: R${saldo} "
    print(f"\n{valor_deposito} depositado com sucesso \nSeu saldo atual é {saldo}")

def sacar(*, saldo, valor_saque, extrato, numero_saques):
    if valor_saque <= saldo:
        saldo -= valor_saque
        numero_saques += 1
        extrato += f"Saque: R${valor_saque} "
        print(f"\n{valor_saque} sacado com sucesso \nSeu saldo atual é {saldo}")
        
    else:
        print("Saldo indisponivel")

def mostrar_extrato (saldo,/, *, extrato):
     print(f"""

            Extrato: {extrato}
            Saldo atual: R${saldo}
=> """)

while True:

    opcao = input(menu)

    if opcao == "1":
        
        cpf = int(input("\nInsira seu cpf somente com os numeros: "))
        nome = input("Insira seu nome: ")
        data_nasc = input("Insira sua data de nascimento: ")
        endereco = input("Insira seu endereço: ")
        criar_usuario(nome= nome, data_nasc= data_nasc, cpf_user= cpf, endereco= endereco)
    
    elif opcao == "2":
        
        cpf = int(input("\nInsira seu cpf somente com os numeros: "))    
        criar_conta_corrente(agencia=AGENCIA, num_conta= num_conta,usuario= cpf)
        num_conta += 1
    
    elif opcao == "3":
        
        numero_da_conta = int(input("\nInsira seu numero da conta: "))    
        exibir_conta(num_conta= numero_da_conta )
        
    elif opcao == "4":
        
       cpf = int(input("\nInsira seu cpf somente com os numeros: "))    
       exibir_usuario(cpf_user=cpf)
        
    elif opcao == "5":
        
        valor_deposito += float(input("\nInsira o valor a ser depositado: "))
        depositar(valor_deposito, saldo)
       
    elif opcao == "6":
        
        if numero_saques < LIMITE_SAQUES:
            
            valor_saque = float(input("\nInsira o valor a ser sacado: "))
            sacar(saldo = saldo, valor_saque= valor_saque, extrato= extrato, numero_saques= numero_saques)
           
        else:
            print("Limite de saques diários execedido")

    elif opcao == "7":
        
        mostrar_extrato(saldo, extrato=extrato)
    

    elif opcao == "8":
        break

    else:
        print("Operação inválida, por favor selecione novamente a operação desejada.")
