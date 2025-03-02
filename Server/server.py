from flask import Flask, request, jsonify
import geolib
app = Flask(__name__)

class Location:
    def __init__(self, latitude, longitude):
        self.latitude = longitude
        self.longitude = longitude

class Player:
    def __init__(self, user_name, role = "runner"):
        self.user_name = user_name
        # runner or tagger
        self.role = role
        self.location = Location(0.0, 0.0)
        self.is_tagged = False
        
class Game:
    def __init__(self, lobby_name):
        self.lobby_name = lobby_name
        self.is_active = False
        self.players = []

games = []

def verify_credentials_data(data):
    if 'lobby_name' not in data:
        return -1
    
    if not isinstance(data['lobby_name'], str):
        return -1

    for index, game in enumerate(games):
        if game.lobby_name == data['lobby_name']:
            return index
    return -1

def verify_credentials_arguments(lobby_name):
    if not isinstance(lobby_name, str):
        return -1

    for index, game in enumerate(games):
        if game.lobby_name == lobby_name:
            return index
    return -1
        
def identify_Tagger(players):
    for player in players:
        if player.role == "tagger":
            return player
    return None

def find_nearest_player(tagger, players):
    nearest_player = None
    min_distance = float('inf')  # Initialize with a large value

    for player in players:
        if player.user_name != tagger.user_name:  # Skip the tagger itself
            if player.is_tagged == True:
                # Calculate distance using geolib
                distance = geohash.distance(
                    (tagger.location.latitude, tagger.location.longitude),
                    (player.location.latitude, player.location.longitude)
                )
                if distance < min_distance:
                    min_distance = distance
                    nearest_player = player

    return nearest_player, min_distance

def find_center_coordinates(players):
    if not players:
        return None  # Return None if no players exist

    # Create a list of dictionaries containing lat/lon for each player
    player_locations = {[player.location.latitude, player.location.longitude] for player in players}

    # Use geolib to find the center
    center = getCenter(player_locations)

    return center

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

@app.route('/join_game', methods=['POST'])
def join_game():
    global games
    data = request.get_json()
    index = verify_credentials_data(data)
    
    if index == -1:
        return jsonify({"code": 7})
    
    if 'user_name' not in data:
        return jsonify({"code": 7})
    
    if not isinstance(data['user_name'], str):
        return jsonify({"code": 7})

    for player in games[index].players:
        if player.user_name == str(data['user_name']):
            return jsonify({"code": 7})
    
    games[index].players.append(Player(data['user_name']))
    
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
        "game_status": game.is_active,
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
    
    if 'role' not in data or 'user_name' not in data or 'latitude' not in data or 'longitude' not in data or 'is_tagged' not in data:
        return jsonify({"code": 7})
    
    if not isinstance(data['user_name'], str) or not isinstance(data['latitude'], float) or not isinstance(data['longitude'], float) or not isinstance(data['is_tagged'], bool):
        return jsonify({"code": 7})
    
    for player in games[index].players:
        if player.user_name == data['user_name']:
            player.role = data['role']
            player.location.latitude = data['latitude']
            player.location.longitude = data['longitude']
            player.is_tagged = data['is_tagged']
            return jsonify({"code": 0})

    return jsonify({"code": 7})

@app.route('/get_center_coords', methods=['GET'])
def get_center_coords():
    global games
    lobby_name = request.args.get("lobby_name")

    if not lobby_name:
        return jsonify({"code": 7})

    index = verify_credentials_arguments(lobby_name)
    if index == -1:
        return jsonify({"code": 7})

    game = games[index]

    center = find_center_coordinates(game.players)
    if center is None:
        return jsonify({"code": 8})

    return jsonify({"code": 7, "center_coordinates":center})

if __name__ == '__main__':
    # Enable threaded mode to handle multiple requests concurrently
    app.run(debug=True, use_reloader=False, threaded=True)