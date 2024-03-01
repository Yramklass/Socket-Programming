from socket import *
from threading import Thread


serverName = "localhost"             # UCT : 196.47.229.247"
serverPort = 12001
clientSocket = socket(AF_INET, SOCK_STREAM)
clientSocket.connect((serverName,serverPort))


def main():
    logged_in = False
    while logged_in == False:
        username = input("Enter Username:\n")
        password = input("Enter Password:\n")
        message = "LOGIN " + "\r\n" + "USERNAME " + username + "\r\nPASSWORD " + password+ "\r\nIP NUMBER " + clientSocket.getsockname()[0] + "\r\nSOCKET NUMBER " + str(clientSocket.getsockname()[1]) + "\r\n\r\n"
        clientSocket.send(message.encode())
        returnmessage = clientSocket.recv(1024).decode()
        #Decision Tree
        returncommand = returnmessage[:returnmessage.find("\r")-1]
        reason = returnmessage[returnmessage.find("\n")+1:-5]

        if returncommand == "UNSUCCESSFUL":
            if reason == "DUPLICATE":                                                       # If user logged in already
                print("\nUser ({}) already logged into the server.\n".format(username))
            else:                                                                           # If incorrect password
                print("\nPassword incorrect.\n")
            
        else:                                                                               # If successful - logged_in = True
            if reason == "NEW":
                print ("\nNew user successfully registered.\n")
            else:
                print ("\nWelcome back {}!\n".format(username))
            logged_in = True


    
    


    while logged_in == True:
        
        print("Current User: {}\n".format(username))
        message = "GETSTATUS \r\n" + "USERNAME " + username +"\r\n\r\n"
        clientSocket.send(message.encode())
        returnmessage = clientSocket.recv(1024).decode()
        print ("Current Status: " + returnmessage[returnmessage.find("\n")+1:]) #Protocol : "STATUS \r\n userstatus\r\n\r\n"
        
    
        options = "Choose an option:\n1.) Chat\n2.) List Clients\n3.) Set Status\n4.) Exit\n"              #String of options to be displayed
 
        user_choice = (input(options))#add all options

        if user_choice == "1":                                  
            peer_username = input("Enter Peer Username:\n")
            chat(peer_username,username)            


        elif user_choice == "4":                                           #Last option
            message = message = "SETSTATUS \r\n" + "USERNAME {}\r\n".format(username) +  "OFFLINE\r\n\r\n"
            clientSocket.send(message.encode())
            exit()

     
            
        elif user_choice == "3":
            newstatus = input("What would you like to set your status to?\n1.) Available\n2.) Away\n")
            if newstatus == "1":
                message = "SETSTATUS \r\n" + "USERNAME {}\r\n".format(username) +  "AVAILABLE\r\n\r\n"
                clientSocket.send(message.encode())
                returnmessage = clientSocket.recv(1024).decode()
            elif newstatus == "2":
                message = "SETSTATUS \r\n" + "USERNAME {}\r\n".format(username) + "AWAY\r\n\r\n"
                clientSocket.send(message.encode())
                returnmessage = clientSocket.recv(1024).decode()
            else:
                print("Invalid choice.\n")

        elif user_choice == "2":
            #List clients
            message = "LIST \r\n"
            clientSocket.send(message.encode())
            returnmessage = clientSocket.recv(1024).decode()            #"LIST \r\n" + "username\rstatus\ripaddress\r\n" + ....
            returnmessage = returnmessage[returnmessage.find("\n")+1:]
            client_list = "\tLIST OF USERS:\t\nUSERNAME\t"+ "STATUS".ljust(10) + "\t\n"#+"\tIP ADDRESS".ljust(10)+"\tPORT NUMBER\t\n"      #PRIVACY CONCERN- don't display IP and Port
            while (returnmessage!="\r\n\r\n"):   
                     #while not end of the message / list
                client_list += (returnmessage[:returnmessage.find("\r")]).ljust(10)
                returnmessage = returnmessage[returnmessage.find("\r")+1:]

                client_list += "\t{}\n".format((returnmessage[:returnmessage.find("\r")]).ljust(10))
                returnmessage = returnmessage[returnmessage.find("\r")+1:]

                #client_list += "\t{}".format((returnmessage[:returnmessage.find("\r")]).ljust(10))
                returnmessage = returnmessage[returnmessage.find("\r")+1:]

                #client_list += "\t{}\n".format(returnmessage[:returnmessage.find("\r")])
                returnmessage = returnmessage[returnmessage.find("\n")+1:]
            print(client_list)
        

           

        


  

def chat(peer_username,username):

    message = "CHAT \r\nSTART\r\n{}\r\n{}\r\n\r\n".format(peer_username,username)
    clientSocket.send(message.encode())

    returnmessage = clientSocket.recv(1024).decode()    
    print(returnmessage)
    command = returnmessage[:returnmessage.find("\r")]

    if command == "BUSY":
        print("User is currently busy.\n")
    
    elif command == "OFFLINE":
        print("User is currently offline.\n")

    elif command =="AVAILABLE":
        print("User available. Initializing chat...\n")                                        #AVAILABLE\r\npeerIP\r\ndport\r\nsport\r\n\r\n
        returnmessage = returnmessage[returnmessage.find("\n")+1:]
        ip_address = returnmessage[:returnmessage.find("\r")]
        returnmessage = returnmessage[returnmessage.find("\n")+1:]
        sport = returnmessage[:returnmessage.find("\r")]   
        returnmessage = returnmessage[returnmessage.find("\n")+1:]
        dport = returnmessage[:returnmessage.find("\r")]


        dport = int(dport)
        sport = int(sport)
        print(dport)
        print(sport)

        sock = socket(AF_INET, SOCK_DGRAM)  
        sock.bind(('0.0.0.0', sport))
        sock.sendto(b'0',(ip_address,dport))

          
        def listen():
            sock = socket(AF_INET, SOCK_DGRAM)
            sock.bind(('0.0.0.0', sport))
            while True:
                data = sock.recv(1024)
                print('\rpeer: {}\n> '.format(data.decode()), end='')


        listener = Thread(target=listen, daemon=True)
        listener.start()

        sock = socket(AF_INET, SOCK_DGRAM)
        sock.bind(('0.0.0.0', dport))

        while True:
            msg = input('> ')
            sock.sendto(msg.encode(), (ip_address, sport))
            
if __name__ == "__main__":
    main()