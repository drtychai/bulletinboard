# -*- coding: utf-8 -*-
"""
    Bulletin Board: Client
    @author: justin
    @date: Web Nov. 25, 2015
"""

import socket
import sys

def post_checker(client_socket):
    response = client_socket.recv(8192)
    
    #check if response is "NP" for a new post from another user
    if response == "   ":
        new_response = client_socket.recv(8192)
        print new_response
    else: #print original message being sent
        print response


target_host = "beta.cse.ohio-state.edu"
target_port = 9990

#create socket object
client = socket.socket(socket.AF_INET,socket.SOCK_STREAM)

#connect the client
client.connect((target_host,target_port))

#receiving user name prompt
print client.recv(1024)

usrname = str(raw_input()) 

#send username
client.send(usrname)

#check if username was unique
while client.recv(1024) == "NU": #should exit once "ACK" received
    print client.recv(1024) #print username promt again

    usrname = str(raw_input()) #client enters in another username
    client.send(usrname)

#receive group options
post_checker(client)

#send back choice of group
group_choice = str(raw_input("$: "))
client.send(group_choice)

#receive user joined message/welcome message/help menu
post_checker(client)



#loops until client disconnects
while True:
    
    #set socket timeout
    client.settimeout(2) #2 second
    
    #see if any posts from other users are waited to been received
    while True:
        try:
            #msg = client.recv(8192)
            post_checker(client)
	    pass
        except socket.timeout, e:
            err = e.args[0]
            if err == 'timed out':
                #no new posts
                break
            else:
                print e
                sys.exit(1)
        except socket.error, e:
            # Something else happened, handle error, exit, etc.
            print e
            sys.exit(1)
    
    request = str(raw_input("\n\nWhat would you like to do? "))
    client.send(request)
    
    if request == "-h":
        
        help_menu = client.recv(4096) 
        print help_menu
        
    elif request == "-p":
        #get subject_request    
        post_checker(client) 
        
        #see if any posts from other users are waited to been received
        while True:
            try:
                #msg = client.recv(4096)
                post_checker(client)
		pass
            except socket.timeout, e:
                err = e.args[0]
                if err == 'timed out':
                    #no new posts
                    break
                else:
                    print e
                    sys.exit(1)
            except socket.error, e:
                # Something else happened, handle error, exit, etc.
                print e
                sys.exit(1)
        
        subject = str(raw_input())
        client.send(subject)
        
        #get contents_request of post
        post_checker(client)
        
        contents = str(raw_input())
        client.send(contents)
    
        #get post notification 
        post_checker(client)
        
    elif request == "-r":
        #get id value request of post 
        post_checker(client)  
        
        #see if any posts from other users are waited to been received
        while True:
            try:
                post_checker(client)
                pass
            except socket.timeout, e:
                err = e.args[0]
                if err == 'timed out':
                    #no new posts
                    break
                else:
                    print e
                    sys.exit(1)
            except socket.error, e:
                # Something else happened, handle error, exit, etc.
                print e
                sys.exit(1)
            
        message_id = str(raw_input())
        client.send(message_id)
        
        #get contents of post 
        post_checker(client)  
       
    elif request == "-q":
        break

    elif request == "-u":  #used to pass through loop once more to update posts
        continue

    else: #receive help menu
        print client.recv(1024) 
    
