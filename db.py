import os

import mysql.connector

db_host = os.getenv('DB_HOST')
db_user = os.getenv('DB_USER')
db_password = os.getenv('DB_PASSWORD')
db_name = os.getenv('DB_NAME')

class BancoDeDados:
    def __init__(self):
        self.db = mysql.connector.connect(
            host=db_host,
            user=db_user,
            password=db_password,
            database=db_name
        )
        self.cursor = self.db.cursor()

    def inserir_pacote(self, ip_origem, ip_destino, protocolo, tamanho_pacote):
        self.cursor.execute(
            "INSERT INTO pacotes (ip_origem, ip_destino, protocolo, tamanho_pacote) VALUES (%s, %s, %s, %s)",
            (ip_origem, ip_destino, protocolo, tamanho_pacote)
        )
        self.db.commit()

    def buscar_top_cinco_ips_origem(self):
        self.cursor.execute("SELECT ip_origem, COUNT(*) FROM pacotes GROUP BY ip_origem ORDER BY COUNT(*) DESC LIMIT 5")
        top_ips = self.cursor.fetchall()
        return top_ips

    def buscar_pacotes_por_protocolo(self):
        self.cursor.execute("SELECT protocolo, COUNT(*) FROM pacotes GROUP BY protocolo")
        contagem_protocolos = self.cursor.fetchall()
        return contagem_protocolos

    def contar_pacotes(self):
        self.cursor.execute("SELECT COUNT(*) FROM pacotes")
        total_pacotes = self.cursor.fetchone()[0]
        return total_pacotes

