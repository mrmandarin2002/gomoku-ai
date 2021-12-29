#ifndef gomoku_ai
#define gomoku_ai

#include <future>
#include "board.h"

class ai{

public:
    tbb::concurrent_unordered_map<ull, int> t_table;
    std::atomic<int> available_cores;
    std::atomic<bool> initial_threads_launched;
    std::atomic<int> alpha;
    std::atomic<int> beta;
    int max_core_cnt;
    ai(int cores);

};

int mini_max(board* board_ptr, int depth, int og_depth, bool black_turn, int alpha, int beta, ai* ai_ptr);
int open_new_threads(board* board_ptr, int depth, bool black_turn, int alpha, int beta, ai* ai_ptr);
std::pair<int, int> get_best_move(board* board_ptr, int max_depth, ai* ai_ptr);
void clear_table(ai* ai_ptr);
#endif