import unittest
from unittest.mock import patch, MagicMock
from db import BancoDeDados

class TestBancoDeDados(unittest.TestCase):

    @patch('db.mysql.connector.connect')
    def setUp(self, mock_connect):
        self.mock_db = MagicMock()
        self.mock_cursor = MagicMock()
        mock_connect.return_value = self.mock_db
        self.mock_db.cursor.return_value = self.mock_cursor
        self.banco_de_dados = BancoDeDados()

    def test_inserir_pacote(self):
        self.banco_de_dados.inserir_pacote('192.168.0.1', '192.168.0.2', 'TCP', 100)
        self.mock_cursor.execute.assert_called_once_with(
            "INSERT INTO pacotes (ip_origem, ip_destino, protocolo, tamanho_pacote) VALUES (%s, %s, %s, %s)",
            ('192.168.0.1', '192.168.0.2', 'TCP', 100)
        )
        self.mock_db.commit.assert_called_once()

    def test_buscar_top_cinco_ips_origem(self):
        self.mock_cursor.fetchall.return_value = [('192.168.0.1', 10), ('192.168.0.2', 8)]
        result = self.banco_de_dados.buscar_top_cinco_ips_origem()
        self.mock_cursor.execute.assert_called_once_with(
            "SELECT ip_origem, COUNT(*) FROM pacotes GROUP BY ip_origem ORDER BY COUNT(*) DESC LIMIT 5"
        )
        self.assertEqual(result, [('192.168.0.1', 10), ('192.168.0.2', 8)])

    def test_buscar_pacotes_por_protocolo(self):
        self.mock_cursor.fetchall.return_value = [('TCP', 10), ('UDP', 5)]
        result = self.banco_de_dados.buscar_pacotes_por_protocolo()
        self.mock_cursor.execute.assert_called_once_with(
            "SELECT protocolo, COUNT(*) FROM pacotes GROUP BY protocolo"
        )
        self.assertEqual(result, [('TCP', 10), ('UDP', 5)])

    def test_contar_pacotes(self):
        self.mock_cursor.fetchone.return_value = [15]
        result = self.banco_de_dados.contar_pacotes()
        self.mock_cursor.execute.assert_called_once_with("SELECT COUNT(*) FROM pacotes")
        self.assertEqual(result, 15)
