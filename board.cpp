//where the ai magic happens
#include "board.h"

//idea is to give higher weights to center squares when processing
std::vector<int> surrounding_squares[ROWS * COLS];
int weight_to_square[ROWS * COLS + 1][2];
int square_weight[ROWS][COLS];
std::vector<std::pair<int, int>> movement;
std::vector<pattern> threat_patterns[8];
int threat_weight[10][256]; 
int min_pat_sz = 1e9;
int max_pat_sz = 0;
bool piece_to_bool[256];
char pieces[2] = {'W', 'B'};
tbb::concurrent_unordered_map<ull, int> s_table;

ull zobrist_table[8][8][2];
std::mt19937 mt(01234567);

ull randomInt()
{
	std::uniform_int_distribution<ull>dist(0, UINT64_MAX);
	return dist(mt);
}

void add_pattern(std::string pat, int pattern_weight, bool force) {
	pattern temp_pat;
	temp_pat.p = 0;
	for (int x = 0; x < pat.size(); x++) {
		temp_pat.p = temp_pat.p << 1;
		if (pat[x] == 'X') {
			temp_pat.p += 1;
		}
	}
	temp_pat.p_length = pat.size();
	threat_weight[temp_pat.p_length][temp_pat.p] = pattern_weight;
	min_pat_sz = std::min(min_pat_sz, temp_pat.p_length);
	max_pat_sz = std::max(max_pat_sz, temp_pat.p_length);
	temp_pat.p_weight = pattern_weight;
	temp_pat.forcing = force;
	threat_patterns[temp_pat.p_length].push_back(temp_pat);
}

bool in_board(int x, int y) {
	if (x >= 0 && x < ROWS && y >= 0 && y < COLS) return true;
	return false;
}

//fill the pattern vector
void fill_patterns() {
	//forcing patterns
	add_pattern("XXXXXX", -2000000, true);
	add_pattern("XXXXX", 1000000, true);
	add_pattern(".XXXX.", 10000, true);
	add_pattern("XXXX.", 900, true);
	add_pattern("XXX.X", 1100, true);
	add_pattern("XX.XX", 1100, true);
	add_pattern("X.XXX", 1100, true);
	add_pattern(".XXXX", 900, true);

	//non-forcing patterns
	add_pattern(".XXX.", 400, false);
	add_pattern(".XXX", 300, false);
	add_pattern("XXX.", 300, false);
	add_pattern(".XX.X.", 700, false);
	add_pattern(".X.XX.", 700, false);
}

void preprocessing() {
	piece_to_bool['B'] = true;
	piece_to_bool['W'] = false;
	memset(threat_weight, 0, sizeof(threat_weight));
	fill_patterns();
	movement.push_back({ 0, 1 });
	movement.push_back({ 1, 0 });
	movement.push_back({ 0, -1 });
	movement.push_back({ -1, 0 });

	int weight = 64;

	for (int i = 0; i < 8; i++)
		for (int j = 0; j < 8; j++)
			for (int k = 0; k < 2; k++) {
				zobrist_table[i][j][k] = randomInt();
				//std::cout << zobrist_table[i][j][k] << '\n';
			}

	for (int i = 3; i >= 0; i--) {
		int start_x = i, start_y = i;
		for (int x = 0; x < (4 - i) * 4 + (4 - i - 1) * 4; x++) {
			start_x += movement[x / ((3 - i) * 2 + 1)].first;
			start_y += movement[x / ((3 - i) * 2 + 1)].second;
			square_weight[start_x][start_y] = weight;
			weight_to_square[weight][0] = start_x;
			weight_to_square[weight][1] = start_y;
			weight--;
		}
	}

	for (int x = 0; x < 8; x++) {
		for (int y = 0; y < 8; y++) {
			for (int cor_x = -SQUARE_RADIUS; cor_x <= SQUARE_RADIUS; cor_x++) {
				for (int cor_y = -SQUARE_RADIUS; cor_y <= SQUARE_RADIUS; cor_y++) {
					int cur_x = x + cor_x;
					int cur_y = y + cor_y;
					if (in_board(cur_x, cur_y) && !(cur_x == x && cur_y == y)) {
						surrounding_squares[x * ROWS + y].push_back(square_weight[cur_x][cur_y]);
					}
				}
			}
		}
	}
}

//constructor
board::board(std::string str_board) {
	memset(visited, 0, sizeof(visited));
	memset(b, 0x2E, sizeof(b)); //initialize everything with '.'
	char cur_char;
	for (int x = 0; x < ROWS; x++) {
		for (int y = 0; y < COLS; y++) {
			cur_char = str_board[x * 8 + y];
			if (cur_char != '.') {
				num_pieces[piece_to_bool[cur_char]];
				make_move(x, y, cur_char);
			}
		}
	}
}

std::string board::get_string() {
	std::string temp_string = "";
	for (int x = 0; x < ROWS; x++) {
		for (int y = 0; y < COLS; y++) {
			temp_string += b[x][y];
		}
	}
	return temp_string;
}

