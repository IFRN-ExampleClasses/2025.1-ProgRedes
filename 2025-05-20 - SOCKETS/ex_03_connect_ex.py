import socket, sys

strHost = input('\nInforme o nome do HOST ou URL do site: ')

# https://pt.wikipedia.org/wiki/Lista_de_portas_dos_protocolos_TCP_e_UDP
lstPorts = [22, 23, 25, 80, 443, 5432, 8080]

try:
   strIPHost = socket.gethostbyname(strHost)
except:
    sys.exit(f'\nERRO: Não foi possível resolver o nome do host.\n{sys.exc_info()}')
else:
    print(f'\nIP do HOST: {strIPHost}\n')
    for intPort in lstPorts:
        socketTeste = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        socketTeste.settimeout(5)
        print(f'Testando a porta {intPort:>4}... ', end='')
        try:
            socketTeste.connect_ex((strIPHost, intPort))
        except KeyboardInterrupt:
            sys.exit('\n\nSaindo...\n')
        except:
            print(f'ERRO... {sys.exc_info()}')
        else:
            print(f'OK...')
        finally:
            socketTeste.close()