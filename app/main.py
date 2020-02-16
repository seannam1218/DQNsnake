import json
import os
import random
import bottle
import copy

from api import ping_response, start_response, move_response, end_response

maxwidth = 11+2
maxheight = 11+2
prev_move = None

LAND = '_' #[1,0,0,0,0]
MYSNAKE = 'M' #[0,1,0,0,0]
SNAKE = 'S' #[0,0,1,0,0]
WALL = 'W' #[0,0,0,1,0]
FOOD = 'F' #[0,0,0,0,1]


# Print the state of the game in grid format in the command line interface.
def printgrid(grid):
	for row in grid:
		print(' '.join(row))
		#print(''.join(str(row)))

# Make new grid and store the state information in the grid
def load(data):
	width = data['board']['width']
	height = data['board']['height']
	grid = [[LAND for i in range(width)] for j in range(height)]

	#print("enemy snake body: " + str(data['board']['snakes']))
	for snake in data['board']['snakes']:
		for coord in snake['body']:
			grid[coord['y']][coord['x']] = SNAKE		

	#print("mysnake body: " + str(data['you']['body']))
	for coord in data['you']['body']:
		grid[coord['y']][coord['x']] = MYSNAKE		
	
	for f in data['board']['food']:
		grid[f['y']][f['x']] = FOOD

	pad_walls(grid)

	return grid


def pad_walls(grid):
	#pad the top wall
	width = len(grid[0])
	horz_wall = [WALL for i in range(width)]
	grid.insert(0, copy.deepcopy(horz_wall))

	#pad the bottom wall
	bottom_pad_size = maxheight - len(grid)
	for i in range(bottom_pad_size):
		grid.append(copy.deepcopy(horz_wall))

	#pad the left wall
	for j in range(maxheight):
		grid[j].insert(0, WALL)

	#pad the right wall
	right_pad_size = maxwidth - len(grid[0])
	for k in range(maxheight):
		for l in range(right_pad_size):
			grid[k].append(WALL)

	return 


def check_alive():
	alive = 0
	
		

	return alive

###################################
########## SERVER CALLS ###########
###################################

@bottle.route('/')
def index():
    return '''
    Battlesnake documentation can be found at
       <a href="https://docs.battlesnake.com">https://docs.battlesnake.com</a>.
    '''


@bottle.route('/static/<path:path>')
def static(path):
    """
    Given a path, return the static file located relative
    to the static folder.

    This can be used to return the snake head URL in an API response.
    """
    return bottle.static_file(path, root='static/')


@bottle.post('/ping')
def ping():
    """
    A keep-alive endpoint used to prevent cloud application platforms,
    such as Heroku, from sleeping the application instance.
    """
    return ping_response()


@bottle.post('/start')
def start():
	data = bottle.request.json
	grid = load(data)
	# printgrid(grid)


	"""
	TODO: If you intend to have a stateful snake AI,
		    initialize your snake state here using the
		    request's data if necessary.
	"""

	color = "#000550"

	#print(json.dumps(data, indent=4))
	return start_response(color)


@bottle.post('/move')
def move():
	data = bottle.request.json
	grid = load(data)
	printgrid(grid)

	turn = data['turn']	
	check_alive(data['you'], data['snakes'])

	print('\n')
	print('turn: ' + str(turn))

	#Use trained DQN network to choose a direction to move in
	directions = ['up', 'down', 'left', 'right']
	
	direction = random.choice(directions)
	print('direction: ' + direction + '\n')

	prev_move = direction
	return move_response(direction)


@bottle.post('/end')
def end():
	data = bottle.request.json

	print(json.dumps(data, indent=4))
	print('\n============GAMEOVER==============\n')

	#concat the state info to a json file


	return end_response()


# Expose WSGI app (so gunicorn can find it)
application = bottle.default_app()

if __name__ == '__main__':
    bottle.run(
        application,
        host=os.getenv('IP', '0.0.0.0'),
        port=os.getenv('PORT', '8080'),
        debug=os.getenv('DEBUG', True)
    )
	


