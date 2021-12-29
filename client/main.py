import gomoku
import time, random

possible_pieces = [' ', 'b', 'w']

def generate_random_board():
    return [[possible_pieces[random.randint(0,2)] for x in range(0,8)] for x in range(0,8)]

while(True):
    print("SENDING BOARD")
    gomoku.move(generate_random_board(), 1)
    time.sleep(5)