from flask import Flask, render_template
from flask_socketio import SocketIO, emit, join_room

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your-secret-key'
socketio = SocketIO(app)

# Store game states
games = {}

@app.route('/')
def index():
    return render_template('index.html')

@socketio.on('connect')
def handle_connect():
    print('Client connected')

@socketio.on('join_game')
def handle_join_game(data):
    game_id = data['game_id']
    player_name = data['player_name']
    
    if game_id not in games:
        games[game_id] = {
            'players': [],
            'current_turn': 0,
            'deck': [],
            'hands': {},
            'marbles': {}
        }
    
    # Add player to game
    games[game_id]['players'].append(player_name)
    join_room(game_id)
    
    # Broadcast updated game state
    emit('game_update', games[game_id], to=game_id)

@socketio.on('make_move')
def handle_move(data):
    game_id = data['game_id']
    # Process the move...
    # Update game state...
    
    # Broadcast updated game state to all players
    emit('game_update', games[game_id], to=game_id)

if __name__ == '__main__':
    socketio.run(app, debug=True)