import inspect
import socket
import threading
import json

class Server:

    def __init__(self, port: int):
        self._socketServer = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self._PORT = port
        self._HEADER = 64
        self._FORMAT = "utf-8"
        self._HOST = socket.gethostbyname(socket.gethostname())
        self._DISCONNECT_MESSAGE = "DISCONNECT"
        self._socketServer.bind((self._HOST, self._PORT))
        self._FUNCTIONS = {}

    def start(self) -> None:
        self._socketServer.listen()
        print(f"[LISTENING FOR CONNECTIONS] Server is listening for connections on {self._HOST}")
        while True:
            connection, address = self._socketServer.accept()
            thread = threading.Thread(target=self.handleClient, args=(connection, address))
            thread.start()
            print(f"[ACTIVE CONNECTIONS] {threading.active_count()-1}")

    def handleClient(self, connection: socket, address: str) -> None:
        print(f"[NEW CONNECTION] {address} connected")

        connected = True
        while connected:
            msgLength = connection.recv(self._HEADER).decode(self._FORMAT)
            if msgLength:
                msgLength = int(msgLength)
                msg = connection.recv(msgLength).decode(self._FORMAT)
                
                print(f"[{address}] {msg}")

                try:                
                    msg = json.loads(msg)
                    if type(msg) == dict:
                        result = self.handleFunction(msg)
                    elif type(msg) == str:
                        if msg == self._DISCONNECT_MESSAGE:
                            connected = False
                            result = "Disconnecting from server"
                        elif "list" in msg:
                            result = self.listFunctions()

                    result = json.dumps(str(result)).encode(self._FORMAT)
                    resultLen = len(result)
                    resultLen = str(resultLen).encode(self._FORMAT)
                    resultLen += b' '*(self._HEADER - len(resultLen))
                    connection.send(resultLen)
                    connection.send(result)

                except json.decoder.JSONDecodeError as e:
                    print("NOT JSON")
                    
        connection.close()

    def registerFunction(self, function) -> None:
        try:
            self._FUNCTIONS.update({function.__name__ : function})
        except:
            return Exception("A non function object has been passed into Server")

    def handleFunction(self, data: dict) -> any:
        if data["nome"] not in self._FUNCTIONS.keys():
            return Exception("The function is not registered in the server")

        try: 
            result = self._FUNCTIONS[data["nome"]](*data["args"])
        except TypeError as e:
            return Exception("The arguments were not passed correctly into the function")


        return result
    
    def listFunctions(self) -> list:
        functionsList = []
        for key in self._FUNCTIONS.keys():
            functionData = {"nome" : key,
                             "tipos de argumentos" : [],
                             "tipo de retorno" : inspect.signature(self._FUNCTIONS[key]).return_annotation
                             }   

            for t in inspect.signature(self._FUNCTIONS[key]).parameters.items():
                functionData["tipos de argumentos"].append(t[1])

            functionsList.append(functionData)  

        return functionsList       

def add(*a:int) -> int:
    sum = 0
    for i in a:
        sum += i
    return sum

def sub(a:int, b:int) -> int:
    return a-b

def distancia_entre_dois_pontos(x1:int, y1: int, x2: int, y2: int) -> float:
    return ((x2-x1)**2 + (y2-y1)**2)**(1/2)

def mmc(a:int, b:int) -> int:
    x = a
    y = b
    while a != b:
        if a > b:
            b += y
        else:
            a += x
    return a

def mdc(a:int, b:int) -> int:
    x = a
    y = b
    while a != b:
        if a > b:
            a -= b
        else:
            b -= a
    return a

def eh_primo(n: int) -> bool:
    if n < 2:
        return False
    for i in range(2, int(n**0.5) + 1):
        if n % i == 0:
            return False
    return True

def celsius_para_fahrenheit(celsius: float) -> float:
    return (celsius * 9/5) + 32

def fahrenheit_para_celsius(fahrenheit: float) -> float:
    return (fahrenheit - 32) * 5/9

def fibonacci(n: int) -> list:
    seq = [0, 1]
    while len(seq) < n:
        seq.append(seq[-1] + seq[-2])
    return seq

if __name__ == "__main__":
    server = Server(5050)
    server.registerFunction(add)
    server.registerFunction(sub)    
    server.registerFunction(distancia_entre_dois_pontos)
    server.registerFunction(mmc)
    server.registerFunction(mdc)
    server.registerFunction(eh_primo)
    server.registerFunction(celsius_para_fahrenheit)
    server.registerFunction(fahrenheit_para_celsius)
    server.registerFunction(fibonacci)
    server.start()
