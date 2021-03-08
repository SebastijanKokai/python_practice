from threading import Thread
import requests
import json


class CommunicationAPI:

    def get_url(self):
        return "http://localhost:9080"

    # vraca mapu
    def make_get_request(self, relative_url):
        r = requests.get(url=self.get_url() + relative_url)
        data = r.json()
        return data

    # vraca mapu nakon sto se joinuje
    def join_game(self, playerId, gameId):
        return self.make_get_request('/game/play?playerId=' + str(playerId) + '&gameId=' + str(gameId))

    def return_map(self, playerId, gameId):
        mapJson = self.join_game(playerId, gameId)
        return mapJson

    def return_matrix(self, playerId, gameId):
        map = self.return_map(playerId, gameId)
        matrix = map
        return matrix


    def do_action(self, playerId, gameId, action):
        URL = '/doAction?playerId=' + str(playerId) + "&gameId=" + str(gameId) + '&action=' + action
        print(URL)
        response = self.make_get_request(URL)
        return response

    def calculate(self, map, playerId, gameId):
        #logika
        #u zavisnosti od logike biramo action
        player1 = map.get('result').get('player1')
        player2 = map.get('result').get('player2')

        playerIndex = map.get('playerIndex')

        if(playerIndex == 1):
            # enemy coordinates
            enemy_x = player2.get('x')
            enemy_y = player2.get('y')

            # my coordinates
            x = player1.get('x')
            y = player1.get('y')

            action = self.temp(x, y, enemy_x, enemy_y)

        elif(playerIndex == 2):
            # enemy coordinates
            enemy_x = player1.get('x')
            enemy_y = player1.get('y')

            # my coordinates
            x = player2.get('x')
            y = player2.get('y')

            action = self.temp(x, y, enemy_x, enemy_y)

        if(action != ''):
            response = self.do_action(playerId, gameId, action)
            self.run(response, playerId, gameId)

    def run(self, map, playerId, gameId):
        res = self.calculate(map, playerId, gameId)
        #self.run()

    def temp(self, x, y, enemy_x, enemy_y):
        action = ''
        if(x < enemy_x):
            action = 'd'
        elif(x > enemy_x):
            action = 'a'
        if(y < enemy_y):
            action = 's'
        elif(y > enemy_y):
            action = 'w'

        return action



c = CommunicationAPI()


#join game
#print(c.return_matrix(20, 20))

print("Enter player ID:")
playerId = input()
print("Enter game id:")
gameId = input()

#join game
map = (c.return_matrix(playerId, gameId))
print(map)

#run game
#c.run(map, playerId, gameId)

#run with two threads
Thread(target = c.run(map, playerId, gameId)).start()
Thread(target = c.run(map, 2, gameId)).start()
