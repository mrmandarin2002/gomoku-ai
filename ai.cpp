#include "ai.h"

ai::ai(int cores){
    max_core_cnt = cores;
    available_cores = cores;
    initial_threads_launched = false;
}

int mini_max(board* board_ptr, int depth, int og_depth, bool black_turn, int alpha, int beta, ai* ai_ptr) {
	if (depth == 0 || (abs(board_ptr->board_score) > 50000)) {
		if(depth == og_depth) ai_ptr->available_cores++;
		return board_ptr->board_score;
	} 
	int fuck_locks = ai_ptr->t_table[board_ptr->hash_val];
	if (fuck_locks) {
		if(depth == og_depth) ai_ptr->available_cores++;
		return fuck_locks;
	}
	
	if(ai_ptr->available_cores > 0 && depth > 2 && ai_ptr->initial_threads_launched){
		return open_new_threads(board_ptr, depth, black_turn, alpha, beta, ai_ptr);
	}

	int cur_score = board_ptr->board_score;
	char piece = (black_turn ? 'B' : 'W');
	int maximize = (black_turn ? -1e9 : 1e9);
	std::vector<int> moves_list(board_ptr->move_list.begin(), board_ptr->move_list.end());
	if (black_turn) {
		for (int weight : moves_list) {
			int square_x = weight_to_square[weight][0];
			int square_y = weight_to_square[weight][1];
			board_ptr->make_move(square_x, square_y, piece);
			maximize = std::max(maximize, mini_max(board_ptr, depth - 1, og_depth, !black_turn, alpha, beta, ai_ptr));
			alpha = std::max(alpha, maximize);
			board_ptr->undo_move(square_x, square_y, piece, true, cur_score);
			if (beta <= alpha) {
				if (depth == og_depth) ai_ptr->available_cores++;
				return maximize;
			}
		}
	}
	else {
		for (int weight : moves_list) {
			int square_x = weight_to_square[weight][0];
			int square_y = weight_to_square[weight][1];
			board_ptr->make_move(square_x, square_y, piece);
			maximize = std::min(maximize, mini_max(board_ptr, depth - 1, og_depth, !black_turn, alpha, beta, ai_ptr));
			beta = std::min(beta, maximize);
			board_ptr->undo_move(square_x, square_y, piece, true, cur_score);
			if (beta <= alpha){
				if (depth == og_depth) ai_ptr->available_cores++;
				return maximize;
			} 
		}
	}

	ai_ptr->t_table[board_ptr->hash_val] = maximize;
	if(depth == og_depth) ai_ptr->available_cores++;
	return maximize;
}

// when program detects that cores are available this function will launch and will
// use the extra cores to compute branches
int open_new_threads(board* board_ptr, int depth, bool black_turn, int alpha, int beta, ai* ai_ptr){
	//std::cout << "CREATING NEW THREADS" << '\n';
	std::vector<std::future<int>> future_scores;
	std::string board_string = board_ptr->get_string();
	ai_ptr->initial_threads_launched = false;
	for(int weight : board_ptr->move_list){
		int square_x = weight_to_square[weight][0];
		int square_y = weight_to_square[weight][1];
		board* temp_board = new board(board_string);
		temp_board->make_move(square_x, square_y, pieces[black_turn]);
		ai_ptr->available_cores--;
		future_scores.push_back(std::async(std::launch::async, mini_max, temp_board, depth - 1, depth - 1, !black_turn, alpha, beta, ai_ptr));
	}
	ai_ptr->initial_threads_launched = true;

    //gets maximum score
    int maximize = (black_turn ? -1e9 : 1e9);
	int cur_weight = 0;
	int score = 0;
	for (auto& e : future_scores) {
		score = e.get();
		if (black_turn) maximize = (score > maximize ? score : maximize);
		else maximize = (score < maximize ? score : maximize);
	}
	return maximize;
}

std::pair<int, int> get_best_move(board* board_ptr, int max_depth, ai* ai_ptr) {
	auto begin = std::chrono::high_resolution_clock::now();
	std::vector<std::pair<std::future<int>, int>> future_scores;
	char piece = 'B';
	int maximize = -1e9;
	if (board_ptr->num_pieces[0] != board_ptr->num_pieces[1]) {
		piece = 'W';
		maximize = 1e9;
	}
	int cur_weight = 0;
	int score = 0;
	std::clock_t start_main;
	start_main = std::clock();
	std::string board_string = board_ptr->get_string();
	for (int it : board_ptr->move_list) {
		int square_x = weight_to_square[it][0];
		int square_y = weight_to_square[it][1];
		board* temp_board = new board(board_string);
		temp_board->make_move(square_x, square_y, piece);
		if(abs(temp_board->board_score) > 70000 && abs(temp_board->board_score) < 170000){
			std::cout << "WON!" << '\n';
			return { square_x, square_y };
		}
		ai_ptr->available_cores--;
		future_scores.push_back({ std::async(std::launch::async, mini_max, temp_board, max_depth, max_depth, !piece_to_bool[piece], -1e9, 1e9, ai_ptr), it});
	}     
	ai_ptr->initial_threads_launched = true;
	for (auto& e : future_scores) {
		score = e.first.get();
		if (piece == 'B') {
			if (score > maximize) {
				maximize = score;
				cur_weight = e.second;
			}
		}
		else {
			if (score < maximize) {
				maximize = score;
				cur_weight = e.second;
			}
		}
		//score_board[weight_to_square[e.second][0]][weight_to_square[e.second][1]] = score;
	}
	ai_ptr->initial_threads_launched = false;
	
    /*
	for (int x = 0; x < ROWS; x++) {
		for (int y = 0; y < COLS; y++) {
			std::cout << score_board[x][y] << ' ';
		}
		std::cout << '\n';
	}
    */
	
	auto end = std::chrono::high_resolution_clock::now();
	auto elapsed = std::chrono::duration_cast<std::chrono::nanoseconds>(end - begin);
	printf("Get Move Runtime: %.3f seconds.\n", elapsed.count() * 1e-9);
	return { weight_to_square[cur_weight][0], weight_to_square[cur_weight][1] };
}

void clear_table(ai* ai_ptr) {
	ai_ptr->t_table.clear();
}