import socket
import threading
import os,pickle,pyaudio,struct,wave


class TCPserver:
    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.bind((self.host, self.port))
        self.clients = {}

    def handle_client(self, client_socket, client_address):
        while True:
            # Recebe a mensagem do cliente
            data = client_socket.recv(1024)
            if not data:
                break

            message = data.decode('utf-8')
            print(f"Recebido de {client_address}: {message}")

            if message == 'amigos':
                # Monta a lista de clientes conectados
                client_list = []

                for client in self.clients:
                    if client == client_socket:
                        client_list.append(f'{self.clients[client]} (eu)')
                    else:
                        client_list.append(self.clients[client])
                    

                # Envia a lista de clientes de volta ao cliente que fez a solicitação
                response ="\nLista de clientes online:\n" + (", ".join(client_list))
                
                client_socket.sendall(response.encode('utf-8'))

            elif message == 'musicas':
            # Obtém a lista de músicas no diretório do servidor
                music_list = os.listdir('C:\\Users\\solen\\OneDrive\\Documentos\\projetoredes\\musica')

                # Envia a lista de músicas de volta ao cliente
                response = '\nconfira a lista de musicas disponiveis para o streaming:\n' + "\n  ".join(music_list)
                client_socket.sendall(response.encode('utf-8'))

            elif message == 'ouvir':
                music_list = os.listdir('C:\\Users\\solen\\OneDrive\\Documentos\\projetoredes\\musica')
                response = '\n\nescolha o numero da musica que deseja ouvir:\n'
                for i in range(len(music_list)):
                    response += f'{i + 1}. {music_list[i]}\n'
                client_socket.sendall(response.encode('utf-8'))
                escolha = client_socket.recv(1024)
                esc = int(escolha)
                wf = wave.open(music_list[esc-1], 'rb')
                p = pyaudio.PyAudio()
                stream = p.open(format=p.get_format_from_width(wf.getsampwidth()),
                                channels=wf.getnchannels(),
                                rate=wf.getframerate(),
                                input=True,
                                frames_per_buffer=1024)
                data = None
                while True:
                    if client_socket:
                        print(client_socket)
                        while True:
                            data = wf.readframes(1024)
                            a = pickle.dumps(data)
                            message = struct.pack("Q",len(a))+a
                            client_socket.sendall(message)

            elif message == 'remoto':
                # Monta a lista de clientes conectados
                client_list = []

                for client in self.clients:
                    if client != client_socket:
                        client_list.append(self.clients[client])

                response ="\nEm que dispositivo deseja tocar musica remotamente?\n" + (", ".join(client_list))
                
                client_socket.sendall(response.encode('utf-8'))

                #ainda fazer de acordo com os envios em loop do cliente
            



            else:
                # Envia a mensagem de volta ao cliente
                client_socket.sendall(('\nopcao invalida. por favor insira novamente.\n').encode('utf-8'))
                

        # Remove o cliente da lista quando a conexão é encerrada
        del self.clients[client_socket]
        client_socket.close()
        print(f'{client_address} foi desconectado')

    def run(self):
        self.server_socket.listen(5)
        print(f"Servidor iniciado. Aguardando conexoes em {self.host}:{self.port}.")

        while True:
            client_socket, client_address = self.server_socket.accept()
            print(f"Cliente conectado: {client_address}")

            # Recebe o nome do cliente
            name = client_socket.recv(1024).decode('utf-8')

            # Adiciona o cliente à lista de clientes
            self.clients[client_socket] = name

            # Inicia uma nova thread para lidar com o cliente
            client_thread = threading.Thread(target=self.handle_client, args=(client_socket, client_address))
            client_thread.start()

    def close(self):
        for client_socket in self.clients.keys():
            client_socket.close()
        self.server_socket.close()

def get_local_machine_info():
    HOST = socket.gethostname()
    ip_address = socket.gethostbyname(HOST)
    return HOST, ip_address


PORT = 12345  # Porta para conexão
HOST, ip_address = get_local_machine_info()
print(f"Nome do computador: {HOST}")
print(f"Endereco IP: {ip_address}")

# Cria e inicia o servidor
server = TCPserver(HOST, PORT)
server.run()