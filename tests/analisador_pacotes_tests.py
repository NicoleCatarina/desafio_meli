import unittest
from unittest.mock import patch, MagicMock

from analisador_pacotes import AnalisadorPacotes


class TestAnalisadorPacotes(unittest.TestCase):

    @patch('analisador_pacotes.BancoDeDados')
    def setUp(self, mock_banco_de_dados):
        self.mock_db = mock_banco_de_dados.return_value
        self.analisador = AnalisadorPacotes()

    def test_processar_pacote_ip(self):
        pacote = MagicMock()
        pacote.haslayer.return_value = True
        pacote.getlayer.return_value.src = '192.168.0.1'
        pacote.getlayer.return_value.dst = '192.168.0.2'
        self.analisador.processar_pacote(pacote)
        self.mock_db.inserir_pacote.assert_called_once_with('192.168.0.1', '192.168.0.2', 'IP', len(pacote))

    def test_processar_pacote_arp(self):
        pacote = MagicMock()
        pacote.haslayer.side_effect = lambda x: x == 'ARP'
        pacote.getlayer.return_value.psrc = '192.168.0.1'
        pacote.getlayer.return_value.pdst = '192.168.0.2'
        self.analisador.processar_pacote(pacote)
        self.mock_db.inserir_pacote.assert_called_once_with('192.168.0.1', '192.168.0.2', 'ARP', len(pacote))

    def test_processar_pacote_tcp(self):
        pacote = MagicMock()
        pacote.haslayer.side_effect = lambda x: x == 'TCP'
        pacote.getlayer.return_value.src = '192.168.0.1'
        pacote.getlayer.return_value.dst = '192.168.0.2'
        self.analisador.processar_pacote(pacote)
        self.mock_db.inserir_pacote.assert_called_once_with('192.168.0.1', '192.168.0.2', 'TCP', len(pacote))

    def test_processar_pacote_udp(self):
        pacote = MagicMock()
        pacote.haslayer.side_effect = lambda x: x == 'UDP'
        pacote.getlayer.return_value.src = '192.168.0.1'
        pacote.getlayer.return_value.dst = '192.168.0.2'
        self.analisador.processar_pacote(pacote)
        self.mock_db.inserir_pacote.assert_called_once_with('192.168.0.1', '192.168.0.2', 'UDP', len(pacote))

    def test_iniciar_captura(self):
        with patch('analisador_pacotes.sniff') as mock_sniff:
            self.analisador.iniciar_captura(interface='eth0', timeout=10)
            mock_sniff.assert_called_once_with(iface='eth0', prn=self.analisador.processar_pacote, store=False, timeout=10)

    def test_imprimir_estatisticas(self):
        self.mock_db.contar_pacotes.return_value = 10
        self.mock_db.buscar_pacotes_por_protocolo.return_value = [('TCP', 5), ('UDP', 3)]
        self.mock_db.buscar_top_cinco_ips_origem.return_value = [('192.168.0.1', 4), ('192.168.0.2', 3)]

        with patch('builtins.print') as mock_print:
            self.analisador.imprimir_estatisticas()
            mock_print.assert_any_call("Total de pacotes capturados: 10")
            mock_print.assert_any_call("Número de pacotes por protocolo:")
            mock_print.assert_any_call("Protocolo TCP: 5 pacotes")
            mock_print.assert_any_call("Protocolo UDP: 3 pacotes")
            mock_print.assert_any_call("Top 5 endereços IP de origem com mais tráfego:")
            mock_print.assert_any_call("Endereço IP 192.168.0.1: 4 pacotes")
            mock_print.assert_any_call("Endereço IP 192.168.0.2: 3 pacotes")
