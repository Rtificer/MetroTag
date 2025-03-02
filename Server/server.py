from flask import Flask, request, jsonify
import asyncio

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
        Active = False
        Players = []

games = []

def verify_credentials(data):
    if 'lobby_name' in data and 'password' in data and 'user_name' in data:
        if all(isinstance(var, str) for var in (data['lobby_name'], data['password'], data['user_name'])):
            for index, game in enumerate(games):
                if game.lobby_name == data['lobby_name'] and game.password == data['password']:
                    if any(player.user_name == data['user_name'] for player in game.Players):
                        return index
                    else:
                        return -1
            return -1
        else:
            return -1
    else:
        return -1
        

@app.route('/get_gamestate', methods=['GET'])
async def get_gamestate():
    await asyncio.sleep(1)
    data = request.get_json()
    global games
    
    index = verify_credentials()

#update_player_data