# -*- coding: utf-8 -*-
"""
    Bulletin Board: Server
    @author: Jusin Angra
    @date: Wed Nov. 25, 2015
"""
import socket
import threading
from time import gmtime, strftime

user_list = [] #[client socket, username, group]
message_list = [] #[message ID, sender, post date, subject, group]
message_contents = {} #{message ID:contents}
message_id = 1234

bind_ip = "0.0.0.0"
bind_port = 9990

server = socket.socket(socket.AF_INET,socket.SOCK_STREAM)

server.bind((bind_ip, bind_port))

server.listen(5)

print "[*] Listening on %s:%d" % (bind_ip,bind_port)

#create function to perform necessary actions when client joins
def join_client(client_socket):
    
    #prompt client for username
    client_socket.send("Please enter your username: ")    
    
    #print out client username
    usrname = client_socket.recv(1024).lower()
    
    #check if username is already taken
    i,j = 0,1
    while i<j:
        for sublist in user_list:
            if sublist[1] == usrname:
                client_socket.send("NU") #send a not-unique flag to client to prepare for retry of username
                client_socket.send("Sorry, that username is already taken. Please enter another username: ")
                usrname = client_socket.recv(1024)
                j+=1
        i+=1

    #send acknoledgment that username is unique
    client_socket.send("ACK")
    
    #add socket addr and username to list of current connected users 
    user_list.append([client_socket,usrname])
    
    print "[*] Received user: %s" % usrname

    #prompt user for a choice of groups
    client_socket.send("""\n\nPlease choose one of the following groups:
    group1
    group2
    group3
    group4
    group5""")
    
    #append choice to user_list
    group_choice = client_socket.recv(1024)
    user_list[len(user_list)-1].append(group_choice)

    #send 'user joined' message to all users
    for i in xrange (len(user_list)):
        if user_list[i][2] == group_choice:
            user_list[i][0].send("   ")
            user_list[i][0].send("\n\nUser " + usrname + " has joined the group (" + strftime("%a, %d %b %Y %H:%M:%S +0000", gmtime()) + ")\n\n")

    #send list of current users to new user
    client_socket.send("\nThe following users are in this group: ")
    for sublist in user_list:
        if sublist[2] == group_choice:
            client_socket.send("   ")
            client_socket.send(sublist[1] + " ")

    #send ack that all users sent
    client_socket.send("  ")

    #send last two posts to user
    if len(message_list) == 0 :
        pass
    elif len(message_list) == 1 :
        #send first/last message post only if in same group
	if message_list[0][4] == group_choice:
            client_socket.send("""
            Message ID: """ + str(message_list[0][0]) + """
            Sender: """ + message_list[0][1] + """
            Post Date: """ + message_list[0][2] + """
            Subject: """ + message_list[0][3] + """
            """)
    else:
        #find positions in message lists of all group posts for posts in users group
        posts=[]
        for i in xrange (len(message_list)):
            if message_list[i][4] == group_choice:
                posts.append(i)

        if len(posts) == 1: #only one post in the same group as user   
            client_socket.send("""
            Message ID: """ + str(message_list[posts[len(posts)-1]][0]) + """
            Sender: """ + message_list[posts[len(posts)-1]][1] + """
            Post Date: """ + message_list[posts[len(posts)-1]][2] + """
            Subject: """ + message_list[posts[len(posts)-1]][3] + """
            """)        

	if len(posts) > 1 :         
            #send last two values in group posts list
            client_socket.send("""
            Message ID: """ + str(message_list[posts[len(posts)-2]][0]) + """
            Sender: """ + message_list[posts[len(posts)-2]][1] + """
            Post Date: """ + message_list[posts[len(posts)-2]][2] + """
            Subject: """ + message_list[posts[len(posts)-2]][3] + """
            """)
        
            client_socket.send("""
            Message ID: """ + str(message_list[posts[len(posts)-1]][0]) + """
            Sender: """ + message_list[posts[len(posts)-1]][1] + """
            Post Date: """ + message_list[posts[len(posts)-1]][2] + """
            Subject: """ + message_list[posts[len(posts)-1]][3] + """
            """)


def help_menu(client_socket):
    client_socket.send("""
    -h : get help menu 
    -p : post message to the group
    -r : request contents of a message
    -q : leave the group 
    -u : update with any new posts from other users \n\n
    """)

def post_message(client_socket):
    
    #user prompted for subject
    client_socket.send("\n\nEnter a subject for your post: ")
    subject = client_socket.recv(1024)
    
    #user prompted for content
    client_socket.send("\n\nEnter the contents of your post: ")
    contents =  client_socket.recv(2048)
    
    #increment message_id
    new_id = message_id + len(message_list)
    
    #sender looked up via client_socket
    for sublist in user_list:
        if sublist[0] == client_socket:
            sender = sublist[1]
            group = sublist[2]

    #get current time in GMT
    post_date = strftime("%a, %d %b %Y %H:%M:%S +0000", gmtime())   
    
    #post appended to message_list
    message_list.append([new_id,sender,post_date,subject,group])
    
    #message ID and contents added to message_contents dict
    message_contents[new_id] = contents
    
    #notify all users of newly posted message
    for sublist in user_list:
        if sublist[2] == group:
            sublist[0].send("   ")
            sublist[0].send("""
            Message ID: """ + str(new_id) + """
            Sender: """ + sender + """
            Post Date: """ + post_date + """
            Subject: """ + subject + """
            """)
    client_socket.send("  ") #send ack that all users were notified
    
def request_contents(client_socket):
    
    #user prompted for message ID
    client_socket.send("\nEnter the message ID of the post you wish to read: ")
    request_id = int(client_socket.recv(1024))
    
    #messaged found using message_contents dict 
    if request_id in message_contents:
        requested_contents = message_contents[request_id]
        
        #message sent over client_socket  
        client_socket.send("\n" + requested_contents)
        
    else:
        client_socket.send("\nThere is no message with that ID value")
    
def leave_group(client_socket):
    
    usrname = "tmp"
    group = "tmp"
    #client removed from user_list
    for i in xrange (len(user_list)-1):
        if user_list[i][0] == client_socket:
            usrname = user_list[i][1]
            group = user_list[i][2]
            print "[*] User left: " + usrname 
            del user_list[i]
    
    #send a notification to all other users 
    for sublist in user_list:
        if sublist[2] == group:
            sublist[0].send("   ")
            sublist[0].send("\nUser " + usrname + " has left the group")
    client_socket.send("  ") #send ack that all users notified 
    
    #connection to client closed
    client_socket.close()

#create function to handle each client thread
def handle_client(client_socket):
    
    join_client(client_socket)       
    
    client_socket.send("\n\nWelcome to the group, please read our help menu below prior to posting")
    
    #send help menu
    help_menu(client_socket)
    
    #loops until client leaves
    while True:
        request = client_socket.recv(1024)
        if request == "-h": #help menu
             help_menu(client_socket)
        elif request == "-p": #post message**********
            post_message(client_socket)
        elif request == "-r": #request message contents***********
            request_contents(client_socket)
        elif request == "-q": #leave group
            leave_group(client_socket)
            break
	elif request == "-u":
	    continue 
        else:
            help_menu(client_socket)
           
    
#loop server to listen forever    
while True:
    
    client,addr = server.accept()
    
    print "[*] Accepted connection from: %s:%d" % (addr[0],addr[1])
    
    #start client thread to handle incoming data
    client_handler = threading.Thread(target=handle_client,args=(client,))
    client_handler.start()
