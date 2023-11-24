import socket
import json
import threading
import time

returnFromServer = 0

class Client:
    def __init__(self, server: int, port: int):
        self._socketClient = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self._PORT = port
        self._HEADER = 64
        self._FORMAT = "utf-8"
        self._SERVER = server
        self._socketClient.connect((self._SERVER, self._PORT))
        listenThread = threading.Thread(target=self.listenFromServer)
        listenThread.start()
        
    
    def send(self, msg: any) -> None:
        if type(msg) == list:
            msg = {"nome" : msg[0], "args" : msg[1:]}

        msg = json.dumps(msg).encode(self._FORMAT)
        lenMsg = len(msg)
        lenMsg = str(lenMsg).encode(self._FORMAT)
        lenMsg += b' '*(self._HEADER - len(lenMsg))
        self._socketClient.send(lenMsg)
        self._socketClient.send(msg)   


    def listenFromServer(self) -> bool:
        global returnFromServer
        listening = True
        while listening:
            lenMsgReceived = self._socketClient.recv(self._HEADER).decode(self._FORMAT)
            if lenMsgReceived:
                lenMsgReceived = int(lenMsgReceived)
                msgReceived = self._socketClient.recv(lenMsgReceived).decode(self._FORMAT)
                msgReceived = json.loads(msgReceived)
                # print(f"MESSAGE RECEIVED FROM SERVER: {msgReceived}")
                returnFromServer = msgReceived

if __name__ == "__main__":
    client = Client(socket.gethostbyname(socket.gethostname()), 5050)
    input()

    msg = "lista"
    print("LISTA DE FUNÇÕES DISPONÍVEIS NO SERVIDOR:")
    client.send(msg)
    time.sleep(1)
    print(returnFromServer)

    input()
    msg = ["add", 88, 4]
    print(f"RETORNO DA FUNÇÃO {msg[0]} PARA OS PARÂMETROS {msg[1]} E {msg[2]}:")
    client.send(msg)
    time.sleep(1) 
    print(returnFromServer)    

    input()
    msg = ["sub", 35, 3]
    print(f"RETORNO DA FUNÇÃO {msg[0]} PARA OS PARÂMETROS {msg[1]} E {msg[2]}:")
    client.send(msg)
    time.sleep(1)
    print(returnFromServer)

    input()
    msg = ["distancia_entre_dois_pontos", 5, 6, 7, 8]
    print(f"RETORNO DA FUNÇÃO {msg[0]} PARA OS PARÂMETROS {msg[1]}, {msg[2]}, {msg[3]}, {msg[4]}:")
    client.send(msg)
    time.sleep(1)
    print(returnFromServer)

    input()
    msg = ["mmc", 8, 24]
    print(f"RETORNO DA FUNÇÃO {msg[0]} PARA OS PARÂMETROS {msg[1]} E {msg[2]}:")
    client.send(msg)
    time.sleep(1)
    print(returnFromServer)

    input()
    msg = ["mdc", 6, 15]
    print(f"RETORNO DA FUNÇÃO {msg[0]} PARA OS PARÂMETROS {msg[1]} E {msg[2]}:")
    client.send(msg)
    time.sleep(1)
    print(returnFromServer)

    input()
    msg = ["eh_primo", 7]
    print(f"RETORNO DA FUNÇÃO {msg[0]} PARA O PARÂMETRO {msg[1]}:")
    client.send(msg)
    time.sleep(1)
    print(returnFromServer)

    input()
    msg = ["eh_primo", 10]
    print(f"RETORNO DA FUNÇÃO {msg[0]} PARA O PARÂMETRO {msg[1]}:")
    client.send(msg)
    time.sleep(1)
    print(returnFromServer)

    input()
    msg = ["celsius_para_fahrenheit", 10]
    print(f"RETORNO DA FUNÇÃO {msg[0]} PARA O PARÂMETRO {msg[1]}:")
    client.send(msg)
    time.sleep(1)
    print(returnFromServer)

    input()
    msg = ["fahrenheit_para_celsius", 50]
    print(f"RETORNO DA FUNÇÃO {msg[0]} PARA O PARÂMETRO {msg[1]}:")
    client.send(msg)
    time.sleep(1)
    print(returnFromServer)

    input()
    msg = ["fibonacci", 5]
    print(f"RETORNO DA FUNÇÃO {msg[0]} PARA O PARÂMETRO {msg[1]}:")
    client.send(msg)
    time.sleep(1)
    print(returnFromServer)

    input()
    msg = "DISCONNECT"
    client.send(msg)
    
    
