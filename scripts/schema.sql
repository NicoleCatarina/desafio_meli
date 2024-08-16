CREATE TABLE IF NOT EXISTS pacotes (
    id INT AUTO_INCREMENT PRIMARY KEY,
    ip_origem VARCHAR(15),
    ip_destino VARCHAR(15),
    protocolo VARCHAR(15),
    tamanho_pacote INT
);