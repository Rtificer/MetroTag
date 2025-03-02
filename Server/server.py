from flask import Flask, request, jsonify
import asyncio

app = Flask(__name__)

class Location:
    def __init__(self, latitude, longitude):
        self.latitude = latitude
        self.longitude = longitude

class Player:
    def __init__(self, user_name, role, location):
        self.user_name = user_name
        #runner or tagger
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
        

@app.route('/get_game_state', methods=['GET'])
def get_gamestate():
    lobby_name = request.args.get("lobby_name")
    password = request.args.get("password")

    if not lobby_name or not password:
        return jsonify({"code": 7, "message": "Missing credentials"}), 400

    index = verify_credentials(lobby_name, password)
    if index == -1:
        return jsonify({"code": 7, "message": "Invalid credentials"}), 403

    game = games[index]

    game_state = {
        "code": 0,
        "game_status": game.active,
        "players": {
            player.user_name: {
                "role": player.role,
                "location": [player.location.latitude, player.location.longitude],
                "is_tagged": player.istagged
            }
            for player in game.players
        }
    }

    return jsonify(game_state)


#update_player_data

if __name__ == '__main__':
    app.run(debug=True, use_reloader=False)