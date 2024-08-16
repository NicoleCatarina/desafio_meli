# Analisador de Tráfego de Rede

## Descrição

Esta aplicação captura pacotes de uma interface de rede especificada e exibe estatísticas básicas sobre o tráfego.

## Requisitos

- Docker
- Docker Compose

## Configuração e Execução

### Passo 1: Clonar o Repositório

Clone o repositório para sua máquina local

### Passo 2: Executar aplicação

Dentro do diretório do projeto, executar os comandos abaixo em seu terminal considerando os seguintes parâmetros:

INTERFACE: É a interface de rede que você deseja capturar os pacotes. 

Exemplos:
- eth0: Interface de rede Ethernet padrão.
- lo: Interface de loopback local.

TIMEOUT: É o tempo em segundos que a aplicação permanecerá capturando os pacotes da interface especificada.

*Caso nada seja colocado nos paramentros, sera considerado como default:*

INTERFACE=eth0 e TIMEOUT=10
#### Comandos:
O comando abaixo ira executar o docker compose, baixando as imagens necessárias e construindo os conteiner para simular o ambiente:
```
INTERFACE=eth0 TIMEOUT=2 docker-compose up -d
```
Ja o próximo comando, exibirá em seu terminal as estatisticas dos pacotes capturados:
```
docker-compose logs -f app
```

## Resultado
A aplicação exibirá as seguintes estatisticas sobre o trafego:

```
Total de pacotes capturados: 3183

Número de pacotes por protocolo:
Protocolo IP: 3182 pacotes
Protocolo Outro: 1 pacotes

Top 5 endereços IP de origem com mais tráfego:
Endereço IP 172.18.0.3: 3086 pacotes
Endereço IP 172.18.0.2: 96 pacotes
Endereço IP Desconhecido: 1 pacotes
```

