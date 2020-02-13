import json
import os
import random
import bottle

from api import ping_response, start_response, move_response, end_response

ID = 'de508402-17c8-4ac7-ab0b-f96cb53fbee8'
MYSNAKE = 'M'
SNAKE = 'S'
WALL = 'W'
FOOD = 'F'
GOLD = 'G'
SAFTEY = '-'

# Print the state of the game in grid format in the command line interface.
def printgrid(grid):
	for row in grid:
		print(' '.join(row))

# Make new grid and store the state information in the grid
def init(data):
	width = data['board']['width']
	height = data['board']['height']
	grid = [['_' for i in range(width)] for j in range(height)]

	#print("enemy snake body: " + str(data['board']['snakes']))
	for snake in data['board']['snakes']:
		for coord in snake['body']:
			grid[coord['y']][coord['x']] = SNAKE		

	#print("mysnake body: " + str(data['you']['body']))
	for coord in data['you']['body']:
		grid[coord['y']][coord['x']] = MYSNAKE		
	
	for f in data['board']['food']:
		grid[f['y']][f['x']] = FOOD

	return grid


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
	grid = init(data)
	printgrid(grid)


	"""
	TODO: If you intend to have a stateful snake AI,
		    initialize your snake state here using the
		    request's data if necessary.
	"""
	#print(json.dumps(data))

	color = "#000550"

	return start_response(color)


@bottle.post('/move')
def move():
	data = bottle.request.json
	grid = init(data)
	printgrid(grid)

	"""
	TODO: Using the data from the endpoint request object, your
		    snake AI must choose a direction to move in.
	"""
	#print(json.dumps(data))

	directions = ['up', 'down', 'left', 'right']
	direction = random.choice(directions)

	return move_response(direction)


@bottle.post('/end')
def end():
	data = bottle.request.json

	"""
	TODO: If your snake AI was stateful,
		clean up any stateful objects here.
	"""
	#print(json.dumps(data))
	print('\n============GAMEOVER==============\n')
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
	


