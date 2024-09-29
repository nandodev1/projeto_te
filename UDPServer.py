import socket
import sys
import mouse

ss = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
ss.settimeout(0.5)
ss.bind(("", 9999))

try:
    print("Aguardando conexão...")
    add_init = 100
    while True:
        prefix = '192.168.1.'
        add_init += 1
        add_init_str = str(add_init)
        add_search = prefix + add_init_str
        try:
            ss.sendto( b'headmouse\n', ( add_search, 8266))
        except PermissionError:
            sys.stdout.write('Cliente não encontrado.\n')
            sys.stdout.write('Reiniciar busca S-s: sim ou N-n: não\n')
            choise = input()
            if choise == 'S' or choise == 's':
                add_init = 0
            else:
                sys.exit()
        except socket.gaierror:
            sys.stderr.write('Ero ao tentar enviar pacote\n')
        print('Procurando dispositivo cliente em: [' + add_search + ' porta: 8266] ', end='')
        sys.stdout.write(str(int((add_init*100)/255)) + ' %\n')
        try:
            data, adds = ss.recvfrom(12)
        except TimeoutError:
            continue
        if data == b'headmouse\n':
            break
    print("Conectado à endereço:", adds[0], " porta:", adds[1])
    ss.sendto(b'headmouse', adds)
    ss.settimeout(2)
    while True:
        try:
            data, adds = ss.recvfrom(12)
        except TimeoutError:
            sys.stderr.write('Conexão perdida!\n')
            print("Aguardando conexão...")
            add_init = 100
            while True:
                prefix = '192.168.1.'
                add_init += 1
                add_init_str = str(add_init)
                add_search = prefix + add_init_str
                try:
                    ss.sendto( b'headmouse\n', ( add_search, 8266))
                except PermissionError:
                    sys.stdout.write('Cliente não encontrado.\n')
                    sys.stdout.write('Reiniciar busca S-s: sim ou N-n: não\n')
                    choise = input()
                    if choise == 'S' or choise == 's':
                        add_init = 0
                    else:
                        sys.exit()
                except socket.gaierror:
                    sys.stderr.write('Ero ao tentar enviar pacote\n')
                print('Procurando dispositivo cliente em: [' + add_search + ' porta: 8266] ', end='')
                sys.stdout.write(str(int((add_init*100)/255)) + ' %\n')
                try:
                    data, adds = ss.recvfrom(12)
                except TimeoutError:
                    continue
                if data == b'headmouse\n':
                    break
            print("Conectado à endereço:", adds[0], " porta:", adds[1])
            ss.sendto(b'headmouse', adds)
            ss.settimeout(2)
            continue
        data = data.decode("ascii")
            #sys.stdout.write(data)
            #sys.stdout.write(data2.decode("ascii"))
        data = data.split(' ')
        if int(data[1]) < 2_000:
            mouse.move(0, -3, absolute=False, duration=0)
        if int(data[1]) > 5_000:
            mouse.move(0, 3, absolute=False, duration=0)
        if int(data[0]) < 0:
            mouse.move(3, 0, absolute=False, duration=0)
        if int(data[0]) > 4_000:
            mouse.move(-3, 0, absolute=False, duration=0)
    ss.close()
    print('Conexão finalizada.')
except KeyboardInterrupt:
    print('Finalizando servidor')
    ss.close()
    print('Servidor finalizado com sucesso.')

pass