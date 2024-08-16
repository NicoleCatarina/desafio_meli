import scapy.interfaces
from scapy.all import sniff

from db import BancoDeDados


class AnalisadorPacotes:

    def __init__(self):
        self.db = BancoDeDados()

    def processar_pacote(self, pacote):
        if pacote.haslayer('IP'):
            camada_ip = pacote.getlayer('IP')
            ip_origem = camada_ip.src
            ip_destino = camada_ip.dst
            protocolo = 'IP'
        elif pacote.haslayer('ARP'):
            camada_arp = pacote.getlayer('ARP')
            ip_origem = camada_arp.psrc
            ip_destino = camada_arp.pdst
            protocolo = 'ARP'
        elif pacote.haslayer('TCP'):
            camada_tcp = pacote.getlayer('TCP')
            ip_origem = camada_tcp.src
            ip_destino = camada_tcp.dst
            protocolo = 'TCP'
        elif pacote.haslayer('UDP'):
            camada_udp = pacote.getlayer('UDP')
            ip_origem = camada_udp.src
            ip_destino = camada_udp.dst
            protocolo = 'UDP'
        else:
            ip_origem = 'Desconhecido'
            ip_destino = 'Desconhecido'
            protocolo = 'Outro'

        tamanho_pacote = len(pacote)
        self.db.inserir_pacote(ip_origem, ip_destino, protocolo, tamanho_pacote)

    def iniciar_captura(self, interface='eth0', timeout=10):
        sniff(iface=interface, prn=self.processar_pacote, store=False, timeout=timeout)

    def imprimir_estatisticas(self):
        # Total de pacotes capturados
        total_pacotes = self.db.contar_pacotes()

        if total_pacotes == 0:
            print(f"Não houveram pacotes capturados")
            return

        print(f"Total de pacotes capturados: {total_pacotes}")
        print()

        # Número de pacotes por protocolo
        contagem_protocolos = self.db.buscar_pacotes_por_protocolo()
        print("Número de pacotes por protocolo:")
        for protocolo, contagem in contagem_protocolos:
            print(f"Protocolo {protocolo}: {contagem} pacotes")
        print()

        # Top 5 endereços IP de origem com mais tráfego
        top_ips = self.db.buscar_top_cinco_ips_origem()
        print("Top 5 endereços IP de origem com mais tráfego:")
        for ip, contagem in top_ips:
            print(f"Endereço IP {ip}: {contagem} pacotes")