#include <iostream>
#include <fstream>
#include <string>
#include <cmath>
#include "ai.h"

const int CORE_CNT = 24;

std::string test_board_dir = "test_boards/";

std::string get_test_board(std::string board_name) {
	std::string board_str = "";
	std::ifstream boardfile;
	boardfile.open(test_board_dir + board_name + ".txt");
	std::string line;
	if (boardfile.is_open()) {
		while(getline(boardfile, line)) board_str += line;
	}
	else {
		std::cout << "ERROR OPENING FILE " << board_name << '\n';
	}
	return board_str;
}

void play_against(bool player_black) {

	board play_board = board(get_test_board("board1"));
	ai* test_ai = new ai(CORE_CNT);	
	bool black_turn = true;
	char piece = 'B';
	while (abs(play_board.board_score) < 85000) {

		play_board.print_board();

		if (black_turn == player_black) {
			std::cout << "ENTER MOVE: ";
			int move_x, move_y;
			std::cin >> move_x >> move_y;
			play_board.make_move(move_x, move_y, piece);
		}
		else {
			std::pair<int, int> comp_move = get_best_move(&play_board, 4, test_ai);
			play_board.make_move(comp_move.first, comp_move.second, piece);
			clear_table(test_ai);
		}
		black_turn = !black_turn;
		if (piece == 'B') piece = 'W';
		else piece = 'B';

	}

	play_board.print_board();
	if (black_turn) {
		std::cout << "WHITE WINS!" << '\n';
	}
	else {
		std::cout << "BLACK WINS!" << '\n';
	}

	system("pause");
}

int main() {
	preprocessing();
	/*
	while(true){
		play_against(false);
	}
	*/
	board test_board = board(get_test_board("board2"));
	test_board.print_board();
	ai* test_ai = new ai(CORE_CNT);
	
	std::pair<int, int> best_move = get_best_move(&test_board, 4, test_ai);
	std::cout << best_move.first << ' ' << best_move.second << '\n';
	
}
