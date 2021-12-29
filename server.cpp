//regular imports
#include <iostream>
#include <vector>
#include <string>
#include <cmath>
#include <algorithm>

//socket related imports
#include <sys/socket.h>
#include <netinet/in.h>

//own file imports
#include "client.h"

const int NUM_OF_CORES = 24;

//wait for client connections
int main(int argc, char const *argv[]){
    preprocessing();
    std::vector<client*> clients;
    int opt = 1;
    int connected_clients = 0;

    //initializes address, half the code looks like gibberish to me
    struct sockaddr_in address;
    address.sin_family = AF_INET;
    address.sin_addr.s_addr = INADDR_ANY;
    address.sin_port = htons (PORT);
    int addrlen = sizeof(address);

    //creates the socket
    int tcp_socket = socket(AF_INET, SOCK_STREAM, 0);
    if(!tcp_socket){
        perror("socket failed");
        exit(EXIT_FAILURE);
    }

    //checks for errors or some shit idek, I think it's to avoid "address in use" type of error
    if(setsockopt(tcp_socket, SOL_SOCKET, SO_REUSEADDR | SO_REUSEPORT, &opt, sizeof(opt))){
        perror("setsockopt");
        exit(EXIT_FAILURE);
    }

    //Try to attach socket to the port 8080
    if(bind(tcp_socket, (struct sockaddr *)&address, sizeof(address)) < 0){
        perror("bind failed");
        exit(EXIT_FAILURE);
    }

    //main server loop
    while(listen(tcp_socket, 5) >= 0){
        std::cout << "WAITING FOR DEM CLIENTS BRUH" << '\n';
        int new_connection = accept(tcp_socket, (struct sockaddr *)&address, (socklen_t*)&addrlen);
        if(new_connection < 0){
            perror("accept");
        }
        std::cout << "Connection Accepted" << '\n';
        client* new_client = new client(++connected_clients, new_connection, NUM_OF_CORES);
    }
    std::cout << "WE OUT" << '\n';
    perror("listen");
    close(tcp_socket);
    return 0;
}