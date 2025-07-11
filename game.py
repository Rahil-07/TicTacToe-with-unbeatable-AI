import math
import time
from player import HumanPlayer,RandomComputerPlayer,SmartComputerPlayer

class TicTacToe:
    def __init__(self):
        self.board = [' ' for _ in range(9)]
        self.current_winner = None
    
    def print_board(self):
        for row in [ self.board[i*3:(i+1)*3] for i in range(3)]:
            print('| ' + ' | '.join(row) + ' |')
    
    @staticmethod
    def print_board_nums():
        number_board = [   [str(i) for i in range(j*3,(j+1)*3)] for j in range(3)]
        for row in number_board:
            print('| '+' | '.join(row)+' |')

    def make_move(self,square,letter):
        if self.board[square] == ' ':
            self.board[square] = letter
            if self.winner(square,letter):
                self.current_winner = letter
            return True
        return False

    def winner(self, square , letter):

        row_id = math.floor(square / 3)
        row = self.board[row_id*3:(row_id+1)*3]
        if all([s==letter for s in row]):
            return True
        
        col_id = square % 3
        column = [self.board[col_id+i*3] for i in range(3)]
        if all([s == letter for s in column]):
            return True
        
        if square % 2 == 0:
            diago1 = [self.board[i] for i in [0,4,8]]
            if all([s==letter for s in diago1]):
                return True
            
            diago2 = [self.board[i] for i in [2,4,6]]
            if all([s==letter for s in diago2]):
                return True
        return False
    
    def empty_squares(self):
        return ' ' in self.board
    
    def num_empty_squares(self):
        return self.board.count(' ')

    def available_moves(self):
        return [i for i,x in enumerate(self.board) if x == ' ']

def play(game, x_player, o_player, print_game=True):
    
    if print_game:
        game.print_board_nums()
    
    letter = 'X'
    while game.empty_squares():
        if letter == 'O':
            square = o_player.get_move(game)
        else:
            square = x_player.get_move(game)
        
        if game.make_move(square,letter):

            if print_game:
                print(letter + ' makes a move to squares {}'.format(square))
                game.print_board()
                print('')
            
            if game.current_winner:
                if print_game:
                    print(letter + ' Wins! ')
                return letter
            letter = 'O' if letter == 'X' else 'X'
        time.sleep(.8)

    if print_game:
        print("It\'s a Tie! ")

if __name__ == '__main__':
    opponent = int(input('___Opponent___\n\t1. RandomComputer\n\t2. Unbeatable AI\nEnter Opponent no. : '))
    x_player = HumanPlayer('X')
    if opponent == 2:
        o_player = SmartComputerPlayer('O') 
    else: 
        o_player = RandomComputerPlayer('O')
    t = TicTacToe()
    play(t , x_player , o_player , print_game=True)