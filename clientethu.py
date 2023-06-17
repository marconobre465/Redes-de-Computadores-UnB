import socket
import pyaudio
import keyboard,pyaudio,sys,select

# Configurações do cliente
SERVER_HOST = '192.168.237.117'  # Endereço IP do servidor
SERVER_PORT = 12345  # Porta do servidor

def run_client():
    flag = True
    # Conecta ao servidor
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((SERVER_HOST, SERVER_PORT))
    print(f'conexao estabelecida com {SERVER_HOST}')

    # Envia o nome do cliente para o servidor
    name = socket.gethostname()
    client_socket.send(name.encode('utf-8'))

    while True:
        # Solicita o comando ao usuário
        command = input("\n\nDigite o comando a ser enviado ao servidor:\n1. sair\n2. amigos\n3.musicas\n4.ouvir\n5. remoto\n")

        if command == 'sair':
            break

        # Envia o comando para o servidor
        client_socket.send(command.encode('utf-8'))

        # Recebe e imprime a resposta do servidor
        response = client_socket.recv(1024).decode('utf-8')
        print(response)
        

        if command == 'ouvir':
            escolha = input()
            client_socket.send(escolha.encode('utf-8'))
            p = pyaudio.PyAudio()
            stream = p.open(format=pyaudio.paInt16,
                            channels=2,
                            rate=44100,
                            output=True)
            data = client_socket.recv(1024)
            while data:   
                stream.write(data)
                data = client_socket.recv(1024)

            while flag:
                newcommand = input("\n\nDigite o comando a ser enviado ao servidor:\n1. pausar\n2. parar\n")
                client_socket.send(newcommand.encode('utf-8'))
                musicaacabar = False #troca com o comando dps?
                if newcommand == 'parar' or musicaacabar:
                    flag = False
                    break
                    #para o streaming da musica botar o codigo depois

                elif newcommand == 'pausar':
                    while True:
                        newnewcommand = input("\n\nDigite o comando a ser enviado ao servidor:\n1. retomar\n2. reiniciar\n3.parar")

                        client_socket.send(newnewcommand.encode('utf-8'))

                        if newnewcommand == 'parar':
                            flag = False
                            break

                        #elif newnewcommand == 'retomar':

                        #elif newnewcommand == 'reiniciar':

                break           
                    

        elif command == 'remoto': #nao vai controlar com pause ou parar, somente manda tocar
            escolha = input() #servidor da lista de clientes que nao o seu e aqui vc escolhe

            client_socket.send(escolha.encode('utf-8'))

            response2 = client_socket.recv(1024).decode('utf-8') 

            print(response2) #vai dar mensagem de conectado e da lista de musicas de novo

            musica2 = input()
            client_socket.send(musica2.encode('utf-8'))
            #codigo pro streaming mandado pro cliente escolhido e servidor faz o trabalho de streamar

            response3 = client_socket.recv(1024).decode('utf-8') 
            print(response3)

                    
    # Encerra a conexão
    client_socket.close()

def pause():
    keyboard.wait('c')


# Inicia o cliente
run_client()