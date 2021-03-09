import requests
import numpy


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

    def do_action(self, playerId, gameId, action):
        URL = '/doAction?playerId=' + str(playerId) + "&gameId=" + str(gameId) + '&action=' + action
        print(URL)
        response = self.make_get_request(URL)
        return response

    def calculate(self, map, playerId, gameId):
        player1 = map.get('result').get('player1')
        player2 = map.get('result').get('player2')

        action = ''

        playerIndex = map.get('playerIndex')

        if playerIndex == 2:
            # enemy coordinates
            enemy_x = player1.get('x')
            enemy_y = player1.get('y')

            # my coordinates
            x = player2.get('x')
            y = player2.get('y')

            # last action
            lastAction = map.get('result').get('player1').get('lastAction')

            if lastAction != None:
                action = self.move(x, y, enemy_x, enemy_y)
            else:
                action = 'mw'

        elif playerIndex == 1:
            # enemy coordinates
            enemy_x = player2.get('x')
            enemy_y = player2.get('y')

            # my coordinates
            x = player1.get('x')
            y = player1.get('y')

            # last action
            lastAction = map.get('result').get('player2').get('lastAction')

            if lastAction != None:
                action = self.move(x, y, enemy_x, enemy_y)
            else:
                action = 'mw'

        if action != '':
            response = self.do_action(playerId, gameId, action)
            print(response)
            if playerIndex == 1:
                self.calculate(response, playerIndex, gameId)
            if playerIndex == 2:
                self.calculate(response, playerIndex, gameId)

    def move(self, x, y, enemy_x, enemy_y):
        action = ''
        if x < enemy_x:
            action = 'd'
        elif x > enemy_x:
            action = 'a'
        if y < enemy_y:
            action = 's'
        elif y > enemy_y:
            action = 'w'

        return action

    def matrix(self, map):
        # 0, water, fire, grass
        # 0, 1 fire, 2 grass, 3 water, 4 obstacle
        matrixJson = map.get('result').get('map').get('tiles')
        matrix = [[0 for x in range(20)] for y in range(20)]
        for i in range(20):
            for j in range(20):
                type = matrixJson[i][j].get('type')
                item = matrixJson[i][j].get('item')

                # type
                if type == 'WATER':
                    matrix[i][j] = 'w'
                if type == 'FIRE':
                    matrix[i][j] = 'f'
                if type == 'GRASS':
                    matrix[i][j] = 'g'
                if type == 'OBSTACLE':
                    matrix[i][j] = 'o'
                if type == 'NORMAL':
                    matrix[i][j] = 'n'

                # items
                if item == 'WATER':
                    matrix[i][j] = str(matrix[i][j]) + 'w'
                if item == 'FIRE':
                    matrix[i][j] = str(matrix[i][j]) + 'f'
                if item == 'GRASS':
                    matrix[i][j] = str(matrix[i][j]) + 'g'
                if (item == None):
                    matrix[i][j] = str(matrix[i][j]) + 'n'

        print(matrix)

    def distance(self, x, y, matrix):

        for i in range(20):
            for j in range(20):
                matrix[i][j]



c = CommunicationAPI()

print("Enter player ID:")
playerId = input()
print("Enter game id:")
gameId = input()

# join game
levelMap = (c.join_game(playerId, gameId))
print(levelMap)

# fill matrix
c.matrix(levelMap)

# run game
# c.calculate(levelMap, playerId, gameId)
