import socket
import threading

# Choosing Nickname
nickname = input("Choose your nickname: ") # введите никнейм


# Connecting To Server
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # создание сокета клиента
client.connect(('127.0.0.1', 55555)) # подключение к серверу по айпи и порту

# Listening to Server and Sending Nickname
def receive():
    while True:
        try: # бесконечный цикл который ждёт сообщения от пользователя 
            # Receive Message From Server
            # If 'NICK' Send Nickname
            message = client.recv(1024).decode() # соообщение пользователя клиент принимает сообщение от сервера 
            if message == 'NICK': 
                client.send(nickname.encode())
            else:
                print(message)

           

        except:
            # Close Connection When Error
            print("An error occured!")
            client.close()
            break

def write():
    while True:
        # message = '{}: {}'.format(nickname, input(''))
        message = '{}'.format(input(''))
        client.send(message.encode())

# Starting Threads For Listening And Writing
receive_thread = threading.Thread(target=receive) # создается поток , внем ожидается сообщение от других клиентов 
receive_thread.start()

write_thread = threading.Thread(target=write) # создается поток который будет отправлять сообщение на сервер 
write_thread.start()