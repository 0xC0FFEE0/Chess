from flask import Flask, render_template, request, jsonify, session
from flask_socketio import SocketIO, emit
import chess
import chess.engine
from stockfish import Stockfish
import json
import uuid
import os

app = Flask(__name__)
app.config['SECRET_KEY'] = 'chess_app_secret_key_change_in_production'
socketio = SocketIO(app, cors_allowed_origins="*")

# Global game storage (in production, use a proper database)
games = {}

class ChessGame:
    def __init__(self, game_id):
        self.game_id = game_id
        self.board = chess.Board()
        self.move_history = []
        self.stockfish = None
        self.game_over = False
        self.result = None
        
    def initialize_stockfish(self, stockfish_path=None):
        """Initialize Stockfish engine"""
        try:
            # Try to find Stockfish binary
            possible_paths = [
                stockfish_path,
                "stockfish",
                "/usr/bin/stockfish",
                "/usr/local/bin/stockfish",
                "C:/Program Files/Stockfish/bin/stockfish.exe",
                "./stockfish.exe"
            ]
            
            for path in possible_paths:
                if path and os.path.exists(path):
                    self.stockfish = Stockfish(path=path)
                    self.stockfish.set_depth(15)
                    return True
            
            # If no path found, try default
            self.stockfish = Stockfish()
            self.stockfish.set_depth(15)
            return True
            
        except Exception as e:
            print(f"Failed to initialize Stockfish: {e}")
            return False
    
    def make_move(self, move_uci):
        """Make a move on the board"""
        try:
            move = chess.Move.from_uci(move_uci)
            if move in self.board.legal_moves:
                self.board.push(move)
                self.move_history.append(move_uci)
                
                # Check for game over
                if self.board.is_game_over():
                    self.game_over = True
                    self.result = self.board.result()
                
                return True
            return False
        except:
            return False
    
    def get_stockfish_move(self):
        """Get best move from Stockfish"""
        if not self.stockfish or self.game_over:
            return None
        
        try:
            self.stockfish.set_fen_position(self.board.fen())
            best_move = self.stockfish.get_best_move()
            return best_move
        except:
            return None
    
    def get_board_state(self):
        """Get current board state"""
        return {
            'fen': self.board.fen(),
            'turn': 'white' if self.board.turn else 'black',
            'legal_moves': [move.uci() for move in self.board.legal_moves],
            'move_history': self.move_history,
            'game_over': self.game_over,
            'result': self.result,
            'in_check': self.board.is_check(),
            'move_count': len(self.move_history)
        }

@app.route('/')
def index():
    """Main chess game page"""
    return render_template('index.html')

@app.route('/new_game', methods=['POST'])
def new_game():
    """Create a new chess game"""
    game_id = str(uuid.uuid4())
    games[game_id] = ChessGame(game_id)
    
    # Initialize Stockfish
    stockfish_initialized = games[game_id].initialize_stockfish()
    
    return jsonify({
        'game_id': game_id,
        'board_state': games[game_id].get_board_state(),
        'stockfish_available': stockfish_initialized
    })

@app.route('/move', methods=['POST'])
def make_move():
    """Make a player move"""
    data = request.get_json()
    game_id = data.get('game_id')
    move = data.get('move')
    
    if game_id not in games:
        return jsonify({'error': 'Game not found'}), 404
    
    game = games[game_id]
    
    if not game.make_move(move):
        return jsonify({'error': 'Invalid move'}), 400
    
    response = {
        'success': True,
        'board_state': game.get_board_state()
    }
    
    # Get Stockfish response if game is not over and it's black's turn
    if not game.game_over and not game.board.turn:  # Black's turn (Stockfish)
        stockfish_move = game.get_stockfish_move()
        if stockfish_move:
            game.make_move(stockfish_move)
            response['stockfish_move'] = stockfish_move
            response['board_state'] = game.get_board_state()
    
    return jsonify(response)

@app.route('/game/<game_id>')
def get_game_state(game_id):
    """Get current game state"""
    if game_id not in games:
        return jsonify({'error': 'Game not found'}), 404
    
    return jsonify(games[game_id].get_board_state())

@app.route('/stockfish_move', methods=['POST'])
def get_stockfish_move():
    """Get Stockfish move suggestion"""
    data = request.get_json()
    game_id = data.get('game_id')
    
    if game_id not in games:
        return jsonify({'error': 'Game not found'}), 404
    
    game = games[game_id]
    move = game.get_stockfish_move()
    
    if move:
        return jsonify({'move': move})
    else:
        return jsonify({'error': 'Could not get Stockfish move'}), 500

if __name__ == '__main__':
    # Create templates directory if it doesn't exist
    os.makedirs('templates', exist_ok=True)
    os.makedirs('static', exist_ok=True)
    
    print("Starting Chess Web App...")
    print("Make sure Stockfish is installed and accessible in your PATH")
    print("Visit http://localhost:5000 to play chess!")
    
    socketio.run(app, host='0.0.0.0', port=5000, debug=True)