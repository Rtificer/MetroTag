from flask import Flask, request, jsonify

app = Flask(__name__)

class Location:
    def __init__(self, latitude, longitude):
        self.latitude = latitude
        self.longitude = longitude

class Player:
    def __init__(self, user_name, role, location):
        self.user_name = user_name
        # runner or tagger
        self.role = role
        self.location = location
        self.is_tagged = False
        
class Game:
    def __init__(self, lobby_name):
        self.lobby_name = lobby_name
        self.active = False
        self.players = []

games = []

def verify_credentials_data(data):
    if 'lobby_name' not in data:
        return -1
    
    if not isinstance(data['lobby_name'], str)
        return -1

    for index, game in enumerate(games):
        if game.lobby_name == data['lobby_name']
            return index
    return -1

def verify_credentials_arguments(lobby_name):
    if not isinstance(lobby_name, str)
        return -1

    for index, game in enumerate(games):
        if game.lobby_name == lobby_name
            return index
    return -1
        

@app.route('/create_game', methods=['POST'])
def create_game():
    global games
    data = request.get_json()
    if 'lobby_name' not in data:
        return jsonify({"code": 7})
        
    if not isinstance(data['lobby_name'], str):
        return jsonify({"code": 7})

    if len(data['lobby_name']) < 1:
        return jsonify({"code": 3})

    for game in games:
        if game.lobby_name == data['lobby_name']:
            return jsonify({"code": 1})
    
    games.append(Game(data['lobby_name']))
    return jsonify({"code": 0})


@app.route('/get_game_state', methods=['GET'])
def get_gamestate():
    global games
    lobby_name = request.args.get("lobby_name")

    if not lobby_name:
        return jsonify({"code": 7})

    index = verify_credentials_arguments(lobby_name)
    if index == -1:
        return jsonify({"code": 7})

    game = games[index]

    game_state = {
        "code": 0,
        "game_status": game.active,
        "players": {
            player.user_name: {
                "role": player.role,
                "location": [player.location.latitude, player.location.longitude],
                "is_tagged": player.is_tagged
            }
            for player in game.players
        }
    }

    return jsonify(game_state)

@app.route('/update_player_data', methods=['POST'])
def update_player_data():
    global games
    data = request.get_json()
    
    index = verify_credentials_data(data)
    
    if index == -1:
        return jsonify({"code": 7})
    
    game = game[index]
    
    


if __name__ == '__main__':
    # Enable threaded mode to handle multiple requests concurrently
    app.run(debug=True, use_reloader=False, threaded=True)