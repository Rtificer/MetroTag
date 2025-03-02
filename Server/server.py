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
    def __init__(self, lobby_name, password):
        self.lobby_name = lobby_name
        self.password = password
        self.active = False
        self.players = []

games = []

def verify_credentials(lobby_name, password):
    if not isinstance(lobby_name, str) or not isinstance(password, str):
        return -1

    for index, game in enumerate(games):
        if game.lobby_name == lobby_name and game.password == password:
            return index
    return -1
        

@app.route('/create_game', methods=['POST'])
def create_game():
    
    data = request.get_json()
    if 'lobby_name' not in data or 'password' not in data:
        return jsonify({"code": 7})
        
    if not isinstance(data['lobby_name'], str) or not isinstance(data['password'], str):
        return jsonify({"code": 7})

    if len(data['lobby_name']) < 1:
        return jsonify({"code": 3})

    for game in games:
        if game.lobby_name == data['lobby_name']:
            return jsonify({"code": 1})
    
    games.append(Game(data['lobby_name'], data['password']))
    return jsonify({"code": 0})


@app.route('/get_game_state', methods=['GET'])
def get_gamestate():
    lobby_name = request.args.get("lobby_name")
    password = request.args.get("password")

    if not lobby_name or not password:
        return jsonify({"code": 7})

    index = verify_credentials(lobby_name, password)
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


if __name__ == '__main__':
    # Enable threaded mode to handle multiple requests concurrently
    app.run(debug=True, use_reloader=False, threaded=True)