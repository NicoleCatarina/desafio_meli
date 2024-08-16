import os

from analisador_pacotes import AnalisadorPacotes


def main():
    interface = os.getenv('INTERFACE')
    timeout = int(os.getenv('TIMEOUT'))

    analisador = AnalisadorPacotes()
    analisador.iniciar_captura(interface, timeout)
    analisador.imprimir_estatisticas()

if __name__ == "__main__":
    main()
