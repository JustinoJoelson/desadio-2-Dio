from abc import ABC, abstractmethod, abstractproperty
from datetime import datetime

# --- CLASSE BASE ABSTRATA DE INTERFACE ---
class Transacao(ABC):
    @property
    @abstractproperty
    def valor(self):
        pass

    @abstractmethod # CORREÇÃO: Usando @abstractmethod (método de instância abstrato)
    def registrar(self, conta):
        pass

# --- CLASSE CLIENTE (BASE) ---
class Cliente:
    def __init__(self, endereco):
        # AJUSTE: Usando _ para proteger os atributos (Encapsulamento)
        self._endereco = endereco
        self._contas = []

    # AJUSTE: Adicionando properties para leitura dos atributos protegidos
    @property
    def endereco(self):
        return self._endereco

    @property
    def contas(self):
        return self._contas

    def realizar_transacao(self, conta, transacao):
        # O método realizar_transacao delega a responsabilidade para o objeto Transacao
        return transacao.registrar(conta)

    def adicionar_conta(self, conta):
        self._contas.append(conta)

# --- CLASSE CLIENTE CONCRETA (HERANÇA) ---
class PessoaFisica(Cliente):
    def __init__(self, nome, data_nascimento, cpf, endereco):
        super().__init__(endereco)
        # AJUSTE: Usando _ para proteger os atributos da PessoaFisica
        self._nome = nome
        self._data_nascimento = data_nascimento
        self._cpf = cpf

    @property
    def nome(self):
        return self._nome
    
    @property
    def cpf(self):
        return self._cpf
    
    @property
    def data_nascimento(self):
        return self._data_nascimento


# --- CLASSE BASE CONTA (ABSTRATA) ---
class Conta(ABC): # AJUSTE: Tornando Conta abstrata, como o UML sugere indiretamente
    def __init__(self, numero, cliente):
        self._saldo = 0
        self._numero = numero
        self._agencia = "0001"
        self._cliente = cliente
        self._historico = Historico()

    @property
    def saldo(self):
        return self._saldo

    @property
    def numero(self):
        return self._numero

    @property
    def agencia(self):
        return self._agencia

    @property
    def cliente(self):
        return self._cliente

    @property
    def historico(self):
        return self._historico
    
    # AJUSTE: Métodos abstratos. A lógica de saque e depósito
    # CONCRETA (com limites e regras) será definida nas subclasses.
    @abstractmethod
    def sacar(self, valor):
        pass

    @abstractmethod
    def depositar(self, valor):
        pass
    
    # Método auxiliar para a lógica comum de saque/depósito
    # Implementação movida para ContaCorrente para seguir o foco do desafio.

# --- CLASSE CONTA CONCRETA (HERANÇA) ---
class ContaCorrente(Conta):
    def __init__(self, numero, cliente, limite=500, limite_saques=3):
        super().__init__(numero, cliente)
        self._limite = limite
        self._limite_saques = limite_saques

    # Implementação CONCRETA do método sacar (sobrescrevendo o abstrato da classe pai)
    def sacar(self, valor):
        # Sua lógica de saque (limite e contagem de saques) está correta e mantida
        numero_saques = len(
            [
                transacao
                for transacao in self.historico.transacoes
                if transacao["tipo"] == Saque.__name__
            ]
        )

        excedeu_limite = valor > self._limite
        excedeu_saques = numero_saques >= self._limite_saques

        if excedeu_limite:
            print("\n@@@ Operação falhou! O valor do saque excede o limite. @@@")
        elif excedeu_saques:
            print("\n@@@ Operação falhou! Número máximo de saques excedido. @@@")
        elif valor > self.saldo:
            print("\n@@@ Operação falhou! Você não tem saldo suficiente. @@@")
        elif valor > 0:
            self._saldo -= valor # Acesso direto ao atributo protegido de Conta
            print("\n=== Saque realizado com sucesso! ===")
            return True
        else:
            print("\n@@@ Operação falhou! O valor informado é inválido. @@@")
        
        return False

    # Implementação CONCRETA do método depositar (sobrescrevendo o abstrato da classe pai)
    def depositar(self, valor):
        if valor > 0:
            self._saldo += valor # Acesso direto ao atributo protegido de Conta
            print("\n=== Depósito realizado com sucesso! ===")
            return True
        else:
            print("\n@@@ Operação falhou! O valor informado é inválido. @@@")
            return False

    def __str__(self):
        return f"""\
            Agência:\t{self.agencia}
            C/C:\t\t{self.numero}
            Titular:\t{self.cliente.nome}
        """

# --- CLASSE DE COMPOSIÇÃO ---
class Historico:
    def __init__(self):
        self._transacoes = []

    @property
    def transacoes(self):
        return self._transacoes

    def adicionar_transacao(self, transacao):
        self._transacoes.append(
            {
                "tipo": transacao.__class__.__name__,
                # AJUSTE: Usando transacao.valor (property)
                "valor": transacao.valor,
                "data": datetime.now().strftime("%d-%m-%Y %H:%M:%S"),
            }
        )

# --- CLASSES DE TRANSAÇÃO CONCRETA ---
class Saque(Transacao):
    def __init__(self, valor):
        self._valor = valor

    @property
    def valor(self):
        return self._valor

    def registrar(self, conta):
        # Delega a lógica de saque para o método sacar() da Conta
        sucesso_transacao = conta.sacar(self.valor)

        if sucesso_transacao:
            # Adiciona a si mesmo (self) ao histórico se for bem-sucedido
            conta.historico.adicionar_transacao(self)
        
        return sucesso_transacao


class Deposito(Transacao):
    def __init__(self, valor):
        self._valor = valor

    @property
    def valor(self):
        return self._valor

    def registrar(self, conta):
        # Delega a lógica de depósito para o método depositar() da Conta
        sucesso_transacao = conta.depositar(self.valor)

        if sucesso_transacao:
            # Adiciona a si mesmo (self) ao histórico se for bem-sucedido
            conta.historico.adicionar_transacao(self)
        
        return sucesso_transacao