#include <stdio.h>
#include <string.h>  
#include <stdlib.h>
#include <errno.h>
#include <unistd.h>   
#include <arpa/inet.h>    
#include <sys/types.h>
#include <sys/socket.h>
#include <netinet/in.h>
#include <sys/time.h>

#define TRUE   1
#define PORT 5500

int main(int argc , char *argv[])
{
    int opt = TRUE;
    int master_sock , addrlen , new_sock , client_sock[30] ,
            maximum_clients = 30 , act, i , value_read , sock_descriptor;
    int maximum_socket_descriptor;
    struct sockaddr_in adr{};

    char buff[1025];  //data buffer of 1K
    fd_set readfds; //set of socket file descriptors
    char *message = "ECHO Daemon v1.0 \\r\\n"; //message
    
    for (i = 0; i < maximum_clients; i++) //initialise all client_sock to 0 
    {
        client_sock[i] = 0;
    }
    if( (master_sock = socket(AF_INET , SOCK_STREAM , 0)) == 0) //creating a master socket 
    {
        perror("Failed_Socket");
        exit(EXIT_FAILURE);
    }

    //These are the types of sockets that we have created
    adr.sin_family = AF_INET;
    //adr.sin_addr.s_addr = INADDR_ANY
    adr.sin_addr.s_addr = inet_addr("192.168.119.239");
    //adr.sin_addr.s_addr = inet_addr("127.0.0.1");
    adr.sin_port = htons( PORT );
    
    if (bind(master_sock, (struct sockaddr *)&adr, sizeof(adr))<0) //bind the socket to localhost port 5500
    {
        perror("Failed_Bind");
        exit(EXIT_FAILURE);
    }
    printf("Port having listener:  %d \\n", PORT);
    
    if (listen(master_sock, 3) < 0) //Specify 3 as maximum pending connections for master socket
    {
        perror("listen");
        exit(EXIT_FAILURE);
    }
    
    addrlen = sizeof(adr); //Accepting the Incoming Connection 
    puts("Looking For Connections");
    
    //*******************************//
    // Here we start using select functions and the macros for multiple client handling
    
    while(TRUE)
    {
        FD_ZERO(&readfds); //Clearing the socket set
        FD_SET(master_sock, &readfds); //Adding the master socket to the set 
        maximum_socket_descriptor = master_sock;
        
        for ( i = 0 ; i < maximum_clients ; i++) //Adding child sockets to set 
        {
            sock_descriptor = client_sock[i]; //Descriptor for Socket 
            
            if(sock_descriptor > 0) //if the socket descriptor is valid then adding it to the read list 
                FD_SET( sock_descriptor , &readfds);

            if(sock_descriptor > maximum_socket_descriptor) //Highest File Descriptor Number which is needed for the select function 
                maximum_socket_descriptor = sock_descriptor;
        }

        //Waiting for something to happen on the master socket. As the wait time is NULL the wait is indefinite
        act = select( maximum_socket_descriptor + 1 , &readfds , nullptr , nullptr , nullptr);

        if ((act < 0) && (errno!=EINTR))
        {
            printf("Failed_Select");
        }
        if (FD_ISSET(master_sock, &readfds)) //Any activity on the master socket is treated as an incoming connection
        {
            if ((new_sock = accept(master_sock,
                                     (struct sockaddr *)&adr, (socklen_t*)&addrlen))<0)
            {
                perror("Accept!");
                exit(EXIT_FAILURE);
            }

            //Informing the user of the socket number which will be sued to send and receive messages
            printf("This is a New Connection,The socket file descriptor is %d and the IP is : %s on Port : %d\\n"
                   , new_sock , inet_ntoa(adr.sin_addr) , ntohs
                    (adr.sin_port));

            if( send(new_sock, message, strlen(message), 0) != strlen(message)) // Sending Greeting Message on New Connection
            {
                perror("Send!!");
            }
            puts("Welcome Text Sent Affirmative.");

            for (i = 0; i < maximum_clients; i++) // Adding new socket to the array of sockets
            {
                if( client_sock[i] == 0 ) // Checking if the position is empty
                {
                    client_sock[i] = new_sock;
                    printf("Adding new socket to the list of sockets as %d\\n" , i);

                    break;
                }
            }
        }
        for (i = 0; i < maximum_clients; i++) //If not the master socket then it is some i/o activity on some other socket
        {
            sock_descriptor = client_sock[i];
            if (FD_ISSET( sock_descriptor , &readfds))
            {
                //Checking if the activity was for closing and reading the incoming message
                if ((value_read = read( sock_descriptor , buff, 1024)) == 0)
                {
                    //If someone disconnected, getting their details and printing a message
                    getpeername(sock_descriptor , (struct sockaddr*)&adr ,(socklen_t*)&addrlen);
                    printf("Disconnected Host. Their , IP %s and PORT %d \\n" ,
                           inet_ntoa(adr.sin_addr) , ntohs(adr.sin_port));
                    close( sock_descriptor ); //Closing the socket and marking it as 0 in the list to be reused
                    client_sock[i] = 0;
                }
                else //Echoing back the message that came in the socket
                {
                    buff[value_read] = '\\0'; //Setting the string terminating NULL byte on the end of the data that is read
                    send(sock_descriptor , buff , strlen(buff) , 0 );
                }
            }
        }
    }
    return 0;
}