import textwrap
from abc import ABC, abstractmethod
from datetime import datetime

class Cliente:
    def __init__(self, endereco) -> None:
        self.endereco = endereco
        self.contas = []
    
    def realizar_transacao(self,conta, transacao):
        transacao.registrar(conta)
    
    def adicionar_conta(self, conta):
        self.contas.append(conta)

class PessoaFisica(Cliente):
    def __init__(self, cpf, nome, data_nascimento, endereco) -> None:
       super().__init__(endereco)
       self.cpf = cpf
       self.nome = nome
       self.data_nascimento = data_nascimento

class Conta:
    def __init__(self, numero, cliente) -> None:
        self._saldo = 0
        self._num_conta = numero
        self._agencia = "0001"
        self._cliente = cliente
        self._historico = Historico()
    
    @classmethod
    def nova_conta(cls, cliente, numero):
        return cls(numero,cliente)
    
    @property
    def saldo(self):
        return self._saldo
    
    @property
    def numero(self): 
        return self._num_conta
    
    @property
    def agencia(self): 
        return self._agencia
    
    @property
    def cliente(self): 
        return self._cliente
    
    @property
    def historico(self): 
        return self._historico
         
    def sacar(self,valor_saque):
        saldo= self._saldo
        excedeu_saldo = valor_saque > saldo
        
        if excedeu_saldo:
            print("\nSaldo insuficiente!")
            
        elif valor_saque > 0:
            self._saldo -= valor_saque
            print(f"\n{valor_saque} sacado com sucesso \nSeu saldo atual é {self._saldo}")
            return True
    
        else: 
            print("Valor Invalido!")
        
        return False 
    
    def depositar(self, valor):
        if valor > 0:
            self._saldo += valor
            print("\nDepósito realizado com sucesso!")
        else:
            print("\nOperação falhou! O valor informado é inválido.")
            return False

        return True

class ContaCorrente(Conta):
    def __init__(self, num_conta, cliente, limite = 500, limite_saques = 3):
        super().__init__( num_conta, cliente)
        self.limite = limite
        self.limite_saques = limite_saques
    
    def sacar(self, valor):
        numero_saques = len(
            [transacao for transacao in self.historico.transacoes if transacao["tipo"] == Saque.__name__]
        )
        
        excedeu_limite = valor > self.limite
        excedeu_saques = numero_saques > self.limite_saques
        
        if excedeu_limite:
            print("\nValor do saque excede o limite")
            
        elif excedeu_saques:
            print("\nLimite de saques excedido")
        
        else: 
            return super().sacar(valor)
        
        return False   
    
    def __str__(self) -> str:
        return f"""\
            Agencia:\t{self.agencia}
            C/C:\t\t{self.numero}
            titular:\t{self.cliente.nome}
        """

class Historico:
    def __init__(self) -> None:
        self._transacoes = []
        
    @property
    def transacoes(self):
        return self._transacoes
    
    def adicionar_transacao(self, transacao):
        self._transacoes.append({
            "tipo": transacao.__class__.__name__,
            "valor" : transacao.valor,
            "data" : datetime.now()
        })
    
class Transacao(ABC):
    @property
    @abstractmethod
    def registrar():
        pass
    @abstractmethod
    def registrar(self, conta):
        pass
    
class Deposito(Transacao):
    def __init__(self, valor):
        self._valor = valor

    @property
    def valor(self):
        return self._valor

    def registrar(self, conta):
        sucesso_transacao = conta.depositar(self.valor)

        if sucesso_transacao:
            conta.historico.adicionar_transacao(self)
     
class Saque(Transacao):
    def __init__(self, valor) -> None:
        self.valor = valor
    def registrar(self, conta):
        sucesso_transacao = conta.sacar(self.valor)
        
        if sucesso_transacao:
            conta.historico.adicionar_transacao(self)

num_conta = 0

menu = """

[1] Criar usuario
[2] Criar conta
[3] Depositar
[4] Sacar
[5] Extrato
[6] Contas
[7] Sair

=> """

