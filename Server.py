#!/usr/bin/env python3
import socket
import select

def evaluateQuery(query):
    return str(eval(query))

SERVER_HOST = '127.0.0.1'  #   Use 0.0.0.0 for any network interface
SERVER_PORT = 15112        # Port to listen on (non-privileged ports are > 1023)
empty = {}

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# not necessary, for convenience
server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
server_socket.bind((SERVER_HOST, SERVER_PORT))

server_socket.setblocking(False)
server_socket.settimeout(5)

server_socket.listen(1)



print('Listening on port %s ...' % SERVER_PORT)

   # Wait for client connections

watched_sockets = [server_socket]


while True:
    # ready to send and receive messages
    read_sockets, _, _ = select.select(watched_sockets, [], [] )
    for s in read_sockets:
        if s == server_socket:
            conn, addr = s.accept()
            watched_sockets.append(conn)
            print('Connected to', addr)
        else:
            data = s.recv(1024) #receiving from my client socket #which is a dictionary
            if len(data) > 0:
                msg = data.decode('utf-8')
                msgD = eval(msg)
                print("received this from", s, msgD)
                
                if msgD["type"] == "emotion":
                    if msgD['emotion'] in empty: #already contains the emotion
                        
                        empty[msgD['emotion']].append(s) #appends the new addr of client
                    else:
                        empty[msgD['emotion']] = [s] #sets a new list containg the address
                    
#                     print('Looking for', msgD["emotion"])
                    
                elif msgD["type"] == "msg":
                    
                    emotionofPerson = msgD['emotion']
                    for keys in empty:
                        if keys == emotionofPerson:
                            for sockett in empty[emotionofPerson]: #the list of addresses
                                if sockett != s:
                                    print("sending this to", sockett, msgD["msg"])
                                    print(msgD["msg"])
                                    #print(sockett)
                                    print("before", msgD["msg"])
                                    y = str(msgD["msg"])
                                    print(y, "y here")
                                    y = y.encode()
                                    print(y, "here now")
                                    sockett.send(y)
                                
                    
                    
#                     print('Sending a message to', msgD["emotion"], 'saying:', msgD["msg"])
                    
#                 if msgD["type"] != "emotion":   
#                     print("Got msg ", msg)
#                     #res = evaluateQuery(msg)
#                     msg = "RESULT " + msg
#                     s.sendall(msg.encode())
            else:
                break

conn.close()