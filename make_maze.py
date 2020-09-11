
'''
a = [
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
    [1, 0, 1, 0, 1, 0, 0, 0, 0, 1],
    [1, 0, 1, 0, 1, 0, 0, 0, 0, 1],
    [1, 0, 1, 0, 1, 1, 1, 1, 0, 1],
    [1, 0, 1, 0, 0, 0, 0, 1, 0, 1],
    [1, 0, 1, 0, 0, 0, 0, 1, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 1, 0, 1],
    [1, 0, 1, 0, 0, 0, 0, 0, 0, 1],
    [1, 0, 1, 0, 0, 0, 0, 0, 0, 1],
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
]

print(a)

start = 1,1
end = 2,5
'''

# Generating maze with randomized variant of Prim's algorithm
# Source: https://github.com/briangordon/mazes.py/blob/master/mazes.py
import png, random, heapq, argparse

GRID_WIDTH, GRID_HEIGHT = 2,2

img_width = GRID_WIDTH * 2 + 1
img_height = GRID_HEIGHT * 2 + 1


class undirected_graph(dict):
	"""A dictionary of unordered pairs."""
	def __setitem__(self, key, value):
		super(undirected_graph, self).__setitem__(tuple(sorted(key)), value)

	def __getitem__(self, key):
		return super(undirected_graph, self).__getitem__(tuple(sorted(key)))

	def __has_key__(self, key):
		return super(undirected_graph, self).__has_key__(tuple(sorted(key)))

def grid_adjacent(vertex):
	"""Return all grid vertices adjacent to the given point."""
	x, y = vertex
	adj = []

	if x > 0:
		adj.append((x-1, y))
	if x < GRID_WIDTH-1:
		adj.append((x+1, y))
	if y > 0:
		adj.append((x, y-1))
	if y < GRID_HEIGHT-1:
		adj.append((x, y+1))

	return adj

def make_grid():
	weights = undirected_graph()
	for x in range(GRID_WIDTH):
		for y in range(GRID_HEIGHT):
			vertex = (x,y)
			for neighbor in grid_adjacent(vertex):
				weights[(vertex,neighbor)] = random.random()

	return weights

def RDM():
	spanning = undirected_graph()

	closed = set([(0,0)])
	neighbors = [((0,0), x) for x in grid_adjacent((0,0))]

	while neighbors:
		v1, v2 = neighbors.pop(random.randrange(len(neighbors)))

		# v1 is the vertex already in the spanning tree
		# it's possible that we've already added v2 to the spanning tree
		if v2 in closed:
			continue

		# add v2 to the closed set
		closed.add(v2)

		for neighbor in grid_adjacent(v2):
			if neighbor not in closed:
				neighbors.append((v2, neighbor))

		# update the spanning tree
		spanning[(v1,v2)] = True
	return draw_tree(spanning)

def draw_tree(spanning):
	# Create a big array of 0s and 1s for pypng

	pixels = []

	# Add a row of off pixels for the top
	pixels.append([0] + [1] + ([0] * (img_width-2)))

	for y in range(GRID_HEIGHT):
		# Row containing nodes
		row = [0] # First column is off
		for x in range(GRID_WIDTH):
			row.append(1)
			if x < GRID_WIDTH-1:
				row.append( int(((x,y),(x+1,y)) in spanning) )
		row.append(0) # Last column is off
		pixels.append(row)

		if y < GRID_HEIGHT-1:
			# Row containing vertical connections between nodes
			row = [0] # First column is off
			for x in range(GRID_WIDTH):
				row.append( int(((x,y),(x,y+1)) in spanning) )
				row.append(0)
			row.append(0) # Last column is off
			pixels.append(row)

	# Add a row of off pixels for the bottom
	pixels.append(([0] * (img_width-2)) + [1] + [0])

	print(pixels)
	return pixels

pix = RDM()



filename = '/home/numair/Documents/gitMaze/mazeIMAGE.png'
f = open(filename, 'wb')
w = png.Writer(img_width, img_height, greyscale=True, bitdepth=1)
w.write(f, pix)
f.close()