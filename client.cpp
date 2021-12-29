#include "client.h"

//constructor
client::client(int c_id, int connection, int cores) : client_id(c_id), conn(connection), CORE_CNT(cores){
    std::cout << "Successfully connected client!" << '\n';
    send(conn, WELCOME_MESSAGE, sizeof(WELCOME_MESSAGE), 0);
    std::thread client_thread(&client::connection_thread, this);
    client_ai = new ai(CORE_CNT);
    client_thread.detach();
}

void client::get_move(){
    std::string str_board = "";
    int depth = buffer[67] - '0';
    for(int x = 2; x < 66; x++){
        str_board += buffer[x];
    }
    board* client_board = new board(str_board);
    std::pair<int,int> best_move = get_best_move(client_board, depth, client_ai);
    send_buffer[0] = ('0' + best_move.first);
    send_buffer[1] = '|';
    send_buffer[2] = ('0' + best_move.second);
}


//waits for data from client
void client::connection_thread(){
    std::cout << "IN CONNECTION THREAD" << '\n';
    while(true){
        std::cout << "Waiting for data from client" << '\n';
        memset(buffer, 0, sizeof(buffer));
        memset(send_buffer, 0, sizeof(send_buffer));
        read(conn, buffer, buffer_sz);
        if(!buffer[0] || buffer[0] == 'W') {
            std::cout << "Connection with " << client_id << " is closed!" << '\n';
            close(conn);
            break;
        } else {
            //evaluate position
            if(buffer[0] == 'E'){
                get_move(); // --> puts it in the send_buffer as defined in ai.h
                send(conn, send_buffer, 3, 0);
                clear_table(client_ai);
            }
        }
    }
    std::cout << "OUT OF CONNECTION THREAD" << '\n';
}
