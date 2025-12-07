# 🏦 Sistema Bancário Orientado a Objetos (POO) em Python

Este projeto implementa um sistema bancário simples, utilizando os conceitos fundamentais da Programação Orientada a Objetos (POO) em Python. O objetivo principal foi refatorar uma implementação procedural inicial para um modelo baseado em classes, focado em **encapsulamento**, **herança** e **abstração** conforme um diagrama UML.

## 📐 Modelo de Classes (UML)

A estrutura do projeto segue o seguinte modelo de classes UML, que define as relações de herança e composição entre as entidades (Cliente, Conta, Transação, Histórico, etc.):



*Nota: As classes abstratas (como `Transacao` e `Conta`) e os atributos protegidos (`_saldo`, `_agencia`) foram implementados utilizando a biblioteca `abc` e convenções Python (prefixo `_`).*

## ✨ Funcionalidades

O sistema implementa as seguintes operações bancárias:

* **Clientes:** Cadastro e armazenamento de clientes (Pessoa Física) como objetos.
* **Contas:** Criação de contas correntes (Com Herança de `Conta`).
* **Depósito:** Registro de depósitos.
* **Saque:** Realização de saques com regras de negócio específicas:
    * Limite de R$ 500,00 por saque.
    * Limite máximo de 3 saques diários.
* **Extrato/Histórico:** Visualização de todas as transações realizadas, armazenadas na composição da classe `Historico`.

  ## 💡 Conceitos de POO Aplicados

Este projeto serve como um estudo de caso prático para os seguintes conceitos de Programação Orientada a Objetos em Python:

1.  **Herança:** `PessoaFisica` herda de `Cliente` e `ContaCorrente` herda de `Conta`.
2.  **Abstração:** Uso das classes abstratas `Conta` e `Transacao` (`from abc import ABC, abstractmethod`).
3.  **Composição:** A classe `Conta` possui uma instância da classe `Historico`.
4.  **Encapsulamento:** Uso de atributos protegidos (com prefixo `_`) e métodos `@property` para controle de acesso (ex: `saldo`, `endereco`).


   
