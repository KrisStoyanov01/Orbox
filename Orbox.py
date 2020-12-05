from tkinter import *


ENTITY_SIDE = 40
BUBBLE_DISTANCE = 20
PLAYER_SPEED = 75
SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 720

class Entity:
	def __init__(self, x, y):
		self.x = x
		self.y = y
		
	def visualize(self):
		global field
		typeName = self.__class__.__name__
		field[self.x][self.y] = typeName
		if typeName == "Player":
			self.index = canvas.create_image((self.x) * ENTITY_SIDE, (self.y) * ENTITY_SIDE, image=PLAYER_IMAGE, anchor=NW)
		elif typeName == "Wall":
			self.index = canvas.create_image((self.x) * ENTITY_SIDE, (self.y) * ENTITY_SIDE, image=WALL_IMAGE, anchor=NW)
		elif typeName == "EndPoint":
			self.index = canvas.create_image((self.x) * ENTITY_SIDE, (self.y) * ENTITY_SIDE, image=ENDPOINT_IMAGE, anchor=NW)
		elif typeName == "Bubble":
			self.index = canvas.create_image((self.x + 1) * ENTITY_SIDE + BUBBLE_DISTANCE, (self.y + 1) * ENTITY_SIDE + BUBBLE_DISTANCE, image=BUBBLE_IMAGE, anchor=CENTER)


class Player(Entity):
	pass

class Wall(Entity):
	pass

class EndPoint(Entity):
	pass

class Bubble(Entity):
	pass
	
class Level:
	def __init__(self, levelIndex, player, walls, endPoint):
		self.levelIndex = levelIndex
		self.player = player
		self.walls = walls
		self.endPoint = endPoint

	def visualize(self):
		self.player.visualize()
		for wall in self.walls:
			wall.visualize()
		self.endPoint.visualize()


def setWindowProperties(w, h):
	window = Tk()

	window.title("Orbox")

	ws = window.winfo_screenwidth()
	hs = window.winfo_screenheight()

	x = (ws/2) - (w/2)
	y = (hs/2) - (h/2)
	window.geometry('%dx%d+%d+%d' % (w, h, x, y))
	return window

def generateLevel(levelIndex):
	player = Player(8, 4)
	walls = []
	walls.append(Wall(17, 5))
	walls.append(Wall(12, 12))
	walls.append(Wall(13, 4))
	walls.append(Wall(18, 11))
	walls.append(Wall(8, 8))
	endPoint = EndPoint(22, 6)
	level = Level(levelIndex, player, walls, endPoint)
	#Todo replace this with level generating logic
	return level

def generateLevels():
	levels = []
	for x in range(9):
		levels.append(generateLevel(x))
	return levels

def overlapping(a,b):
	x = 0
	y = 0
	if direction == "left":
		x = -ENTITY_SIDE
	if direction == "right":
		x = ENTITY_SIDE
	if direction == "up":
		y = -ENTITY_SIDE
	if direction == "down":
		y = ENTITY_SIDE

	if a[0] + x < b[0] + ENTITY_SIDE and a[0] + ENTITY_SIDE + x > b[0] and a[1] + y < b[1] + ENTITY_SIDE and a[1] + ENTITY_SIDE + y > b[1]:
		return True
	return False
	
def overlappingEndPoint(a,b):
	if a[0] < b[0] + ENTITY_SIDE and a[0] + ENTITY_SIDE > b[0] and a[1] < b[1] + ENTITY_SIDE and a[1] + ENTITY_SIDE > b[1]:
		return True
	return False

