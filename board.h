#ifndef gomoku_board
#define gomoku_board

#include <utility>
#include <algorithm>
#include <vector>
#include <string>
#include <iostream>
#include <cmath>
#include <set>
#include <cstring>
#include <ctime>
#include <chrono>
#include <random>
#include <atomic>
#include "tbb/concurrent_unordered_map.h"


typedef unsigned long long ull;
typedef unsigned char uchar;
#define BOARD_SZ 64
#define ROWS 8
#define COLS 8
#define MAX_DEPTH 5
#define MAX_SCORE 100000
#define SQUARE_RADIUS 1

typedef struct t {
	bool forcing;
	int p_length;
	int p_weight;
	int p; //patern itself using bitmask
} pattern;

class board {
public:
	ull hash_val = 0;
	int board_score = 0; //define positive score as good for black and vice-versa
	char b[8][8];
	short visited[8][8]; //how many pieces are affecting said square
	//where the potential moves are stored
	std::set<int, std::greater<int>> move_list;
	int num_pieces[2] = { 0,0 };
	//construct class by passing it a board
	board(std::string str_board);
	int get_score_in_line(int cor_x, int cor_y, std::pair<int, int> move, int p_length, bool diagonal);
	int get_cor_score(int cor_x, int cor_y);
	void score_change(int move_x, int move_y, char piece, bool undo);
	void make_move(int move_x, int move_y, char piece);
	void undo_move(int move_x, int move_y, char piece, bool prev_score, int score);
	void print_board();
	std::string get_string();
};

void add_pattern(std::string pattern, int pattern_weight, bool force);
//checks if the coordinates are within the board
bool in_board(int x, int y);
void preprocessing();

//idea is to give higher weights to center squares when processing
extern int weight_to_square[ROWS * COLS + 1][2];
extern int square_weight[ROWS][COLS];
extern std::vector<std::pair<int, int>> movement;
extern bool piece_to_bool[256];
extern char pieces[2];
#endif
