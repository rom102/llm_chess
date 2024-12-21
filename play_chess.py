from stockfish import Stockfish
from gemini_model import GeminiModel
import json
import os
from dotenv import load_dotenv

load_dotenv()
stockfish_path = os.getenv("STOCKFISH_PATH")

# Specify the path to the Stockfish executable
stockfish = Stockfish(path=stockfish_path)

# Initial settings
stockfish.set_skill_level(20)
# Display the initial board
print(stockfish.get_board_visual())

# Generate chess moves using GeminiModel
gemini_model = GeminiModel()


def is_game_over(stockfish):
    evaluation = stockfish.get_evaluation()
    return evaluation['type'] == 'mate' or evaluation['type'] == 'stalemate'


def print_evaluation(stockfish):
    evaluation = stockfish.get_evaluation()
    if evaluation['type'] == 'mate':
        print(f"Evaluation: Mate in {evaluation['value']} moves")
    elif evaluation['type'] == 'cp':
        print(f"Evaluation: {evaluation['value']} centipawns ({'White' if evaluation['value'] > 0 else 'Black'} is better)")
    else:
        print("Evaluation: Game is in an undefined state")


while not is_game_over(stockfish):
    # Generate the player's move
    board_state = stockfish.get_fen_position()
    response = gemini_model.generate_chess_move(board_state)
    response_json = json.loads(response.text)
    player_move = response_json.get("move")
    print(f"Your move: {player_move}")
    stockfish.make_moves_from_current_position([player_move])

    # Display evaluation after player's move
    print("After your move:")
    print_evaluation(stockfish)

    if is_game_over(stockfish):
        break

    # Get and display Stockfish's move
    stockfish_move = stockfish.get_best_move()
    print(f"Stockfish's move: {stockfish_move}")
    stockfish.make_moves_from_current_position([stockfish_move])

    # Display the current board
    print(stockfish.get_board_visual())

    # Display evaluation after Stockfish's move
    print("After Stockfish's move:")
    print_evaluation(stockfish)

# Display the message when the game is over
print("Game over")
print(stockfish.get_board_visual())
print_evaluation(stockfish)