def movePlayer():
	canvas.pack()
	global direction, isPlayerMoving
	isPlayerMoving = False
	levelPassed = False
	bubbles = []
	playerPosition = []
	playerPosition = canvas.coords(player.index)
	blockedDirections = []

	if(player.x < 30 and player.x >= -1 and player.y < 16 and player.y >= 1):
		if(field[player.x - 1][player.y] == "Wall"):
			blockedDirections.append("left")
		if(field[player.x + 1][player.y] == "Wall"):
			blockedDirections.append("right")
		if(field[player.x][player.y - 1] == "Wall"):
			blockedDirections.append("up")
		if(field[player.x][player.y + 1] == "Wall"):
			blockedDirections.append("down")
	x = 0
	y = 0
	if not levelPassed:
		if direction == "left" and not "left" in blockedDirections:
			x = -ENTITY_SIDE
			y = 0
			isPlayerMoving = True
		elif direction == "right" and not "right" in blockedDirections:
			x = ENTITY_SIDE
			y = 0
			isPlayerMoving = True
		elif direction == "up" and not "up" in blockedDirections:
			x = 0
			y = -ENTITY_SIDE
			isPlayerMoving = True
		elif direction == "down" and not "down" in blockedDirections:
			x = 0
			y = ENTITY_SIDE
			isPlayerMoving = True

		if not isPlayerMoving and 'gameOver' not in locals():
			window.after(PLAYER_SPEED, movePlayer)

		while isPlayerMoving:
			window.after(PLAYER_SPEED, automaticMove(player, player.index, x, y, bubbles))
			playerPosition = canvas.coords(player.index)
			endPosition = []
			endPosition = canvas.coords(endPoint.index)

			if player.x < 30 and player.x >= -1 and player.y < 16 and player.y >= 1:
				field[player.x][player.y] = ""


			if ((playerPosition[0] <= 0 and playerPosition[0] + ENTITY_SIDE <= 0) or (playerPosition[0] >= SCREEN_WIDTH and playerPosition[0] + ENTITY_SIDE >= SCREEN_WIDTH)) or ((playerPosition[1] <= 0 and playerPosition[1] + ENTITY_SIDE <= 0) or (playerPosition[1] >= SCREEN_HEIGHT and playerPosition[1] + ENTITY_SIDE >= SCREEN_HEIGHT)):
				gameOver = True
				isPlayerMoving = False
				gameOverText = canvas.create_text(SCREEN_WIDTH/2 , 20 , fill="white" , font="Times 20 italic bold", text="GAME OVER!")


			for wall in walls:
				wallPosition = canvas.coords(wall.index)
				if overlapping(playerPosition, wallPosition):
					isPlayerMoving = False
					direction = ""
					window.after(PLAYER_SPEED, movePlayer)


			if overlappingEndPoint(playerPosition, endPosition):
				isPlayerMoving = False
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
	bubbleX = int(position[0] / ENTITY_SIDE) - 1
	bubbleY = int(position[1] / ENTITY_SIDE) - 1
	if bubbleX >= -1 and bubbleX <= 30 and bubbleY >= -1 and bubbleY <= 16:
		bubble = Bubble(bubbleX, bubbleY)
		bubble.visualize()
		bubbles.append(bubble)
	
	canvas.move(index, x , y)

	if player.x < 30 and player.x >= -1 and player.y < 16 and player.y >= 1:
		field[player.x][player.y] = "Player"

def leftKey(event):
	global direction, isPlayerMoving
	if not isPlayerMoving:
		direction = "left"

def rightKey(event):
	global direction, isPlayerMoving
	if not isPlayerMoving:
		direction = "right"

def upKey(event):
	global direction, isPlayerMoving
	if not isPlayerMoving:
		direction = "up"

def downKey(event):
	global direction, isPlayerMoving
	if not isPlayerMoving:
		direction = "down"



window = setWindowProperties(SCREEN_WIDTH, SCREEN_HEIGHT)
canvas = Canvas(window, bg="black", width=SCREEN_WIDTH, height=SCREEN_HEIGHT)
canvas.pack()


PLAYER_IMAGE = PhotoImage(file = "resources/spaceship_transparent.png")
WALL_IMAGE = PhotoImage(file = "resources/wall_transparent.png")
ENDPOINT_IMAGE = PhotoImage(file = "resources/planet_transparent.png")
BUBBLE_IMAGE = PhotoImage(file = "resources/bubble_transparent.png")


canvas.bind("<Left>", leftKey)
canvas.bind("<Right>", rightKey)
canvas.bind("<Up>", upKey)
canvas.bind("<Down>", downKey)
canvas.focus_set()

isPlayerMoving = False

direction = ""
field = [["" for i in range(17)] for j in range(31)]

levels = generateLevels()

level = levels[0]
player = level.player
walls = level.walls
endPoint = level.endPoint
level.visualize()
movePlayer()
window.mainloop()

