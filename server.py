#!/bin/python3
import socket
import threading
import time
import random

# Connection Data
host = '127.0.0.1' ## ip server 
port = 55555 # port srever

# Starting Server
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # создание сокета
server.bind((host, port)) # дополнение  сокет айпи и порта 
server.listen() # сокет в статусе лиен говорит о том что наш сервер слушает эфир и готов к ринятию сообщений

# Lists For Clients and Their Nicknames
clients = [] # массив клиентов  
nicknames = [] # массив никнеймов клиентов 

# Sending Messages To All Connected Clients
def broadcast(message): # функция передачи сообщения всем клиентам 
    for client in clients: # проходит по каждоуму клинту из массива 
        client.send(message) # отправляет сообщение 

# Handling Messages From Clients
def handle(client): # весит на клиенте и ждёт сообщение от клиента (бесконечный цикл)
    while True:
        try: # если сообщение получено отправляем его всем клиентам с помощью ф-ии broadcast(message)
            # Broadcasting Messages
            index = clients.index(client) # находим индекс выбовшего клиента 
            nickname = nicknames[index] # получаем его никнейм по индексу

            message = client.recv(1024).decode() # так как мы не знаем обьем сообщения от клиента мы будем принимать пакеты данных по 
            message = f"{nickname}: {message}".encode()
            print(message.decode())

# ---------------------------------------------------------------------------------------
            # команда АДминистратора(admin) на вывод всех пользователя 
            if message.decode() == "admin: all users" : 
                mes = ''
                for i in range(len(nicknames)) :
                    mes =  mes + (f"{nicknames[i]} - {clients[i].getpeername()}\n")
                client.send(mes.encode()) 
            else:
                broadcast(message) # и отправлять всем клиентам 
# ---------------------------------------------------------------------------------------

        except: # в случае если кто то вышел из чата возникает ошибка так как broadcast(message) не может отправить сообщение , для этого описан ниже код 
            # Removing And Closing Clients
            index = clients.index(client) # находим индекс выбовшего клиента 
            clients.remove(client) # удаляем его из массива
            client.close() # закрываем для него соединениие 
            nickname = nicknames[index] # получаем его никнейм по индексу
            broadcast('{} left!'.format(nickname).encode()) 
            nicknames.remove(nickname) # удаляем никнейм из массива 
            break

# Receiving / Listening Function
def receive(): # основная ф-я которая запускает программу 
    while True: #бесконечный цикл ждём клиентов которые подсоеденяются 
        # Accept Connection 
        client, address = server.accept() #после успешного подсоеденения клиента получаем данные
        print("Connected with {}".format(str(address))) # в лог пиштся о подключение клиента с айпи адресом 

        # Request And Store Nickname
        client.send('NICK'.encode()) # отправляется сообщение клиенту с просьбой ввести ник 
        
        nickname = client.recv(1024).decode() #клиент принимает  сообщение  с ником , оно разбивается на пакеты в 1024 б и записывается в кодировке ascii

        if nickname not in nicknames : 
                nicknames.append(nickname) # в массив никнеймов записывается новый никнейм 
                clients.append(client) #  в массив клиентов записыфвается новый айпи адрес 

                    # Print And Broadcast Nickname
                print("Nickname is {}".format(nickname))  # в лог записывается что зашёл человек с никнеймом ...
                broadcast("{} joined!".format(nickname).encode()) # оповещение всем пользователем о присоединение 
                client.send('Connected to server!'.encode()) # отправка сообщения клиенту о успешном присоеденение 

        else:
                client.send("Nickname is {} уже есть !!!".format(nickname).encode())  
                print("{} - Error Nickname".format(str(address)))
                nicknameA = f"anonimus-{random.randint(0, 100)}"
                client.send("Ваш Nickname is {} ".format(nicknameA).encode()) 
                
                nicknames.append(nicknameA) # в массив никнеймов записывается новый никнейм 
                clients.append(client) #  в массив клиентов записыфвается новый айпи адрес 

                    # Print And Broadcast Nickname
                print("Nickname is {}".format(nicknameA))  # в лог записывается что зашёл человек с никнеймом ...
                broadcast("{} joined!".format(nicknameA).encode()) # оповещение всем пользователем о присоединение 
                client.send('Connected to server!'.encode()) # отправка сообщения клиенту о успешном присоеденение 


        # Start Handling Thread For Client
        thread = threading.Thread(target=handle, args=(client,)) # на каждого клиента создается поток внутри которого запускается функция handle (которая ждёт сообщение от клиента) .
                                 #args=(client,) - клиенту привязана ф-ия target=handle
        thread.start() # поток стартует 

print("Server if listening...")
receive()
# Убрал привязку к кодировке (Теперь можно вводить никнейм и сообщения по русски )