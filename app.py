from flask import Flask, render_template, redirect, url_for, session, request
from game import TicTacToe
from player import HumanPlayer, RandomComputerPlayer, SmartComputerPlayer
import random
import os

app = Flask(__name__)
app.secret_key = os.urandom(24)

# def init_game(opponent_type):
#     game = TicTacToe()
#     x_player = HumanPlayer('X')
#     if opponent_type == 'smart':
#         o_player = SmartComputerPlayer('O')
#     else:
#         o_player = RandomComputerPlayer('O')
#     return game, x_player, o_player

@app.route('/')
def index():
    return render_template('index.html')

# @app.route('/start', methods=['POST'])
# def start():
#     opponent = request.form.get('opponent')
#     game, x_player, o_player = init_game(opponent)
#     session['board'] = game.board
#     session['opponent'] = opponent
#     session['turn'] = 'X'
#     session['winner'] = None
#     return redirect(url_for('play'))
@app.route('/start', methods=['POST'])
def start():

    # Initialize game with unbeatable AI only
    game = TicTacToe()
    x_player = HumanPlayer('X')
    o_player = SmartComputerPlayer('O')

    # Store players and game board in session
    session['board'] = game.board
    session['turn'] = 'X'
    session['winner'] = None

    # Optionally store game object in memory or rebuild on demand in /play
    session['x_letter'] = x_player.letter
    session['o_letter'] = o_player.letter

    return redirect(url_for('play'))


@app.route('/play')
def play():
    board = session.get('board')
    winner = session.get('winner')
    turn = session.get('turn')
    return render_template('game.html', board=board, turn=turn, winner=winner)

@app.route('/move/<int:square>',methods=['POST'])
def move(square):
    board = session['board']
    game = TicTacToe()
    game.board = board
    game.current_winner = None


    if board[square] != ' ':
        return redirect(url_for('play'))
    turn = session['turn']
    # opponent = session['opponent']

    # Player move
    game.make_move(square, turn)

    if game.current_winner:
        session['board'] = game.board
        session['winner'] = turn
        return redirect(url_for('play'))

    # AI move
    # ai_player = SmartComputerPlayer('O')  if opponent == 'smart' else RandomComputerPlayer('O')
    if game.empty_squares():
        ai_player = SmartComputerPlayer('O')
        ai_square = ai_player.get_move(game)
        game.make_move(ai_square, 'O')
        if game.current_winner:
            session['winner'] = 'O'
    else:
        # Tie: no empty squares left
        session['winner'] = 'Tie'

    session['board'] = game.board
    session['turn'] = 'X'
    return redirect(url_for('play'))

@app.route('/reset')
def reset():
    session.clear()
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