def criar_usuario(clientes):
    cpf = int(input("\nInsira seu cpf somente com os numeros: "))
    Cliente = filtrar_cliente(cpf, clientes)
    
    if Cliente:
        print("\n Este CPF já possui conta!")
        return
    
    nome = input("Informe o nome completo: ")
    data_nascimento = input("Informe a data de nascimento (dd-mm-aaaa): ")
    endereco = input("Informe o endereço: ")

    cliente = PessoaFisica(nome=nome, data_nascimento=data_nascimento, cpf=cpf, endereco=endereco)
    clientes.append(cliente)
    print("\n=== Cliente criado com sucesso! ===")

def exibir_usuario(cpf_user):

    for usuario["cpf"] in usuario:
        if usuario["cpf"] == cpf_user:
            print(usuario)
            
def exibir_conta(num_conta):

    for conta_corrente["num_conta"] in conta_corrente:
        if conta_corrente["num_conta"] == num_conta:
            print(conta_corrente)
       
def criar_conta_corrente(num_conta, clientes, contas):
    cpf = int(input("\nInsira seu cpf somente com os numeros: "))
    Cliente = filtrar_cliente(cpf, clientes)
    
    if not Cliente:
        print("\n Cliente não encontrado!")
        return
    
    conta = ContaCorrente.nova_conta(cliente=Cliente, numero= num_conta)
    contas.append(conta)
    Cliente.contas.append(conta)
    print(f"Conta criada com sucesso! Seu numero da conta é {num_conta}")

def filtrar_cliente(cpf, clientes):
    clientes_filtrados = [cliente for cliente in clientes if cliente.cpf == cpf]
    return clientes_filtrados[0] if clientes_filtrados else None

def recuperar_conta_cliente(cliente):
    if not cliente.contas:
        print("\n Cliente não possui conta!")
        return
    
    return cliente.contas[0]
          
def depositar(clientes):
    cpf = int(input("\nInsira seu cpf somente com os numeros: "))
    cliente = filtrar_cliente(cpf, clientes)

    if not cliente:
        print("\n@@@ Cliente não encontrado! @@@")
        return

    valor = float(input("Informe o valor do depósito: "))
    transacao = Deposito(valor)

    conta = recuperar_conta_cliente(cliente)
    if not conta:
        return

    cliente.realizar_transacao(conta, transacao)
   
def sacar(clientes):
    cpf = int(input("\nInsira seu cpf somente com os numeros: "))
    Cliente = filtrar_cliente(cpf, clientes)
    
    if not Cliente:
        print("\n Cliente não encontrado!")
        return
    
    valor = float(input("Informe o valor do saque:"))
    transacao = Saque(valor)
    
    conta = recuperar_conta_cliente(Cliente)
    
    if not conta:
        return
    
    Cliente.realizar_transacao(conta, transacao)

def mostrar_extrato (clientes):
    cpf = int(input("\nInsira seu cpf somente com os numeros: "))
    cliente = filtrar_cliente(cpf, clientes)
    
    if not Cliente:
        print("\n Cliente não encontrado!")
        return 
    
    conta = recuperar_conta_cliente(cliente)
    if not conta:
        return
    
    print("\n================ EXTRATO ================")
    transacoes = conta.historico.transacoes
    
    extrato = ""
    
    if not transacoes:
        extrato = "Não foram realizadas movimentações."
    else:
        for transacao in transacoes:
            extrato += f"\n{transacao['tipo']}:\tR$ {transacao['valor']:.2f}"
    print(extrato)
    print(f"\nSaldo:\tR$ {conta.saldo:.2f}")
    print("============================================")
 
def listar_contas(contas):
    for conta in contas:
        print("=" * 100)
        print(textwrap.dedent(str(conta)))
  
def main():
    clientes = []
    contas = []
    
    while True:

        opcao = input(menu)

        if opcao == "1":
            criar_usuario(clientes)
            
        
        elif opcao == "2":
            numero_conta = len(contas) + 1
            criar_conta_corrente(numero_conta, clientes, contas)
           
        
        elif opcao == "3":
            depositar(clientes)
            
        elif opcao == "4":
            sacar(clientes)
            
        elif opcao == "5":
           mostrar_extrato(clientes)
        
        elif opcao == "6":
            listar_contas(contas)
        
        elif opcao == "7":
            break
        
        else:
            print("Operação inválida, por favor selecione novamente a operação desejada.")
main()
