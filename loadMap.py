import sys

import requests
from collections import deque

ROW = 20
COL = 20

# Below lists detail all four possible movements from a cell
row = [-1, 0, 0, 1]
col = [0, -1, 1, 0]


class Point:
    def __init__(self, x, y):
        self.X = x
        self.Y = y

def moveTemp(self, x, y, enemy_x, enemy_y):

    if x < enemy_x:
        x = x + 1
    elif x > enemy_x:
        x = x - 1
    if y < enemy_y:
        y = y + 1
    elif y > enemy_y:
        y = y - 1

    return Point(x, y)


# Function to check if it is possible to go to position `(row, col)`
# from the current position. The function returns false if row, col
# is not a valid position or has a value 0 or already visited.
def isValid(mat, visited, row, col):
    return (row >= 0) and (row < ROW) and (col >= 0) and (col < COL) \
           and 'o' not in mat[row][col] and not visited[row][col]


# Find the shortest possible route in a matrix `mat` from source
# cell `(i, j)` to destination cell `(x, y)`
def BFS(mat, i, j, x, y):
    # construct a matrix to keep track of visited cells
    visited = [[False for x in range(ROW)] for y in range(COL)]

    # create an empty queue
    q = deque()

    # mark the source cell as visited and enqueue the source node
    visited[i][j] = True

    # `(i, j, dist)` represents matrix cell coordinates, and their
    # minimum distance from the source
    q.append((i, j, 0))

    queue = deque()

    # stores length of the longest path from source to destination
    min_dist = sys.maxsize

    # loop till queue is empty
    while q:

        # dequeue front node and process it
        (i, j, dist) = q.popleft()
        # self.move()
        # queue.append(pt)

        # `(i, j)` represents a current cell, and `dist` stores its
        # minimum distance from the source

        # if the destination is found, update `min_dist` and stop
        if i == x and j == y and visited[i][j]:
            min_dist = dist
            break

        # check for all four possible movements from the current cell
        # and enqueue each valid movement
        for k in range(4):
            # check if it is possible to go to position
            # `(i + row[k], `j` + col[k])` from current position
            if isValid(mat, visited, i + row[k], j + col[k]):
                # mark next cell as visited and enqueue it
                visited[i + row[k]][j + col[k]] = True
                q.append((i + row[k], j + col[k], dist + 1))



    # for i in range(len(queue)):
    #     for j in range(min_dist):
    #         point = queue.popleft()
    #         print(str(point.X) + ' ' + str(point.Y))
    if min_dist != sys.maxsize:
        print("The shortest path from source to destination has length", min_dist)
    else:
        print("Destination can't be reached from a given source")


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

            matrix = self.matrix(map)
            print(matrix)
            self.moveToOrb(matrix, x, y, 6, 3)

            # if lastAction != None:
            #     action = self.move(x, y, enemy_x, enemy_y)
            # else:
            #     action = 'mw'

        if action != '':
            response = self.do_action(playerId, gameId, action)
            print(response)
            if playerIndex == 1:
                self.calculate(response, playerIndex, gameId)
            if playerIndex == 2:
                self.calculate(response, playerIndex, gameId)

        return ''

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
                if type == 'NORMAL':
                    matrix[i][j] = 'n'

                # items
                if item == 'WATER':
                    matrix[i][j] = str(matrix[i][j]) + 'w'
                if item == 'FIRE':
                    matrix[i][j] = str(matrix[i][j]) + 'f'
                if item == 'GRASS':
                    matrix[i][j] = str(matrix[i][j]) + 'g'
                if item == None:
                    matrix[i][j] = str(matrix[i][j]) + 'n'
                if item == 'OBSTACLE':
                    matrix[i][j] = str(matrix[i][j]) + 'o'

        return matrix

    def moveToOrb(self, matrix, x, y, enemy_x, enemy_y):
        print(x)
        print(y)
        print(enemy_x)
        print(enemy_y)
        print(BFS(matrix, x, y, enemy_x, enemy_y))


def main():
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
    c.calculate(levelMap, playerId, gameId)


main()
