from flask import Flask, request, jsonify
import asyncio

class Location:
    def __init__(self, latitude, longitude):
        self.latitude = latitude
        self.longitude = longitude

class Player:
    def __init__(self, user_name, location):
        self.user_name = user_name
        self.location = location
        
class Game:
    def __init__(self, lobby_name, password):
        self.lobby_name = lobby_name
        self.password = password
        Active = False
        Players = []

games = []

def verify_credentials(lobby_name, password, username):
    if all(isinstance(var, str) for var in (lobby_name, password, username)):
        
        

@app.route('/get_player_locations', methods=['GET'])
async def get_player_locations():
    

#update_player_data