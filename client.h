#ifndef client_header
#define client_header

#include <iostream>
#include <string>
#include <vector>
#include <thread>
#include <sys/socket.h>
#include <netinet/in.h>
#include <stdlib.h>
#include <unistd.h>
#include <chrono>
#include <cstring>
#include "ai.h"

#define WELCOME_MESSAGE "Meow"
#define DISCONNECT_MESSAGE "Woof"

//maximum size of message that can be sent back and forth
#define buffer_sz 256
#define PORT 5050

class client{
    private:
    int client_id, conn, CORE_CNT;
    char buffer[buffer_sz] = {0};
    char send_buffer[buffer_sz] = {0};
    void connection_thread();
    ai* client_ai;
    public:
    client(int c_id, int connection, int cores);
    void get_move();
    ~client();
};

#endif