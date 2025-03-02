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
        self.role = role
        self.location = location
        
class Game:
    def __init__(self, lobby_name, password):
        self.lobby_name = lobby_name
        self.password = password
        self.Active = False
        self.Players = []

games = []

def verify_credentials(data):
    if 'lobby_name' in data and 'password' in data and 'user_name' in data and all(isinstance(var, str) for var in (data['lobby_name'], data['password'], data['user_name'])):
        for index, game in enumerate(games):
            if game.lobby_name == data['lobby_name'] and game.password == data['password']:
                if any(player.user_name == data['user_name'] for player in game.Players):
                    return index
                else:
                    return -1
        return -1
    else:
        return -1
        

@app.route('/get_game_state', methods=['GET'])
async def get_gamestate():
    await asyncio.sleep(1)
    data = request.get_json()
    global games
    
    index = verify_credentials()
    if index == -1:
        return jsonify({"code": 7})
    
    game_state = {
        "code": 0,
        "game_status": games[index].Active,
    }

    for player in games[index].Players:
        game_state[player.user_name] = {
            "role": player.role,
            "location": [player.location.latitude, player.location.longitude]
        }

    return jsonify(game_state)

#update_player_data


# Run the app in an asynchronous manner
if __name__ == '__main__':
    app.run(debug=True, use_reloader=False)