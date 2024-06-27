# Requisitos do Projeto

Desenvolva um sistema que utilize o padrão de projetos Circuit Breaker para gerenciar possíveis falhas de interação entre um cliente e um provedor de dados. Implemente o padrão de projeto Circuit Breaker de modo a tolerar falhas na interação do cliente com o provedor de dados, observando os seguintes requisitos:

1. A interação entre o cliente e o provedor de dados deve ser feita utilizando uma das tecnologias vistas ao longo da disciplina;
2. O provedor de dados deve fornecer um serviço simples de armazenamento do tipo chave-valor;
3. Deve ser possível observar o comportamento dos componentes do sistema durante a execução do código;
4. O provedor de dados deve simular falhas com base em um padrão conhecido ou obedecer a comandos do usuário, de modo a permitir testarmos o funcionamento do circuit breaker.

Referência: https://martinfowler.com/bliki/CircuitBreaker.html

## Configuração do Ambiente

### 1. Configuração do Ambiente Virtual

É recomendado criar um ambiente virtual para isolar as dependências do projeto. Utilize o seguinte comando para criar e ativar um ambiente virtual:

```shell
python -m venv venv
source venv/bin/activate # No Windows use venv\Scripts\activate
```

### 2. Instalação dos Requisitos

Após ativar o ambiente virtual, instale as dependências necessárias usando o arquivo `requirements.txt` fornecido:

```shell
pip install -r requirements.txt
```

## Execução do Servidor (`server.py`)

O servidor Flask pode ser executado especificando a chance de falha como um argumento de linha de comando:

```shell
python server.py --fail_chance 0.3
```

- `--fail_chance`: Define a probabilidade de falha do serviço (0.0 à 1.0). Onde 1 equivale a 100% de change de falha e 0 a 0% de change de falha.

O servidor será iniciado e estará pronto para receber solicitações.

## Execução do Cliente (`client.py`)

Após a inicialização do servidor, o cliente pode ser iniciado da seguinte maneira:

```shell
python client.py --fail_max 3 --reset_timeout 10 --number_requests 10
```

- `--fail_max`:Número máximo de falhas antes de abrir o circuito.
- `--reset_timeout`: Tempo em segundos para aguardar antes de tentar reabrir o circuito.
- `--number_requests`: Número de requisições para testar o circuito.


## Demonstrações

### Cenário onde as requisições não falham

![](/figs/cenario_sem_falhas.gif)

### Cenário onde as requisições falham esporadicamente 

![](/figs/cenario_com_falhas_esporadicas.gif)

### Cenário em que todas as requisições falham

![](/figs/cenario_somente_com_falhas.gif)