int board::get_score_in_line(int cor_x, int cor_y, std::pair<int, int> move, int p_length, bool diagonal) {
	int white_overlay = 0, black_overlay = 0, start_x = 0, start_y = 0, cur_x = 0, cur_y = 0;
	if (!diagonal) {
		start_x = std::max(0, cor_x - (move.first * (p_length - 1)));
		start_y = std::max(0, cor_y - (move.second * (p_length - 1)));
	}
	else {
		start_x = cor_x - (move.first * (p_length - 1));
		start_y = cor_y - (move.second * (p_length - 1));
		while (!in_board(start_x, start_y)) {
			start_x += move.first;
			start_y += move.second;
		}
	}
	int black_pieces = 0;
	int white_pieces = 0;
	int cur_score = 0;
	cur_x = start_x;
	cur_y = start_y;
	for (int i = 0; i < p_length; i++) {
		if (!in_board(cur_x, cur_y)) {
			return 0;
		}
		black_overlay = black_overlay << 1;
		white_overlay = white_overlay << 1;
		if (b[cur_x][cur_y] == 'B') {
			black_overlay += 1;
			black_pieces++;
		}
		else if (b[cur_x][cur_y] == 'W') {
			white_overlay += 1;
			white_pieces++;
		}
		cur_x += move.first;
		cur_y += move.second;
	}

	for (int i = 0; i < p_length; i++) {
		//beautiful code, literally made me cum when the timer went down from 300s to 1.6s
		if (!black_pieces) {
			cur_score -= threat_weight[p_length][white_overlay];
		}
		else if (!white_pieces) {
			cur_score += threat_weight[p_length][black_overlay];
		}

		if (i != p_length - 1) {
			if (abs(cor_x - cur_x) >= p_length || abs(cor_y - cur_y) >= p_length || !in_board(cur_x, cur_y)) break;
			if (b[start_x][start_y] == 'B') {
				black_overlay -= (1 << (p_length - 1));
				black_pieces--;
			}
			else if (b[start_x][start_y] == 'W') {
				white_overlay -= (1 << (p_length - 1));
				white_pieces--;
			}

			black_overlay = black_overlay << 1;
			white_overlay = white_overlay << 1;
			if (b[cur_x][cur_y] == 'B') {
				black_overlay += 1;
				black_pieces++;
			}
			else if (b[cur_x][cur_y] == 'W') {
				white_overlay += 1;
				white_pieces++;
			}

			start_x += move.first;
			start_y += move.second;
			cur_x += move.first;
			cur_y += move.second;
		}
	}
	return cur_score;
}

//get score based on center pivot
int board::get_cor_score(int cor_x, int cor_y) {
	int cur_score = 0;

	//loop through pattern lengths
	for (int i = min_pat_sz; i <= max_pat_sz; i++) {
		
		//horizontal
		cur_score += get_score_in_line(cor_x, cor_y, { 0, 1 }, i, false);
		//vertical
		cur_score += get_score_in_line(cor_x, cor_y, { 1, 0 }, i, false);
		//diagonal top left to bottom right
		cur_score += get_score_in_line(cor_x, cor_y, { 1, 1 }, i, true);
		//other diagonal
		cur_score += get_score_in_line(cor_x, cor_y, { 1, -1 }, i, true);

	}
	return cur_score;

}

//returns the change in score by making move
void board::score_change(int move_x, int move_y, char piece, bool undo) {
	int before_score = get_cor_score(move_x, move_y);
	if (!undo) b[move_x][move_y] = piece;
	else b[move_x][move_y] = '.';
	int after_score = get_cor_score(move_x, move_y);
	if (!undo) b[move_x][move_y] = '.';
	else b[move_x][move_y] = piece;
	board_score += (after_score - before_score);
}

//make a move
//I swear there's a way to make this more efficient but for now this'll do
void board::make_move(int move_x, int move_y, char piece) {
	hash_val ^= zobrist_table[move_x][move_y][piece_to_bool[piece]];
	score_change(move_x, move_y, piece, false);
	b[move_x][move_y] = piece;
	int cur_idx = (move_x * ROWS) + move_y;
	move_list.erase(square_weight[move_x][move_y]);
	for (int x = 0; x < surrounding_squares[cur_idx].size(); x++) {
		int weight = surrounding_squares[cur_idx][x];
		int square_x = weight_to_square[weight][0];
		int square_y = weight_to_square[weight][1];
		visited[square_x][square_y]++;
		if (b[square_x][square_y] == '.') move_list.insert(weight);
	}
	num_pieces[piece_to_bool[piece]]++;
}

//as says, there must be a more efficient way
void board::undo_move(int move_x, int move_y, char piece, bool has_prev_score, int prev_score) {
	hash_val ^= zobrist_table[move_x][move_y][piece_to_bool[piece]];
	if (has_prev_score) {
		board_score = prev_score;
	}
	else {
		score_change(move_x, move_y, piece, true);
	}
	b[move_x][move_y] = '.';
	int cur_idx = (move_x * ROWS) + move_y;
	for (int x = 0; x < surrounding_squares[cur_idx].size(); x++) {
		int weight = surrounding_squares[cur_idx][x];
		int square_x = weight_to_square[weight][0];
		int square_y = weight_to_square[weight][1];
		visited[square_x][square_y]--;
		if (!visited[square_x][square_y]) {
			move_list.erase(weight);
		}
	}
	int weight = square_weight[move_x][move_y];
	if (visited[weight_to_square[weight][0]][weight_to_square[weight][1]]) {
		move_list.insert(weight);
	}
	num_pieces[piece_to_bool[piece]]--;
}

void board::print_board() {
	
	std::cout << "BOARD SCORE: " << board_score << '\n';
	std::cout << "  ";
	for (int x = 0; x < ROWS; x++) {
		std::cout << x << ' ';
	}
	std::cout << '\n';
	for (int x = 0; x < ROWS; x++) {
		std::cout << x << ' ';
		for (int y = 0; y < COLS; y++) {
			std::cout << b[x][y] << ' ';
		}
		std::cout << '\n';
	}
	/*
	std::cout << '\n' << "VISITED:" << '\n';
	for (int x = 0; x < ROWS; x++) {
		for (int y = 0; y < COLS; y++) {
			std::cout << visited[x][y] << ' ';
		}
		std::cout << '\n';
	}
	*/
	
	std::cout << '\n' << "LIST OF MOVES:" << '\n';

	for (auto it : move_list) {
		std::cout << it << '\n';
	}
	std::cout << '\n';
	
}