from tkinter import *
ENTITY_SIDE = 40
BUBBLE_DISTANCE = 20
PLAYER_SPEED = 75
SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 720

def setWindowProperties(w, h):
	window = Tk()

	window.title("Orbox")

	ws = window.winfo_screenwidth()
	hs = window.winfo_screenheight()

	x = (ws/2) - (w/2)
	y = (hs/2) - (h/2)
	window.geometry('%dx%d+%d+%d' % (w, h, x, y))
	return window


window = setWindowProperties(SCREEN_WIDTH, SCREEN_HEIGHT)
canvas = Canvas(window, bg="black", width=SCREEN_WIDTH, height=SCREEN_HEIGHT)
canvas.pack()

SPACESHIP_IMAGE = PhotoImage(file = "resources/spaceship_transparent.png")
WALL_IMAGE = PhotoImage(file = "resources/wall_transparent.png")
PLANET_IMAGE = PhotoImage(file = "resources/planet_transparent.png")
BUBBLE_IMAGE = PhotoImage(file = "resources/bubble_transparent.png")

class Entity:
	def __init__(self, x, y, color):
		self.x = x
		self.y = y
		self.color = color
		global field
		field[self.x][self.y] = type(self)
		self.index = canvas.create_rectangle((self.x) * ENTITY_SIDE, (self.y) * ENTITY_SIDE, (self.x + 1) * ENTITY_SIDE, (self.y + 1) * ENTITY_SIDE, fill=self.color)

class Player(Entity):
	def __init__(self, x, y):
		self.x = x
		self.y = y
		global field
		field[self.x][self.y] = "Player"
		self.index = canvas.create_image((self.x) * ENTITY_SIDE, (self.y) * ENTITY_SIDE, image=SPACESHIP_IMAGE, anchor=NW)

class Wall(Entity):
	def __init__(self, x, y):
		self.x = x
		self.y = y
		global field
		field[self.x][self.y] = "Wall"
		self.index = canvas.create_image((self.x) * ENTITY_SIDE, (self.y) * ENTITY_SIDE, image=WALL_IMAGE, anchor=NW)

class EndPoint(Entity):
	def __init__(self, x, y):
		self.x = x
		self.y = y
		global field
		field[self.x][self.y] = "EndPoint"
		self.index = canvas.create_image((self.x) * ENTITY_SIDE, (self.y) * ENTITY_SIDE, image=PLANET_IMAGE, anchor=NW)

class Bubble:
	def __init__(self, x, y):
		self.x = x
		self.y = y
		global field
		field[self.x][self.y] = "Bubble"
		self.index = canvas.create_image((self.x + 1) * ENTITY_SIDE + BUBBLE_DISTANCE, (self.y + 1) * ENTITY_SIDE + BUBBLE_DISTANCE, image=BUBBLE_IMAGE, anchor=CENTER)

class Level:
	def __init__(self):
		self.player = Player(8,4)
		self.walls = []
		self.walls.append(Wall(17, 4))
		self.walls.append(Wall(12, 12))
		self.walls.append(Wall(13, 4))
		self.walls.append(Wall(18, 11))
		self.walls.append(Wall(11, 8))
		self.endPoint = EndPoint(22, 5)


def overlapping(a,b):
	x = 0
	y = 0
	if direction == "left":
		x = -40
	if direction == "right":
		x = 40
	if direction == "up":
		y = -40
	if direction == "down":
		y = 40

	if a[0] + x < b[0] + 40 and a[0] + 40 + x > b[0] and a[1] + y < b[1] + 40 and a[1] + 40 + y > b[1]:
		return True
	return False
	
def overlappingEndPoint(a,b):
	if a[0] < b[0] + 40 and a[0] + 40 > b[0] and a[1] < b[1] + 40 and a[1] + 40 > b[1]:
		return True
	return False

def movePlayer():
	canvas.pack()
	global direction
	isPLayerMoving = False
	levelPassed = False
	bubbles = []
	playerPosition = []
	playerPosition = canvas.coords(player.index)
	x = 0
	y = 0
	if not levelPassed:
		if direction == "left":
			x = -ENTITY_SIDE
			y = 0
			isPLayerMoving = True
		elif direction == "right":
			x = ENTITY_SIDE
			y = 0
			isPLayerMoving = True
		elif direction == "up":
			x = 0
			y = -ENTITY_SIDE
			isPLayerMoving = True
		elif direction == "down":
			x = 0
			y = ENTITY_SIDE
			isPLayerMoving = True

		if not isPLayerMoving and 'gameOver' not in locals():
			window.after(PLAYER_SPEED, movePlayer)

		while isPLayerMoving:
			window.after(PLAYER_SPEED, automaticMove(player, player.index, x, y, bubbles))
			playerPosition = canvas.coords(player.index)
			endPosition = []
			endPosition = canvas.coords(endPoint.index)
			if ((playerPosition[0] <= 0 and playerPosition[0] + 40 <= 0) or (playerPosition[0] >= SCREEN_WIDTH and playerPosition[0] + 40 >= SCREEN_WIDTH)) or ((playerPosition[1] <= 0 and playerPosition[1] + 40 <= 0) or (playerPosition[1] >= SCREEN_HEIGHT and playerPosition[1] + 40 >= SCREEN_HEIGHT)):
				gameOver = True
				isPLayerMoving = False
				gameOverText = canvas.create_text(SCREEN_WIDTH/2 , 20 , fill="white" , font="Times 20 italic bold", text="GAME OVER!")
			for wall in walls:
				wallPosition = canvas.coords(wall.index)
				if overlapping(playerPosition, wallPosition):
					#TODO: bug found: possible movement inside a wall
					isPLayerMoving = False
					direction = ""
					window.after(PLAYER_SPEED, movePlayer)
			if overlappingEndPoint(playerPosition, endPosition):
				isPLayerMoving = False
				direction = ""
				levelPassed = True
				levelPassedText = canvas.create_text(SCREEN_WIDTH/2 , 20 , fill="white" , font="Times 20 italic bold", text="Level Passed")

			canvas.update()


def automaticMove(player, index, x, y, bubbles):
	global direction
	if direction == "up":
		player.y -=1
	elif direction == "down":
		player.y +=1
	elif direction == "left":
		player.x -=1
	elif direction == "right":
		player.x +=1
	position = canvas.coords(index)
	bubbleX = int(position[0] / 40) - 1
	bubbleY = int(position[1] / 40) - 1
	if bubbleX >= -1 and bubbleX <= 30 and bubbleY >= -1 and bubbleY <= 16:
		bubble = Bubble(bubbleX, bubbleY)
		bubbles.append(bubble)
	
	canvas.move(index, x , y)
	

def leftKey(event):
	global direction
	direction = "left"

def rightKey(event):
	global direction
	direction = "right"

def upKey(event):
	global direction
	direction = "up"

def downKey(event):
	global direction
	direction = "down"





canvas.bind("<Left>", leftKey)
canvas.bind("<Right>", rightKey)
canvas.bind("<Up>", upKey)
canvas.bind("<Down>", downKey)
canvas.focus_set()

direction = ""
field = [["" for i in range(17)] for j in range(31)]
canvas.pack()
level = Level()
player = level.player
walls = level.walls
endPoint = level.endPoint

movePlayer()
window.mainloop()
