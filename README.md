Author: Justin Angra
Date: 12/1/2015

The application is run as expected. By first running the server_bb.py script (specifically on beta.cse.ohio-state.edu), you may start the server and prepare it for any incoming connection. By then running the client_bb.py script, you can connect to the server.

After connecting to the server, you user will be prompted for their username, which must be unique to the application. The user is then asked which group they would like to join. After this, the user is prompted with the help menu and is then able to proceed with posting and reading messages. 

Please do not attempt to rush any of the sockets, as some have timeouts of 2.5second in order to properly organized data being sent from the server due to post from other users or users join/leaving the group. 


Intructions are as follows:

type "-h" for help menu
type "-p" to post a message. A prompt will following asking for your subject and message itself
type "-r" to read the contents of a message. A prompt will follow asking for the message ID of the message you wish to read.
type "-q" to leave the group. You may reconnect if you wish to change your username or join another group.
type "-u" to received the lastest posts from your group 

Important: It is wise to update posts (use "-u") immediately prior to using any other command, however it is no necessary. If not used prior to each command, new posts will show directly after executing command, but prior to finishing the command. 

Note: I did not read the "Hint" section of the handout until the day the project was due. Thus my user instructions unfortunately differ. My apologies for any confusion this may cause. 

